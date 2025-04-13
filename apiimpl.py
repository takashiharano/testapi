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
try:
    import postalcode
except:
    pass

LOGS_PATH = './logs/'
DETAIL_LOGS_PATH = LOGS_PATH + 'details/'
DATA_FILE_PATH = './_data_.txt'
ACCESS_LOG_FILE_PATH = LOGS_PATH + 'access.log'
LOG_MAX = 20

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

    write_accesslog(now, status, headers, body)
    util.send_response(body, status=status, headers=headers)

def write_accesslog(timestamp, status, headers, body):
    std_in = util.read_stdin()
    try:
        std_in = std_in.decode()
    except:
        std_in = util.hexdump(std_in)

    info = {}
    info['timestamp'] = util.get_timestamp()
    info['method'] = os.environ.get('REQUEST_METHOD', '')
    info['addr'] = os.environ.get('REMOTE_ADDR', '')
    info['host']= util.get_host_name(info['addr'])
    info['ua'] = os.environ.get('HTTP_USER_AGENT', '')
    info['accept'] = os.environ.get('HTTP_ACCEPT', '')
    info['accept_lang'] = os.environ.get('HTTP_ACCEPT_LANGUAGE', '')
    info['accept_charset'] = os.environ.get('HTTP_ACCEPT_CHARSET', '')
    info['accept_encoding'] = os.environ.get('HTTP_ACCEPT_ENCODING', '')
    info['request_uri'] = os.environ.get('REQUEST_URI', '')
    info['referer'] = os.environ.get('HTTP_REFERER', '')
    info['remote_port'] = os.environ.get('REMOTE_PORT', '')
    info['remote_user'] = os.environ.get('REMOTE_USER', '')
    info['connection'] = os.environ.get('HTTP_CONNECTION', '')
    info['proxy_connection'] = os.environ.get('HTTP_PROXY_CONNECTION', '')
    info['via'] = os.environ.get('HTTP_VIA', '')
    info['x_forwarded_for'] = os.environ.get('HTTP_X_FORWARDED_FOR', '')
    info['x_forwarded_host'] = os.environ.get('HTTP_X_FORWARDED_HOST', '')
    info['x_forwarded_proto'] = os.environ.get('HTTP_X_FORWARDED_PROTO', '')
    info['query_string'] = os.environ.get('QUERY_STRING', '')
    info['content_type'] = os.environ.get('CONTENT_TYPE', '')
    info['content_length'] = os.environ.get('CONTENT_LENGTH', '')
    info['stdin'] = std_in
    info['status'] = status
    info['headers'] = headers
    info['body'] = body

    write_access_simple_log(timestamp, info)
    write_access_detail_log(timestamp, info)
    delete_old_access_detail_logs()

#------------------------------------------------------------------------------
def write_access_simple_log(timestamp, info):
    status = info['status']
    method = info['method']
    addr = info['addr']
    ua = info['ua']

    body = info['body']
    response_content_len = 0
    if body is not None:
        response_content_len = len(body)

    log_text = str(timestamp) + '\t' + method + '\t' + str(status) + '\t' + addr + '\t' + ua + '\t' + str(response_content_len)
    util.append_line_to_text_file(ACCESS_LOG_FILE_PATH, log_text, max=LOG_MAX)

#------------------------------------------------------------------------------
def write_access_detail_log(timestamp, info):
    status = str(info['status'])
    st_message = util.get_status_message(status)

    t = util.milli_to_micro(timestamp)
    dt = util.get_datetime_str(t)
    dt = dt[0:-3]

    s = dt + '\n\n'
    s += '[Request]\n'
    s += 'METHOD           : ' + info['method'] + '\n'
    s += 'ADDR             : ' + info['addr'] + '\n'
    s += 'HOST             : ' + info['host'] + '\n'
    s += 'User-Agent       : ' + info['ua'] + '\n'
    s += 'Accept           : ' + info['accept'] + '\n'
    s += 'Accept-Language  : ' + info['accept_lang'] + '\n'
    s += 'Accept-Encoding  : ' + info['accept_encoding'] + '\n'
    s += 'Accept-Charset   : ' + info['accept_charset'] + '\n'
    s += 'REQUEST_URI      : ' + info['request_uri'] + '\n'
    s += 'Referer          : ' + info['referer'] + '\n'
    s += 'Connection       : ' + info['connection'] + '\n'
    s += 'Proxy-Connection : ' + info['proxy_connection'] + '\n'
    s += 'Via              : ' + info['via'] + '\n'
    s += 'X-Forwarded-For  : ' + info['x_forwarded_for'] + '\n' 
    s += 'X-Forwarded-Host : ' + info['x_forwarded_host'] + '\n'
    s += 'X-Forwarded-Proto: ' + info['x_forwarded_proto'] + '\n'
    s += 'REMOTE_PORT      : ' + info['remote_port'] + '\n'
    s += 'REMOTE_USER      : ' + info['remote_user'] + '\n'
    s += 'QUERY_STRING     : ' + info['query_string'] + '\n'
    s += 'Content-Type     : ' + info['content_type'] + '\n'
    s += 'Content-Length   : ' + info['content_length'] + '\n'
    s += 'Body             : \n' + info['stdin'] + '\n'
    s += '\n'

    s += '[Response]\n';
    s += status + ' ' + st_message + '\n'

    headers = info['headers']
    for i in range(len(headers)):
        header = headers[i]
        for name in header:
            s += name + ': ' + header[name] + '\n'

    s += '\n'
    s += info['body']

    path = DETAIL_LOGS_PATH + str(timestamp) + '.txt'
    util.write_text_file(path, s)

#------------------------------------------------------------------------------
def delete_old_access_detail_logs():
    files = util.list_files(DETAIL_LOGS_PATH)
    files.sort()
    n = len(files)

    del_num = n - LOG_MAX
    if del_num <= 0:
        return

    del_files = files[0: del_num]
    for i in range(del_num):
        del_tartget = del_files[i]
        path = DETAIL_LOGS_PATH + del_tartget
        util.delete_file(path)

#----------------------------------------------------------
def main():
    api = util.get_request_param('api', '');

    func_name = 'api_' + api
    g = globals()
    if func_name in g:
        g[func_name]()
    else:
        send_response_from_data()
