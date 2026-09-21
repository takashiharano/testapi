# TestAPI
Browser-based HTTP/1.1 API emulator and response editor.  
Configure arbitrary status codes, response headers and bodies, and inspect incoming request logs from the browser.

## Requirements
- Python 3 and a CGI-capable web server
- Util libraries https://libutil.com/
  - util.js
  - util.py

### Optional
- websys https://github.com/takashiharano/websys

`websys` is required only when console authentication is enabled in `appconfig.py`. It is not required by default.

## Deploy
Edit the shebang in `index.cgi`, `console/index.cgi` and `console/api.cgi` to the Python path of your web server.  
Deploy the files to the server as below:

```
/
|
+- testapi/
|  |
|  +- apiimpl.py [644]
|  +- appcommon.py [644]
|  +- appconfig.py [644]
|  +- applogger.py [644]
|  +- index.cgi [755]
|  +- test.html [644]
|  |
|  +- console/
|     |
|     +- api.cgi [755]
|     +- apiimpl.py [644]
|     +- index.cgi [755]
|     +- main.js [644]
|     +- screen.py [644]
|     +- style.css [644]
|
+- libs/
   |
   +- util.js
   +- util.py
```
When console authentication is enabled, deploy `websys` at `/websys/`.

The web server process must be able to write the response data and log files used by TestAPI.  
Create the runtime paths as needed and grant write permission to the web server process:

```
testapi/_data_.txt
testapi/logs/testapi.log
testapi/logs/details/
```

Console authentication is configured in `appconfig.py`:

```python
console_auth_required = False
console_app_permission_name = 'testapi'
```

Set `console_auth_required` to `True` when `websys` authentication is used.

## Usage
Open the console:

```
http(s)://SERVER/testapi/console/
```

Edit the HTTP response headers and body, then click **Apply**.  
The configured response is served at:

```
http(s)://SERVER/testapi/
```

For example, the response data can be configured as:

```http
HTTP/1.1 200 OK
Date: Sat, 19 Sep 2026 12:20:28 GMT
Content-Type: application/json
Content-Length: 27

{"message": "Hello, World!"}
```

The console provides quick templates for common HTTP status codes such as `200`, `301`, `400`, `401`, `403`, `404`, `500` and `503`.  
Other status codes can be selected from the status list or entered manually. **Auto Apply** immediately saves a selected template, **Set Date** updates the `Date` header, and **Revert** reloads the currently saved response.

`Content-Length` is updated automatically when the response body is edited.

![testapi1](https://github.com/user-attachments/assets/1c8014b7-2a95-4ba7-a68e-3906c405329a)

## Built-in APIs
The `api` query parameter can be used to call several built-in test endpoints instead of the configured response.

```text
http(s)://SERVER/testapi/?api=hello
http(s)://SERVER/testapi/?api=hello&name=Alice
http(s)://SERVER/testapi/?api=ip
http(s)://SERVER/testapi/?api=host
http(s)://SERVER/testapi/?api=status&code=404
```

Examples:

```text
GET /testapi/?api=hello
{"message": "Hello!"}
```

```text
GET /testapi/?api=hello&name=Alice
{"message": "Hello, Alice!"}
```

```text
GET /testapi/?api=status&code=404
HTTP/1.1 404 Not Found
```

## Access Logs
Requests handled by the configurable API are recorded in the console.  
The log shows the request time, method, response status, remote IP address, User-Agent and response size.

Click a request log entry to inspect detailed request and response information, including headers and body.  
The logger keeps up to 20 recent entries and detailed logs by default.

## License
MIT License
