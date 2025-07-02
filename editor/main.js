/*!
 * Copyright 2025 Takashi Harano
 */
var main = {};

main.HTTP_STATUS_MESSAGES = {
  100: 'Continue',
  101: 'Switching Protocols',
  200: 'OK',
  201: 'Created',
  202: 'Accepted',
  203: 'Non-Authoritative Information',
  204: 'No Content',
  205: 'Reset Content',
  206: 'Partial Content',
  300: 'Multiple Choices',
  301: 'Moved Permanently',
  302: 'Found',
  303: 'See Other',
  304: 'Not Modified',
  305: 'Use Proxy',
  307: 'Temporary Redirect',
  400: 'Bad Request',
  401: 'Unauthorized',
  402: 'Payment Required',
  403: 'Forbidden',
  404: 'Not Found',
  405: 'Method Not Allowed',
  406: 'Not Acceptable',
  407: 'Proxy Authentication Required',
  408: 'Request Time-out',
  409: 'Conflict',
  410: 'Gone',
  411: 'Length Required',
  412: 'Precondition Failed',
  413: 'Request Entity Too Large',
  414: 'Request-URI Too Large',
  415: 'Unsupported Media Type',
  416: 'Requested range not satisfiable',
  417: 'Expectation Failed',
  418: 'I\'m a teapot',
  500: 'Internal Server Error',
  501: 'Not Implemented',
  502: 'Bad Gateway',
  503: 'Service Unavailable',
  504: 'Gateway Time-out',
  505: 'HTTP Version not supported'
};

main.ST_NONE = 0;
main.ST_INITIALIED = 1;
main.INTERVAL = 1500;
main.apiurl = '';
main.autoReload = false;
main.status = main.ST_NONE;
main.latestLogTimestamp = -1;
main.activeStatus = -1;
main.logWindow = null;

$onReady = function() {
  dbg.init({zoom: 1.4});
  util.clock('#clock', '%YYYY-%MM-%DD %W %HH:%mm:%SS %Z');

  var url = location.href.replace(/editor\/$/, '');
  main.apiurl = url;
  var urlLabel = main.buildCopyableLabel(url);
  $el('#url').innerHTML = urlLabel;

  main.led1 = new util.Led('#led1');
  main.console1 = util.initConsole('#log-console');

  util.textarea.addStatusInfo('#data-body', '#textareainfo');
  $el('#data-header').focus();

  main.startAutoReload();
};

main.printLog = function(s) {
  main.console1.print(s);
};

main.writeLog = function(s) {
  main.console1.write(s);
};

main.onSysReady = function() {
  main.getData();
};

main.reload = function() {
  main.getData();
  main.inActiveButton();
};

main.getData = function() {
  var param = null;
  main.callApi('get_data', param, main.getDataCb);
};
main.getDataCb = function(xhr, res, req) {
  if (xhr.status != 200) {
    main.showInfotip('HTTP ' + xhr.status);
    return;
  }
  if (res.status == 'FORBIDDEN') {
    location.href = location.href;
    return;
  } else if (res.status != 'OK') {
    main.showInfotip(res.status);
    return;
  }
  var data = res.body;
  var header = data.header;
  var body = data.body;
  $el('#data-header').value = header;
  $el('#data-body').value = body;

  if (main.status & main.ST_INITIALIED) {
    main.showInfotip('Data Loaded');
  } else {
    main.status |= main.ST_INITIALIED;
  }
};

main.save = function() {
  main.saveData();
  main.activeStatus = -1;
  main.activeButton(-1);
};

main.activeButton = function(status) {
  main.inActiveButton();
  $el('#button-' + status).addClass('button-active');
};

main.inActiveButton = function() {
  $el('.status-button').removeClass('button-active');
};

