#!python
#!/usr/bin/python3
#===============================
# Test API
# Copyright 2022 Takashi Harano
# Released under the MIT license
#===============================
import os
import sys

ROOT_DIR = '../'
sys.path.append(os.path.join(os.path.dirname(__file__), ROOT_DIR + 'libs'))
import util

util.append_system_path(__file__, './postalcode')
import postalcode

def hello():
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

#----------------------------------------------------------
def main():
    api = util.get_request_param('api', '');

    func_name = 'proc_' + api
    g = globals()
    if func_name in g:
        g[func_name]()
    else:
        hello()

main()
