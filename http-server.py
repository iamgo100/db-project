import socket
from email.parser import Parser
from functools import lru_cache
from urllib.parse import parse_qs, urlparse

MAX_LINE = 64*1024
MAX_HEADERS = 100

class MyHTTPServer:
    def __init__(self, host, port, serverName):
        self._host = host
        self._port = port
        self._serverName = serverName
        
    def serve_forever(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
        try:
            sock.bind((self._host, self._port))
            sock.listen(10)
            while True:
                conn, addr = sock.accept()
                try:
                    self.serve_client(conn)
                except Exception as e:
                    print('Client serving failed', e)
        finally:
            sock.close()
    
    def serve_client(self, conn):
        try:
            req = self.parse_request(conn)
            res = self.handle_request(req)
            self.send_response(conn, res)
        except ConnectionResetError:
            conn = None
        except Exception as e:
            self.send_error(conn, e)
        
        if conn:
            req.rfile.close()
            conn.close()
    
    def parse_request(self, conn):
        rfile = conn.makefile('rb')
        method, target, ver = self.parse_request_line(rfile)
        headers = self.parse_headers(rfile)
        host = headers.get('Host')
        if not host:
            raise HTTPError(400, 'Bad request', 'Host header is missing')
        if host not in (self._serverName, f'{self._serverName}:{self._port}'):
            raise HTTPError(404, 'Not found')
        return Request(method, target, ver, headers, rfile)
        
    def parse_request_line(self, rfile):
        raw = rfile.readline(MAX_LINE + 1)
        if len(raw) > MAX_LINE:
            raise HTTPError(400, 'Bad request', 'Request line is too long')
        
        reqLine = str(raw, 'iso-8859-1')
        reqLine = reqLine.rstrip('\r\n')
        words = reqLine.split()
        if len(words) != 3:
            raise HTTPError(400, 'Bad request','Malformed request line')
        
        method, target, ver = words
        if ver != 'HTTP/1.1':
            raise HTTPError(505, 'HTTP Version Not Supported')
        return method, target, ver
    
    def parse_headers(self, rfile):
        headers = []
        while True:
            line = rfile.readline(MAX_LINE + 1)
            if len(line) > MAX_LINE:
                raise HTTPError(494, 'Request header too large')
            if line in (b'\r\n', b'\n', b''):
                break
            headers.append(line)
            if len(headers) > MAX_HEADERS:
                raise HTTPError(494, 'Too many headers')
        
        sheaders = b''.join(headers).decode('iso-8859-1')
        return Parser().parsestr(sheaders)
    
    def handle_request(self, req):
        # обработка запросов
        if req.path == '/users' and req.method == 'GET':
            return self.handle_get_users(req)
        
        # если ничего не вернулось, значит:
        raise HTTPError(404, 'Not Found')
    
    def send_response(self, conn, res):
        wfile = conn.makefile('wb')
        statusLine = f'HTTP/1.1 {res.status} {res.reason}\r\n'
        wfile.write(statusLine.encode('iso-8859-1'))
        
        if res.hesders:
            for (key, value) in res.headers:
                headerLine = f'{key}: {value}\r\n'
                wfile.write(headerLine.encode('iso-8859-1'))
        wfile.write(b'\r\n')
        
        if res.body:
            wfile.write(res.body)
        
        wfile.flush()
        wfile.close()
    
    def send_error(self, conn, err):
        try:
            status = err.status
            reason = err.reason
            body = (err.body or err.reason).encode('utf-8')
        except:
            status = 500
            reason = b'Internal Server Error'
            body = b'Internal Server Error'
        res = Response(status, reason,
                       [('Content-Length', len(body))],
                       body)
        self.send_response(conn, res)

    def handle_get_users(self, req):
        # сделать что-то с этим запросом (пример):
        accept = req.headers.get('Accept')
        if 'text/html' in accept:
            contentType = 'text/html; charset=utf-8'
            # организуем body
        elif 'application/json' in accept:
            contentType = 'application/json; charset=utf-8'
            # по-другому организуем body
        else:
            # https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/406
            return Response(406, 'Not Acceptable')
        body = body.encode('utf-8')
        headers = [('Content-Type', contentType),
                   ('Content-Length', len(body))]
        # и вернуть ответ:
        return Response(200, 'OK', headers, body)

class Request:
    def __init__(self, method, target, version, headers, rfile):
        self.method = method
        self.target = target
        self.version = version
        self.headers = headers
        self.rfile = rfile
    
    @property
    def path(self):
        return self.url.path
    
    @property
    @lru_cache(maxsize=None)
    def query(self):
        return parse_qs(self.url.query)
    
    @property
    @lru_cache(maxsize=None)
    def url(self):
        return urlparse(self.target)
    
    def body(self):
        size = self.headers.get('Content-Length')
        if not size:
            return None
        return self.rfile.read(size)

class Response:
    def __init__(self, status, reason, headers = None, body = None):
        self.status = status
        self.reason = reason
        self.headers = headers
        self.body = body

class HTTPError(Exception):
    def __init__(self, status, reason, body = None):
        super()
        self.status = status
        self.reason = reason
        self.body = body

if __name__ == "__main__":
    host = 'localhost'
    port = '9090'
    name = 'example.local'
    
    server = MyHTTPServer(host, port, name)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