main.saveData = function() {
  var header = $el('#data-header').value;
  var body = $el('#data-body').value;
  var param = {
    header: header,
    body: body
  };
  main.callApi('save_data', param, main.saveDataCb);
};
main.saveDataCb = function(xhr, res, req) {
  if (xhr.status != 200) {
    main.showInfotip('HTTP ' + xhr.status);
    return;
  }
  if (res.status == 'FORBIDDEN') {
    location.href = location.href;
    return;
  } else if (res.status != 'OK') {
    var m = res.status + ': ' + res.body
    main.showInfotip(m);
    return;
  }
  var m = 'Saved';
  var st = main.activeStatus;
  if (st >= 0) {
    m = 'HTTP status set to ' + st
  }
  main.showInfotip(m);
};

main.getRfc822DateString = function(t) {
  var MOS = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'};
  if (t === undefined) t = Date.now();
  dt = util.getDateTimeString(t, '%YYYY%MM%DD%HH%mm%SS%w', '+0');
  var yyyy = dt.substring(0, 4);
  var mm = dt.substring(4, 6);
  var dd = dt.substring(6, 8);
  var hh = dt.substring(8, 10);
  var mi = dt.substring(10, 12);
  var ss = dt.substring(12, 14);
  var w = dt.substring(14, 17);
  var mo = MOS[mm | 0];
  var d = w + ', ' + dd + ' ' + mo + ' ' + yyyy + ' ' + hh + ':' + mi + ':' + ss + ' GMT';
  return d;
};

main.buildBodyTemplate = function(status, statusMessage) {
  if (status == 200) {
    return main.buildBodyTemplate200();
  }
  var s = '';
  s += '<!DOCTYPE html>\n';
  s += '<html>\n';
  s += '<head>\n';
  s += '<title>' + statusMessage + '</title>\n';
  s += '<meta charset="utf-8">\n';
  s += '</head>\n';
  s += '<body>\n';
  s += '<h1>' + statusMessage + '</h1>\n';
  s += '</body>\n';
  s += '</html>\n';
  return s;
};

main.buildBodyTemplate200 = function() {
  return '{"message":"Hello, World!"}';
};

main.onSetStatusButton = function(status) {
  main.setResponseTemplate(status);
  $el('#status').value = '';
  $el('#status-code').value = '';
  main.saveData();
  main.activeStatus = status;
  main.activeButton(status);
};

main.getHttpStatusMessage = function(status) {
  var message = main.HTTP_STATUS_MESSAGES[status];
  if (!message) message = 'Unknown';
  return message;
};

main.setResponseTemplate = function(status) {
  status |= 0;

  var message = main.getHttpStatusMessage(status);

  var d = main.getRfc822DateString();
  var statusMessage = status + ' ' + message;

  var b = '';
  if (main.isBodyRequired(status)) {
    b += main.buildBodyTemplate(status, statusMessage);
  }

  var h = 'HTTP/1.1 ' + statusMessage + '\n';

  if (main.isDateHeaderRequired(status)) {
    h += 'Date: ' + d + '\n';
  }

  switch (status) {
    case 301:
    case 302:
    case 307:
      var url = main.apiurl + 'testpage.html';
      h += 'Location: ' + url + '\n';
      break;
    case 401:
      h += 'WWW-Authenticate: Basic\n';
      break;
  }

  if (main.isContentHeaderRequired(status)) {
    var contentType = main.getContentType(status);
    h += 'Content-Type: ' + contentType + '\n';
    h += 'Content-Length: ' + util.lenB(b) + '\n';
  }

  main.setData(h, b);
};

main.isDateHeaderRequired = function(status) {
  var excludeStatus = [300, 301, 302, 307];
  return !excludeStatus.includes(status);
};

main.isContentHeaderRequired = function(status) {
  var excludeStatus= [300, 301, 302, 307, 401];
  return !excludeStatus.includes(status);
};

main.getContentType = function(status) {
  var contentType = 'text/html; charset=UTF-8';
  if (status == 200) {
    contentType = 'application/json';
  }
  return contentType;
};

main.isBodyRequired = function(status) {
  var excludeStatus = [204, 300, 301, 302, 307, 304, 401];
  return !excludeStatus.includes(status);
};

