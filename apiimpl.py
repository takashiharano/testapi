#==============================================================================
# Test API
# Copyright 2023 Takashi Harano
# Released under the MIT license
# https://github.com/takashiharano/testapi
# Created: 20231220
#==============================================================================
import os
import sys

ROOT_DIR = '../'
sys.path.append(os.path.join(os.path.dirname(__file__), ROOT_DIR + 'libs'))
import util

def main():
    params = util.get_request_param();

    obj = {}
    i = 0
    for key in params:
        obj[key] = params[key]
        i += 1

    if i == 0:
        obj = {'message': 'Hello!'}

    json = util.to_json(obj)
    util.send_response(json, 'application/json');
