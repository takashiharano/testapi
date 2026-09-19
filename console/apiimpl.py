#==============================================================================
# API EMULATOR - Console API
# Copyright 2025 Takashi Harano
#==============================================================================
import os
import sys

ROOT_PATH = '../../'
BASE_PATH = '../'

sys.path.append(os.path.join(os.path.dirname(__file__), ROOT_PATH + 'libs'))
import util

util.append_system_path(__file__, BASE_PATH)
import appconfig
import appcommon
import applogger

util.append_system_path(__file__, ROOT_PATH + 'websys')
try:
    import websys
except:
    pass

DATA_FILE_PATH = BASE_PATH + '_data_.txt'

#------------------------------------------------------------------------------
# Returns None if the value not found
def get_request_param(key, default=None):
    return util.get_request_param(key, default=default)

def get_request_param_as_int(key, default=0):
    return util.get_request_param_as_int(key, default)

def send_result_json(status, body=None):
    util.send_result_json(status, body)

def send_error_text(msg):
    b = msg.encode()
    util.send_as_file(b, filename='error.txt')

def proc_on_forbidden():
    send_result_json('FORBIDDEN')

#------------------------------------------------------------------------------
def proc_get_data(context):
    header = ''
    body = ''

    data = util.read_text_file(DATA_FILE_PATH, '')
    pos = data.find("\n\n")

    if pos >= 0:
        header = data[:pos] + '\n'
        body = data[pos + 2:]
    else:
        header = data

    o = {
        'header': header,
        'body': body
    }

    util.send_result_json('OK', body=o)

#------------------------------------------------------------------------------
def proc_save_data(context):
    header = get_request_param('header', '')
    body = get_request_param('body', '')

    header = header.strip()
    header = util.replace(header, '\n{2,}', '')

    data = header + '\n\n' + body

    try:
        util.write_text_file(DATA_FILE_PATH, data)
        status = 'OK'
        body = None
    except Exception as e:
        status = 'ERROR'
        body = str(e)

    write_log(data)
    util.send_result_json(status, body=body)

#------------------------------------------------------------------------------
def write_log(data):
    timestamp = util.get_unixtime_millis()

    o = appcommon.parse_data(data)
    status = o['status']

    headers = [{'name': 'User-Agent', 'value': 'Test API Console'}]

    info = {}
    info['method'] = '#SET#'
    info['addr'] = os.environ.get('REMOTE_ADDR', '')
    info['status'] = status
    info['request_headers'] = headers
    info['body'] = data

    applogger.write_log(timestamp, info)

#------------------------------------------------------------------------------
def proc_get_logs(context):
    latest_timestamp = get_request_param_as_int('latest_timestamp', -1)
    data = applogger.get_log()
    a = util.text2list(data)
    if len(a) > 0 and latest_timestamp >= 0:
        latest_line = a[-1]
        if latest_line != '':
            log_fields = latest_line.split('\t')
            timestamp = int(log_fields[0])
            if timestamp == latest_timestamp:
                util.send_result_json('NOT_MODIFIED', body=None)
                return

    util.send_result_json('OK', body=data)

#------------------------------------------------------------------------------
def proc_clear_logs(context):
    applogger.clear_log()
    applogger.clear_detailed_logs()
    util.send_result_json('OK', body=None)

#------------------------------------------------------------------------------
def proc_get_detailed_log(context):
    id = get_request_param('id', '')
    data = applogger.get_detailed_log(id)

    status = 'OK'
    if data is None:
        status = 'NOT_FOUND'
    util.send_result_json(status, body=data)

#------------------------------------------------------------------------------
def proc_api(context, act):
    status = 'OK'
    result = None
    func_name = 'proc_' + act
    g = globals()
    if func_name in g:
        g[func_name](context)
    else:
        util.send_result_json('PROC_NOT_FOUND:' + act, None)

#------------------------------------------------------------------------------
def main():
    context = None
    if 'websys' in sys.modules:
        context = websys.on_access()

    act = get_request_param('act')

    if appconfig.console_auth_required:
        if 'websys' in sys.modules:
            if context.is_authorized():
                if context.has_permission(appconfig.console_app_permission_name):
                    proc_api(context, act)
                else:
                    proc_on_forbidden()
            else:
                proc_on_forbidden()
        else:
            util.send_result_json('MODULE_LOAD_ERROR', body=None)
    else:
        proc_api(context, act)
