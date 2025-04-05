/*!
 * Copyright 2025 Takashi Harano
 */
var apieditor = {};
var scnjs = apieditor;

scnjs.HTTP_STATUS = {
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

$onReady = function() {
  util.clock('#clock', '%YYYY-%MM-%DD %W %HH:%mm:%SS %Z');
  var url = location.href.replace(/editor\/$/, '');
  var urlLabel = scnjs.buildCopyableLabel(url);
  $el('#url').innerHTML = urlLabel;
  util.textarea.addStatusInfo('#data-body', '#textareainfo');
  $el('#data-header').focus();
};

scnjs.onSysReady = function() {
  scnjs.getData();
};

scnjs.reload = function() {
  scnjs.getData();
};

scnjs.getData = function() {
  var param = null;
  scnjs.callApi('get_data', param, scnjs.getDataCb);
};
scnjs.getDataCb = function(xhr, res, req) {
  if (xhr.status != 200) {
    scnjs.showInfotip('HTTP ' + xhr.status);
    return;
  }
  if (res.status == 'FORBIDDEN') {
    location.href = location.href;
    return;
  } else if (res.status != 'OK') {
    scnjs.showInfotip(res.status);
    return;
  }
  var data = res.body;
  var header = data.header;
  var body = data.body;
  $el('#data-header').value = header;
  $el('#data-body').value = body;
  scnjs.showInfotip('Data Loaded');
};

scnjs.saveData = function() {
  var header = $el('#data-header').value;
  var body = $el('#data-body').value;

  var param = {
    header: header,
    body: body
  };
  scnjs.callApi('save_data', param, scnjs.saveDataCb);
};
scnjs.saveDataCb = function(xhr, res, req) {
  if (xhr.status != 200) {
    scnjs.showInfotip('HTTP ' + xhr.status);
    return;
  }
  if (res.status == 'FORBIDDEN') {
    location.href = location.href;
    return;
  } else if (res.status != 'OK') {
    var m = res.status + ': ' + res.body
    scnjs.showInfotip(m);
    return;
  }
  scnjs.showInfotip('Saved');
};

scnjs.getRfc822DateString = function(t) {
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

scnjs.set200json = function() {
  var d = scnjs.getRfc822DateString();

  var b = '{"message":"Hello, World!"}';

  var contentLen = util.lenB(b);

  var h = '';
  h += 'HTTP/1.1 200 OK\n';
  h += 'Date: ' + d + '\n';
  h += 'Content-Type: application/json\n';
  h += 'Content-Length: ' + contentLen + '\n';

  scnjs.setData(h, b);
};

scnjs.setStatus = function(status) {
  var message = scnjs.HTTP_STATUS[status];
  if (!message) message = 'Unknown';
  scnjs.setDefaultData(status, message);
};

scnjs.setDefaultData = function(status, message) {
  var d = scnjs.getRfc822DateString();
  var statusMessage = status + ' ' + message;

  var b = '';
  if (!((status == 204) || (status == 304))) {
    b += '<!DOCTYPE html>\n';
    b += '<html>\n';
    b += '<head>\n';
    b += '<title>' + statusMessage + '</title>\n';
    b += '<meta charset="utf-8">\n';
    b += '</head>\n';
    b += '<body>\n';
    b += '<h1>' + statusMessage + '</h1>\n';
    b += '</body>\n';
    b += '</html>\n';
  }

  var h = '';
  h += 'HTTP/1.1 ' + statusMessage + '\n';
  h += 'Date: ' + d + '\n';
  h += 'Content-Type: text/html; charset=UTF-8\n';
  h += 'Content-Length: ' + util.lenB(b) + '\n';

  scnjs.setData(h, b);
};

scnjs.setData = function(h, b) {
  $el('#data-header').value = h;
  $el('#data-body').value = b;
};

scnjs.onStatusSet = function() {
  var status = $el('#status-code').value.trim();
  if (status.match(/[0-9]{3}/)) {
    scnjs.setStatus(status);
    $el('#status').value = '';
  } else {
    scnjs.showInfotip('Status code must be 3 digit number');
  }
};

scnjs.onStatusSelected = function() {
  var status = $el('#status').value;
  if (status) {
    scnjs.setStatus(status);
    $el('#status-code').value = '';
  }
};

scnjs.setDateField = function() {
  var d = scnjs.getRfc822DateString();
  scnjs.setHeaderField('Date', d, 2);
};

scnjs.setHeaderField = function(name, value, index) {
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

scnjs.onDataBodyChange = function() {
  var s = $el('#data-body').value;
  var b = util.lenB(s);
  scnjs.setHeaderField('Content-Length', b, -1);
};

scnjs.http = function(req, cb) {
  req.cb = cb;
  websys.http(req);
};

scnjs.callApi = function(act, params, cb) {
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
  scnjs.http(req, cb);
};

scnjs.showInfotip = function(m, d, o) {
  if (!o) o = {};
  o.style = {
    'font-size': '16px'
  };
  util.infotip.show(m, d, o);
};

scnjs.buildCopyableLabel = function(v, s) {
  if (!s) s = v;
  v = v.replace(/\\/g, '\\\\').replace(/'/g, '\\\'').replace(/"/g, '&quot;');
  var label = s;
  var r = '<span class="pseudo-link" onclick="scnjs.copy(\'' + v + '\');" data-tooltip2="Click to copy">' + label + '</span>';
  return r;
};

scnjs.copy = function(s) {
  util.copy(s);
  var o = {pos: 'pointer'};
  scnjs.showInfotip('Copied', 1000, o);
};

$onCtrlS = function(e) {
  if ($el('#data-header').hasFocus() || $el('#data-body').hasFocus()) {
    scnjs.saveData();
  }
};

$onEnterKey = function(e) {
  if ($el('#status-code').hasFocus()) {
    scnjs.onStatusSet();
  }
};
