#==============================================================================
# API EMULATOR - RESPONSE SETTER SCREEN
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
<span id="title">API EMULATOR - RESPONSE SETTER</span>
<span id="clock"></span>
</div>
<div style="margin:8px 0 12px 0;">URL <span id="url"></span></div>
<div style="margin-top:8px;margin-bottom:8px;">
<button onclick="apiadmin.reload();">Reload</button>
<button onclick="apiadmin.saveData();">Save</button>
<span style="margin-left:64px;">
Status: 
<input type="text" id="status"><button onclick="apiadmin.setStatus($el('#status').value);" style="margin-left:4px;">Set</button>
<button onclick="apiadmin.set200();" style="margin-left:8px;">200</button>
<button onclick="apiadmin.setStatus(404);">404</button>
<button onclick="apiadmin.setStatus(500);">500</button>
<button onclick="apiadmin.setStatus(503);">503</button>
</span>
</div>

<div id="data-area">
<div><span class="item-name">Headers</span></div>
<div id="data-header-wrappeer">
<textarea id="data-header"></textarea>
</div>

<div style="margin-top:16px;"><span class="item-name">Body</span></div>
<div id="data-body-wrappeer">
<textarea id="data-body"></textarea>
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
