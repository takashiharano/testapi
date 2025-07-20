#==================================
# Test API Logging Module
# Copyright (c) 2025 Takashi Harano
# Released under the MIT license
#==================================
import os
import sys

LOGS_PATH = os.path.join(os.path.dirname(__file__), './logs/')
DETAILED_LOGS_PATH = LOGS_PATH + 'details/'
LOG_FILE_PATH = LOGS_PATH + 'testapi.log'

sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
import appcommon

sys.path.append(appcommon.LIB_PATH)
import util

LOG_MAX = 20

#------------------------------------------------------------------------------
def write_log(timestamp, info):
    status = info['status']
    method = info['method']
    addr = info['addr']
    request_headers = info['request_headers']
    uafield = util.get_dict_by_key(request_headers, 'name', 'User-Agent')
    if uafield is None:
        ua = ''
    else:
        ua = uafield['value']

    body = info['body']
    response_content_len = 0
    if body is not None:
        response_content_len = len(body)

    log_text = str(timestamp) + '\t' + method + '\t' + str(status) + '\t' + addr + '\t' + ua + '\t' + str(response_content_len)
    util.append_line_to_text_file(LOG_FILE_PATH, log_text, max=LOG_MAX)

#------------------------------------------------------------------------------
def get_log():
    data = util.read_text_file(LOG_FILE_PATH, '')
    return  data

#------------------------------------------------------------------------------
def clear_log():
    util.write_text_file(LOG_FILE_PATH, '')

#------------------------------------------------------------------------------
def write_detailed_log(timestamp, info):
    status = str(info['status'])
    st_message = util.get_status_message(status)

    t = util.milli_to_micro(timestamp)
    dt = util.get_datetime_str(t)
    dt = dt[0:-3]

    request_headers = info['request_headers']
    name_max_len = count_key_max_len(request_headers)
    if name_max_len < 12:
        name_max_len = 12

    s = dt + '\n\n'
    s += '-------------------------------------------------------------------------------\n'
    s += 'Request\n'
    s += '-------------------------------------------------------------------------------\n'
    s += util.rpad('Method', ' ', name_max_len) + ': ' + info['method'] + '\n'
    s += util.rpad('Request URI', ' ', name_max_len) + ': ' + info['request_uri'] + '\n'
    s += util.rpad('Query String', ' ', name_max_len) + ': ' + info['query_string'] + '\n'

    s += '\n'
    s += '[Remote Host]\n'
    s += util.rpad('IP Address', ' ', name_max_len) + ': ' + info['addr'] + '\n'
    s += util.rpad('Host Name', ' ', name_max_len) + ': ' + info['host'] + '\n'
    s += util.rpad('Remote Port', ' ', name_max_len) + ': ' + info['remote_port'] + '\n'
    s += util.rpad('Remote User', ' ', name_max_len) + ': ' + info['remote_user'] + '\n'

    s += '\n'
    s += '[Headers]\n'
    for i in range(len(request_headers)):
        header = request_headers[i]
        header_name = header['name']
        header_value = header['value']
        s += util.rpad(header_name, ' ', name_max_len) + ': ' + header_value + '\n'

    s += '\n'
    s += '[Body]\n'
    s  += info['stdin'] + '\n'
    s += '\n'

    s += '-------------------------------------------------------------------------------\n'
    s += 'Response\n';
    s += '-------------------------------------------------------------------------------\n'
    s += '[Headers]\n'
    s += status + ' ' + st_message + '\n'

    headers = info['headers']
    for i in range(len(headers)):
        header = headers[i]
        for name in header:
            s += name + ': ' + header[name] + '\n'

    s += '\n'
    s += '[Body]\n'
    s += info['body']

    path = DETAILED_LOGS_PATH + str(timestamp) + '.txt'
    util.write_text_file(path, s)

#------------------------------------------------------------------------------
def get_detailed_log(id):
    path = DETAILED_LOGS_PATH + id + '.txt'
    data = util.read_text_file(path, None)
    return data

#------------------------------------------------------------------------------
def delete_old_detailed_logs():
    files = util.list_files(DETAILED_LOGS_PATH)
    files.sort()
    n = len(files)

    del_num = n - LOG_MAX
    if del_num <= 0:
        return

    del_files = files[0: del_num]
    for i in range(del_num):
        del_tartget = del_files[i]
        path = DETAILED_LOGS_PATH + del_tartget
        util.delete_file(path)

#------------------------------------------------------------------------------
def clear_detailed_logs():
    files = util.list_files(DETAILED_LOGS_PATH)
    for i in range(len(files)):
        del_tartget = files[i]
        path = DETAILED_LOGS_PATH + del_tartget
        util.delete_file(path)

#------------------------------------------------------------------------------
def count_key_max_len(dict):
    max = 0
    for i in range(len(dict)):
        item = dict[i]
        name = item['name']
        n = len(name)
        if n > max:
            max = n
    return max
