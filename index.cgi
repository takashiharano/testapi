#!python
#!/usr/bin/python3
#===============================
# Test API
# Copyright 2025 Takashi Harano
# Released under the MIT license
#===============================
import os
import sys

ROOT_DIR = '../'
sys.path.append(os.path.join(os.path.dirname(__file__), ROOT_DIR + 'libs'))
import util

util.append_system_path(__file__, './postalcode')
import postalcode

DATA_FILE_PATH = './_data_.txt'

def proc_hello():
    name = util.get_request_param('name', '');
    text = 'Hello'
    if name != '':
        text += ', ' + name
    text += '!'
    json = '{"message": "' + text + '"}'
    util.send_response(json, 'application/json');

def proc_host():
    addr = os.environ.get('REMOTE_ADDR', '')
    try:
        host = socket.gethostbyaddr(addr)[0]
    except Exception as e:
        host = '(no host name)'
    
    print('Content-Type: text/plain');
    print();
    print(host, end='')

def proc_ip():
    addr = os.environ.get('REMOTE_ADDR', '')
    print('Content-Type: text/plain')
    print()
    print(addr, end='')

def proc_status():
    p_code = util.get_request_param('code', '');
    try:
        code = int(p_code)
    except:
        code = 200

    message = util.get_status_message(p_code)

    html = '<!DOCTYPE html>'
    html += '<html>'
    html += '<head>'
    html += '<meta charset="utf-8">'
    html += '<title>HTTP Status Code Test</title>'
    html += '</head>'
    html += '<body>'
    html += 'HTTP ' + message
    html += '</body>'
    html += '</html>'

    util.send_response(html, 'text/html', status=code)

def proc_postalcode():
    postalcode.webmain()

def send_response_from_data():
    header = ''
    body = ''

    data = util.read_text_file(DATA_FILE_PATH, '')
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

    util.send_response(body, status=status, headers=headers)

#----------------------------------------------------------
def main():
    api = util.get_request_param('api', '');

    func_name = 'proc_' + api
    g = globals()
    if func_name in g:
        g[func_name]()
    else:
        send_response_from_data()

main()