main.setData = function(h, b) {
  $el('#data-header').value = h;
  $el('#data-body').value = b;
};

main.onStatusSet = function() {
  var status = $el('#status-code').value.trim();
  if (status.match(/[0-9]{3}/)) {
    main.setResponseTemplate(status);
    $el('#status').value = '';
    main.inActiveButton();
  } else {
    main.showInfotip('Status code must be 3 digit number');
  }
};

main.onStatusSelected = function() {
  var status = $el('#status').value;
  if (status) {
    main.setResponseTemplate(status);
    $el('#status-code').value = '';
    main.inActiveButton();
  }
};

main.setDateField = function() {
  var d = main.getRfc822DateString();
  main.setHeaderField('Date', d, 2);
};

main.setHeaderField = function(name, value, index) {
  var hv = name + ': ' + value;
  var h = $el('#data-header').value;
  var a = util.text2list(h);
  var b = [];
  var f = 0;
  var re = new RegExp(name + ':');
  for (var i = 0; i < a.length; i++) {
    var s = a[i].trim();
    if (s.match(re)) {
      s = hv;
      var f = 1;
    }
    if (s) b.push(s);
  }
  if (!f) {
    if ((index < 0) || (b.length < index)) {
      b.push(hv);
    } else {
      b.splice(index - 1, 0, hv);
    }
  }
  h = util.list2text(b);
  $el('#data-header').value = h;
};

main.onDataBodyChange = function() {
  var s = $el('#data-body').value;
  var b = util.lenB(s);
  main.setHeaderField('Content-Length', b, -1);
};

//-----------------------------------------------------------------------------
main.getAccessLog = function() {
  var param = {latest_timestamp: main.latestLogTimestamp};
  main.callApi('get_accesslog', param, main.getAccessLogCb);
};
main.getAccessLogCb = function(xhr, res, req) {
  if (xhr.status != 200) {
    var m = 'HTTP ' + xhr.status;
    if (xhr.status == 0) {
      m = 'CONNECTION ERROR';
    }
    main.showInfotip(m);
    main.onError();
    return;
  }
  if (res.status == 'FORBIDDEN') {
    location.href = location.href;
    return;
  } else if (res.status == 'NOT_MODIFIED') {
    util.IntervalProc.next('getlog');
    return;
  } else if (res.status != 'OK') {
    main.showInfotip(res.status);
    return;
  }
  var logs = res.body;
  main.printAccessLog(logs);
  util.IntervalProc.next('getlog');
};
main.printAccessLog = function(logs) {
  var s = '';
  var a = util.text2list(logs);
  for (var i = 0; i < a.length; i++) {
    var line = a[i];
    var fields = line.split('\t');
    var timestamp = +fields[0];
    var method = fields[1];
    var status = fields[2];
    var addr = fields[3];
    var ua = fields[4];
    var bLen = fields[5];

    main.latestLogTimestamp = timestamp;

    var dt = util.getDateTimeString(timestamp, '%YYYY-%MM-%DD %HH:%mm:%SS.%sss');
    var message = main.getHttpStatusMessage(status);

    var statusClass = 'status-ok';
    if (!(status.startsWith('1') || status.startsWith('2'))) {
      statusClass = 'status-err';
    }

    var m = '<span class="log-line" onclick="main.getAccessDetailLog(' + timestamp + ');">';
    m += dt + '\t' + method + '\t' + status + ' ' + message + '\t' + addr + '\t' + ua + '\t' + bLen + ' bytes'
    m += '</span>\n';
    s += m;
  }
  s = util.alignFields(s, '\t', 2);
  s = s.replace(/(  )([2].. .+?)(  )/g, '$1<span class="status-ok">$2</span>$3');
  s = s.replace(/(  )([4-9].. .+?)(  )/g, '$1<span class="status-err">$2</span>$3');
  main.writeLog(s);
};

