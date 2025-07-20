#==================================
# Test API Common Module
# Copyright (c) 2025 Takashi Harano
# Released under the MIT license
#==================================
import os
import sys

ROOT_PATH = '../'
LIB_PATH = os.path.join(os.path.dirname(__file__), ROOT_PATH + 'libs')
sys.path.append(LIB_PATH)
import util

#------------------------------------------------------------------------------
def parse_data(data):
    header = ''
    body = ''

    pos = data.find("\n\n")

    if pos >= 0:
        header = data[:pos] + '\n'
        body = data[pos + 2:]
    else:
        header = data

    header_lines = util.text2list(header)
    status_line = header_lines[0]

    status_code = util.extract_string(status_line, r'.+([0-9]{3}).+')
    try:
        status = int(status_code)
    except:
        status = 200

    headers = []
    for i in range(1, len(header_lines)):
        header_field = header_lines[i]
        fields = header_field.split(': ')
        name = fields[0]
        value = fields[1]
        headers.append({name: value})

    o = {
        'status': status,
        'headers': headers,
        'body': body
    }

    return o
