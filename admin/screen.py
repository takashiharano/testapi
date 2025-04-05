#==============================================================================
# API EMULATOR - RESPONSE EDITOR SCREEN
# Copyright 2025 Takashi Harano
#==============================================================================
import os
import sys

ROOT_PATH = '../../'

sys.path.append(os.path.join(os.path.dirname(__file__), ROOT_PATH + 'libs'))
import util

util.append_system_path(__file__, ROOT_PATH + '/websys')
import websys

import js

#------------------------------------------------------------------------------
def build_main_screen(context):
    html = '''<!DOCTYPE html><html><head><meta charset="utf-8">
<meta name="robots" content="none">
<meta name="referrer" content="no-referrer">
<meta name="referrer" content="never">
<meta name="viewport" content="width=device-width,initial-scale=1">
'''
    html += '<title>Test API Admin</title>'
    html += '<link rel="stylesheet" href="style.css" />'
    html += '<script src="' + ROOT_PATH + 'libs/sha.js"></script>'
    html += '<script src="' + ROOT_PATH + 'libs/debug.js"></script>'
    html += '<script src="' + ROOT_PATH + 'libs/util.js"></script>'
    html += '<script src="' + ROOT_PATH + 'websys/websys.js"></script>'
    html += '<script src="apiadmin.js"></script>'
    html += '''<script src="./?res=js"></script>
</head>
<body>
<div id="body1">
<div id="header-line">
<span id="title">API EMULATOR - RESPONSE EDITOR</span>
<span style="margin-left:16px;">API URL <span id="url"></span></span>
<span id="clock"></span>
</div>

<div style="margin-top:8px;margin-bottom:4px;">
<button onclick="apiadmin.reload();">Reload</button>
<span style="margin-left:16px;">
<button onclick="apiadmin.saveData();">Save</button>
</span>

<span style="margin-left:32px;">
Status: 
<select id="status" onchange="apiadmin.onStatusSelected();">
<option value=""></option>
<optgroup label="1. Informational responses">
  <option value="100">100 Continue</option>
  <option value="101">101 Switching Protocols</option>
</optgroup>
<optgroup label="2. Successful responses">
  <option value="200">200 OK</option>
  <option value="201">201 Created</option>
  <option value="202">202 Accepted</option>
  <option value="203">203 Non-Authoritative Information</option>
  <option value="204">204 No Content</option>
  <option value="205">205 Reset Content</option>
  <option value="206">206 Partial Content</option>
</optgroup>
<optgroup label="3. Redirection messages">
  <option value="300">300 Multiple Choices</option>
  <option value="301">301 Moved Permanently</option>
  <option value="302">302 Found</option>
  <option value="303">303 See Other</option>
  <option value="304">304 Not Modified</option>
  <option value="305">305 Use Proxy</option>
  <option value="307">307 Temporary Redirect</option>
</optgroup>
<optgroup label="4. Client error responses">
  <option value="400">400 Bad Request</option>
  <option value="401">401 Unauthorized</option>
  <option value="402">402 Payment Required</option>
  <option value="403">403 Forbidden</option>
  <option value="404">404 Not Found</option>
  <option value="405">405 Method Not Allowed</option>
  <option value="406">406 Not Acceptable</option>
  <option value="407">407 Proxy Authentication Required</option>
  <option value="408">408 Request Time-out</option>
  <option value="409">409 Conflict</option>
  <option value="410">410 Gone</option>
  <option value="411">411 Length Required</option>
  <option value="412">412 Precondition Failed</option>
  <option value="413">413 Request Entity Too Large</option>
  <option value="414">414 Request-URI Too Large</option>
  <option value="415">415 Unsupported Media Type</option>
  <option value="416">416 Requested range not satisfiable</option>
  <option value="417">417 Expectation Failed</option>
  <option value="418">418 I'm a teapot</option>
</optgroup>
<optgroup label="5. Server error responses">
  <option value="500">500 Internal Server Error</option>
  <option value="501">501 Not Implemented</option>
  <option value="502">502 Bad Gateway</option>
  <option value="503">503 Service Unavailable</option>
  <option value="504">504 Gateway Time-out</option>
  <option value="505">505 HTTP Version not supported</option>
</optgroup>
</select>

<input type="text" id="status-code"><button onclick="apiadmin.onStatusSet();" style="margin-left:4px;">Set</button>
</span>

<span style="margin-left:32px;">
<button onclick="apiadmin.setDateField();">Set Date:</button>
</span>

<span style="margin-left:32px;">
<button onclick="apiadmin.set200json();">200 OK JSON</button>
</span>
</div>

<div id="data-area">
<div><span class="item-name">Headers</span></div>
<div id="data-header-wrappeer">
<textarea id="data-header"></textarea>
</div>

<div style="margin-top:16px;"><span class="item-name">Body</span></div>
<div id="data-body-wrappeer">
<textarea id="data-body" oninput="apiadmin.onDataBodyChange();" onchange="apiadmin.onDataBodyChange();"></textarea>
<div id="textareainfo"></div>
</div>
</div>

</div>
</body>
</html>'''
    return html

#------------------------------------------------------------------------------
def build_forbidden_screen(context):
    html = '''<!DOCTYPE html><html><head><meta charset="utf-8">
<meta name="robots" content="none">
<meta name="referrer" content="no-referrer">
<meta name="referrer" content="never">
<meta name="viewport" content="width=device-width,initial-scale=1">
'''
    html += '<title>Test API Admin</title>'
    html += '<link rel="stylesheet" href="style.css" />'
    html += '<script src="' + ROOT_PATH + 'libs/debug.js"></script>'
    html += '<script src="' + ROOT_PATH + 'libs/util.js"></script>'
    html += '<script src="' + ROOT_PATH + 'websys/websys.js"></script>'
    html += '''
</head>
<body>
FORBIDDEN
</body></html>'''
    return html

#------------------------------------------------------------------------------
def build_auth_redirection_screen():
    html = '''<!DOCTYPE html><html><head><meta charset="utf-8">
<meta name="robots" content="none">
<meta name="referrer" content="no-referrer">
<meta name="referrer" content="never">
'''
    html += '<script src="' + ROOT_PATH + 'libs/debug.js"></script>'
    html += '<script src="' + ROOT_PATH + 'libs/util.js"></script>'
    html += '<script src="' + ROOT_PATH + 'websys/websys.js"></script>'
    html += '<script src="./?res=js"></script>'
    html += '''
<script>
$onLoad = function() {
  websys.authRedirection(location.href);
};
</script>
</head><body></body></html>'''
    return html

#------------------------------------------------------------------------------
def main():
    context = websys.on_access()
    res = util.get_request_param('res')
    if res == 'js':
        js.main()
        return

    if context.is_authorized():
        if context.has_permission('testapi'):
            html = build_main_screen(context)
        else:
            html = build_forbidden_screen(context)

    else:
        html = build_auth_redirection_screen()

    util.send_html(html)
