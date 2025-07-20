#==================================
# Test API
# Copyright (c) 2025 Takashi Harano
# Released under the MIT license
#==================================
import os
import sys

ROOT_DIR = '../'
sys.path.append(os.path.join(os.path.dirname(__file__), ROOT_DIR + 'libs'))
import util

import appcommon
import applogger

util.append_system_path(__file__, './postalcode')
try:
    import postalcode
except:
    pass

DATA_FILE_PATH = './_data_.txt'

#------------------------------------------------------------------------------
def api_hello():
    name = util.get_request_param('name', '');
    text = 'Hello'
    if name != '':
        text += ', ' + name
    text += '!'
    json = '{"message": "' + text + '"}'
    util.send_response(json, 'application/json');

#------------------------------------------------------------------------------
def api_host():
    addr = os.environ.get('REMOTE_ADDR', '')
    try:
        host = socket.gethostbyaddr(addr)[0]
    except Exception as e:
        host = '(no host name)'
    
    print('Content-Type: text/plain');
    print();
    print(host, end='')

#------------------------------------------------------------------------------
def api_ip():
    addr = os.environ.get('REMOTE_ADDR', '')
    print('Content-Type: text/plain')
    print()
    print(addr, end='')

#------------------------------------------------------------------------------
def api_status():
    p_code = util.get_request_param('code', '');
    try:
        code = int(p_code)
    except:
        code = 200

    message = p_code + ' ' + util.get_status_message(p_code)

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

#------------------------------------------------------------------------------
def api_postalcode():
    if 'postalcode' in sys.modules:
        postalcode.webmain()
    else:
        util.send_response('postalcode module is required.');

#------------------------------------------------------------------------------
def send_response_from_data():
    now = util.get_unixtime_millis()

    data = util.read_text_file(DATA_FILE_PATH, '')
    o = appcommon.parse_data(data)
    status = o['status']
    headers = o['headers']
    body = o['body']

    write_accesslog(now, status, headers, body)
    util.send_response(body, status=status, headers=headers)

#------------------------------------------------------------------------------
def write_accesslog(timestamp, status, headers, body):
    std_in = util.read_stdin()
    try:
        std_in = std_in.decode()
    except:
        std_in = util.hexdump(std_in)

    info = {}
    info['timestamp'] = util.get_timestamp()
    info['method'] = os.environ.get('REQUEST_METHOD', '')
    info['request_uri'] = os.environ.get('REQUEST_URI', '')
    info['addr'] = os.environ.get('REMOTE_ADDR', '')
    info['host']= util.get_host_name(info['addr'])
    info['remote_port'] = os.environ.get('REMOTE_PORT', '')
    info['remote_user'] = os.environ.get('REMOTE_USER', '')
    info['query_string'] = os.environ.get('QUERY_STRING', '')
    info['request_headers'] = get_request_headers()
    info['stdin'] = std_in
    info['status'] = status
    info['headers'] = headers
    info['body'] = body

    applogger.write_log(timestamp, info)
    applogger.write_detailed_log(timestamp, info)
    applogger.delete_old_detailed_logs()

#------------------------------------------------------------------------------
def get_request_headers():
    headers = []

    keys = []
    for key, value in os.environ.items():
        if key.startswith('HTTP_') or key in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
            name = normalize_header_name(key)
            o = {
                'name': name,
                'value': value
            }
            headers.append(o)

    headers = util.sort_object_list(headers, 'name')

    return headers

#------------------------------------------------------------------------------
# env_key: 'HTTP_USER_AGENT' -> 'User-Agent'
def normalize_header_name(env_key):
    raw = env_key[5:] if env_key.startswith('HTTP_') else env_key
    parts = raw.lower().split('_')

    exceptions = {
        'cdn': 'CDN',
        'ch': 'CH',
        'dns': 'DNS',
        'dnt': 'DNT',
        'etag': 'ETag',
        'fpm': 'FPM',
        'gpc': 'GPC',
        'id': 'ID',
        'ip': 'IP',
        'php': 'PHP',
        'ssl': 'SSL',
        'te': 'TE',
        'ua': 'UA',
        'wow64': 'WoW64',
        'www': 'WWW',
        'xss': 'XSS'
    }

    normalized = []
    for part in parts:
        if part in exceptions:
            normalized.append(exceptions[part])
        else:
            normalized.append(part.capitalize())
    return '-'.join(normalized)

#----------------------------------------------------------
def main():
    api = util.get_request_param('api', '');

    func_name = 'api_' + api
    g = globals()
    if func_name in g:
        g[func_name]()
    else:
        send_response_from_data()
