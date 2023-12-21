#==============================================================================
# Test API
# Copyright 2023 Takashi Harano
# Released under the MIT license
# https://github.com/takashiharano/testapi
# Created: 20231220
# Updated: 20231221
#==============================================================================
import os
import sys
import time

ROOT_DIR = '../'
sys.path.append(os.path.join(os.path.dirname(__file__), ROOT_DIR + 'libs'))
import util

LOG_FILE_PATH =  './api.log'
DATA_MAX_RECORDS = 1000

#------------------------------------------------------------------------------
def main():
    method = os.environ.get('REQUEST_METHOD', '')
    addr = os.environ.get('REMOTE_ADDR', '')

    params = util.get_request_param();

    obj = {'method': method}
    i = 0
    for key in params:
        obj[key] = params[key]
        i += 1

    if i == 0:
        obj = {'message': 'Hello!'}

    j = util.to_json(obj)

    save_log(method, addr, j)

    util.send_response(j, 'application/json');

#------------------------------------------------------------------------------
def save_log(method, addr, m):
    date_time = util.get_datetime_str('%Y-%m-%dT%H:%M:%S.%f') + util.get_tz(True)
    s = date_time + ' ' + addr + ' ' + method + ' ' + m

    lock_file_path = 'lock'
    wait = 0.25
    retry = 50
    cnt = 0
    while True:
        if not os.path.exists(lock_file_path):
            try:
                os.makedirs(lock_file_path)
                util.append_line_to_text_file(LOG_FILE_PATH, s, max=DATA_MAX_RECORDS)
                os.rmdir(lock_file_path)
                break
            except:
                pass
        cnt += 1
        if cnt > retry:
            break
        time.sleep(wait)
