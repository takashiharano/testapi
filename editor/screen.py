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

#------------------------------------------------------------------------------
def build_main_screen(context):
    html = '''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="robots" content="none">
<meta name="referrer" content="no-referrer">
<meta name="referrer" content="never">
<meta name="viewport" content="width=device-width,initial-scale=1">
'''
    html += '<title>Test API Editor</title>'
    html += '<link rel="stylesheet" href="style.css" />'
    html += '<script src="' + ROOT_PATH + 'libs/sha.js"></script>'
    html += '<script src="' + ROOT_PATH + 'libs/debug.js"></script>'
    html += '<script src="' + ROOT_PATH + 'libs/util.js"></script>'
    html += '<script src="' + ROOT_PATH + 'websys/websys.js"></script>'
    html += '<script src="main.js"></script>'
    html += '''<script src="./?res=js"></script>
</head>
<body>
<div id="body1">
<div id="header-line">
<div id="header-content">
<span id="title" style="margin-left:8px;"><span id="api">API</span> Emulator - Response Editor</span>
<span id="url-info" style="margin-left:16px;">API URL <span id="url"></span></span>
<span id="clock"></span>
</div>
</div>

<div id="content-wrapper">
<div>
<span id="led1" style="margin-right:4px;"></span><span class="item-name">Access Log</span>
<button class="button-small" onclick="main.clearAccessLog();">Clear</button>
<div id="console-area"><pre id="log-console"></pre></div>
</div>

<div style="margin-top:8px;margin-bottom:4px;">
<span>
<button class="button-large button-blue" onclick="main.save();">Save</button>
</span>

<span style="margin-left:16px;">
Status:
<span>
<button id="button-200" class="status-button" onclick="main.onSetStatusButton(200);" data-tooltip2="200 OK">200</button>
<button id="button-301" class="status-button" onclick="main.onSetStatusButton(301);" data-tooltip2="301 Moved Permanently">301</button>
<button id="button-401" class="status-button" onclick="main.onSetStatusButton(401);" data-tooltip2="401 Unauthorized">401</button>
<button id="button-403" class="status-button" onclick="main.onSetStatusButton(403);" data-tooltip2="403 Forbidden">403</button>
<button id="button-404" class="status-button" onclick="main.onSetStatusButton(404);" data-tooltip2="404 Not Found">404</button>
<button id="button-500" class="status-button" onclick="main.onSetStatusButton(500);" data-tooltip2="500 Internal Server Error">500</button>
<button id="button-503" class="status-button" onclick="main.onSetStatusButton(503);" data-tooltip2="503 Service Unavailable">503</button>
</span>

<input type="text" id="status-code" spellcheck="false"><button onclick="main.onStatusSet();" style="margin-left:4px;">Set</button>
<select id="status" onchange="main.onStatusSelected();">
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
</span>

<span style="margin-left:24px;">
<button onclick="main.setDateField();" data-tooltip="Set current date-time to Date field">Set Date:</button>
</span>

<span style="margin-left:24px;">
<button onclick="main.reload();">Reload</button>
</span>
</div>

<div id="data-area">
<div><span class="item-name">Headers</span></div>
<div id="data-header-wrappeer">
<textarea id="data-header" spellcheck="false"></textarea>
</div>

<div style="margin-top:16px;"><span class="item-name">Body</span></div>
<div id="data-body-wrappeer">
<textarea id="data-body" oninput="main.onDataBodyChange();" onchange="main.onDataBodyChange();" spellcheck="false"></textarea>
<div id="textareainfo"></div>
</div>
</div>

</div>
</div>
</body>
</html>
'''
    return html

#------------------------------------------------------------------------------
def build_forbidden_screen(context):
    html = '''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="robots" content="none">
<title>Test API</title>
</head>
<body>
FORBIDDEN
</body>
</html>
'''
    return html

#------------------------------------------------------------------------------
def build_auth_redirection_screen():
    html = '''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="robots" content="none">
<meta name="referrer" content="no-referrer">
<meta name="referrer" content="never">
'''
    html += '<script src="' + ROOT_PATH + 'libs/util.js"></script>'
    html += '<script src="' + ROOT_PATH + 'websys/websys.js"></script>'
    html += '<script src="./?res=js"></script>'
    html += '''
<script>
$onLoad = function() {
  websys.authRedirection(location.href);
};
</script>
</head>
<body>
</body>
</html>
'''
    return html

#------------------------------------------------------------------------------
def send_js():
    js = 'var main = main || {};'
    js += 'websys.init(\'' + ROOT_PATH + '/\', main.onSysReady);'
    util.send_response(js, 'text/javascript')

#------------------------------------------------------------------------------
def main():
    context = websys.on_access()
    res = util.get_request_param('res')
    if res == 'js':
        send_js()
        return

    if context.is_authorized():
        if context.has_permission('testapi'):
            html = build_main_screen(context)
        else:
            html = build_forbidden_screen(context)

    else:
        html = build_auth_redirection_screen()

    util.send_html(html)
