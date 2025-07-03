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

    write_access_simple_log(timestamp, info)
    write_access_detail_log(timestamp, info)
    delete_old_access_detail_logs()

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

#------------------------------------------------------------------------------
def write_access_simple_log(timestamp, info):
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
    util.append_line_to_text_file(ACCESS_LOG_FILE_PATH, log_text, max=LOG_MAX)

#------------------------------------------------------------------------------
def write_access_detail_log(timestamp, info):
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

#----------------------------------------------------------
def main():
    api = util.get_request_param('api', '');

    func_name = 'api_' + api
    g = globals()
    if func_name in g:
        g[func_name]()
    else:
        send_response_from_data()
