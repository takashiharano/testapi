#==============================================================================
# API EMULATOR - RESPONSE EDITOR
# Copyright 2025 Takashi Harano
#==============================================================================
import os
import sys

ROOT_PATH = '../../'

sys.path.append(os.path.join(os.path.dirname(__file__), ROOT_PATH + 'libs'))
import util

util.append_system_path(__file__, ROOT_PATH + 'websys')
import websys

DATA_DIR = util.get_relative_path(__file__, '../../../private/websys/')
GROUPS_DATA_FILE_PATH = DATA_DIR + 'groups.json'

DATA_FILE_PATH = '../_data_.txt'
LOG_FILE_PATH = '../_access.log'

#------------------------------------------------------------------------------
# Returns None if the value not found
def get_request_param(key, default=None):
    return websys.get_request_param(key, default=default)

def get_request_param_as_int(key):
    return websys.get_request_param_as_int(key)

def send_result_json(status, body=None):
    websys.send_result_json(status, body)

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

    websys.send_result_json('OK', body=o)

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
    websys.send_result_json(status, body=body)

#------------------------------------------------------------------------------
def proc_get_accesslog(context):
    data = util.read_text_file(LOG_FILE_PATH, '')
    websys.send_result_json('OK', body=data)

def proc_clear_accesslog(context):
    util.write_text_file(LOG_FILE_PATH, '')
    websys.send_result_json('OK', body=None)

#------------------------------------------------------------------------------
def proc_api(context, act):
    status = 'OK'
    result = None
    func_name = 'proc_' + act
    g = globals()
    if func_name in g:
        g[func_name](context)
    else:
        websys.send_result_json('PROC_NOT_FOUND:' + act, None)

#------------------------------------------------------------------------------
def main():
    context = websys.on_access()
    act = get_request_param('act')

    if context.is_authorized():
        if context.has_permission('testapi'):
            proc_api(context, act)
            return

    proc_on_forbidden()