main.clearAccessLog = function() {
  main.callApi('clear_accesslog', null, main.clearAccessLogCb);
};
main.clearAccessLogCb = function(xhr, res, req) {
  if (xhr.status != 200) {
    var m = 'HTTP ' + xhr.status;
    if (xhr.status == 0) {
      m = 'CONNECTION ERROR';
    }
    main.showInfotip(m);
    main.onError();
    return;
  }
  if (res.status == 'OK') {
    main.writeLog('');
  } else if (res.status == 'FORBIDDEN') {
    location.href = location.href;
  } else {
    main.showInfotip(res.status);
  }
};

//-----------------------------------------------------------------------------
main.getAccessDetailLog = function(id) {
  var param = {id: id};
  main.callApi('get_access_detail_log', param, main.getAccessDetailLogCb);
};
main.getAccessDetailLogCb = function(xhr, res, req) {
  if (xhr.status != 200) {
    var m = 'HTTP ' + xhr.status;
    if (xhr.status == 0) {
      m = 'CONNECTION ERROR';
    }
    main.showInfotip(m);
    main.onError();
    return;
  }
  if (res.status == 'FORBIDDEN') {
    location.href = location.href;
    return;
  } else if (res.status != 'OK') {
    main.showInfotip(res.status);
    return;
  }
  var logData = res.body;
  main.showAccessDetailLog(logData);
};
main.showAccessDetailLog = function(logData) {
  if (!main.logWindow) {
    main.logWindow = main.openLogWindow();
  }
  $el('#detail-log').value = logData;
};

main.openLogWindow = function() {
  html = '<div id="detail-log-wrapper">';
  html += '<textarea id="detail-log" class="no-line-break" readonly></textarea>';
  html += '</div>';
  var opt = {
    draggable: true,
    resizable: true,
    pos: 'c',
    closeButton: true,
    width: 800,
    height: 600,
    title: {
      text: 'Access Log'
    },
    body: {
      style: {
        background: '#fff'
      }
    },
    onclose: main.onLogWindowClose,
    content: html
  };
  var win = util.newWindow(opt);
  return win;
};

main.onLogWindowClose = function() {
  main.logWindow = null;
};

main.startAutoReload = function() {
  main.autoReload = true;
  var updateInterval = main.INTERVAL;
  util.IntervalProc.start('getlog', main.procInterval, updateInterval, null, true);
  main.led1.on();
};

main.stopAutoReload = function() {
  main.autoReload = false;
  main.led1.off();
};

main.procInterval = function() {
  if (main.autoReload) {
    main.getAccessLog();
  }
};

main.onError = function() {
  main.stopAutoReload();
  main.led1.on('#ffa0a0');
};

//-----------------------------------------------------------------------------
main.http = function(req, cb) {
  req.cb = cb;
  websys.http(req);
};

main.callApi = function(act, params, cb) {
  if (!params) params = {};
  var data = {act: act};
  if (params) {
    for (var k in params) {
      data[k] = params[k];
    }
  }
  var req = {
    url: 'api.cgi',
    method: 'POST',
    data: data,
    responseType: 'json'
  };
  main.http(req, cb);
};

main.showInfotip = function(m, d, o) {
  if (!o) o = {};
  o.style = {
    'font-size': '16px'
  };
  util.infotip.show(m, d, o);
};

main.buildCopyableLabel = function(v, s) {
  if (!s) s = v;
  v = v.replace(/\\/g, '\\\\').replace(/'/g, '\\\'').replace(/"/g, '&quot;');
  var label = s;
  var r = '<span class="pseudo-link" onclick="main.copy(\'' + v + '\');" data-tooltip2="Click to copy">' + label + '</span>';
  return r;
};

main.copy = function(s) {
  util.copy(s);
  var o = {pos: 'pointer'};
  main.showInfotip('Copied', 1000, o);
};

$onCtrlS = function(e) {
  if ($el('#data-header').hasFocus() || $el('#data-body').hasFocus()) {
    main.saveData();
  }
};

$onEnterKey = function(e) {
  if ($el('#status-code').hasFocus()) {
    main.onStatusSet();
  }
};
