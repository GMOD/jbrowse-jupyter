#!/usr/bin/env python3
import os
import re
from http.server import HTTPServer, SimpleHTTPRequestHandler

'''
This server takes inspiration from multiple solutions to provide:
* CORS enabled HTTPServer
    - https://gist.github.com/acdha/925e9ffc3d74ad59c3ea
* Allowing Range Request Server
    - https://github.com/danvk/RangeHTTPServer/blob/master/RangeHTTPServer
* Adding specific directory
    - https://stackoverflow.com/a/46332163
'''
# CREDIT FOR ENABLING RANGE REQUEST HTTP SERVER:
# lines 20-31, 34,37-52, 59-107
# https://github.com/danvk/RangeHTTPServer/blob/master/RangeHTTPServer


def copy_byte_range(infile, outfile, start=None, stop=None, bufsize=16*1024):
    '''Like shutil.copyfileobj, but only copy a range of the streams.
    Both start and stop are inclusive.
    '''
    if start is not None:
        infile.seek(start)
    while 1:
        to_read = min(bufsize, stop + 1 - infile.tell() if stop else bufsize)
        buf = infile.read(to_read)
        if not buf:
            break
        outfile.write(buf)


BYTE_RANGE_RE = re.compile(r'bytes=(\d+)-(\d+)?$')


def parse_byte_range(byte_range):
    """
    Returns the two numbers in 'bytes=123-456' or throws ValueError.
    The last number or both numbers may be None.
    """
    if byte_range.strip() == '':
        return None, None

    m = BYTE_RANGE_RE.match(byte_range)
    if not m:
        raise ValueError('Invalid byte range %s' % byte_range)

    first, last = [x and int(x) for x in m.groups()]
    if last and last < first:
        raise ValueError('Invalid byte range %s' % byte_range)
    return first, last


class CustomRequestHandler (SimpleHTTPRequestHandler):
    """
    Creating a small HTTP request server
    """
    def send_head(self):
        if 'Range' not in self.headers:
            self.range = None
            return SimpleHTTPRequestHandler.send_head(self)
        try:
            self.range = parse_byte_range(self.headers['Range'])
        except ValueError:
            self.send_error(400, 'Invalid byte range')
            return None
        first, last = self.range

        # Mirroring SimpleHTTPServer.py here
        path = self.translate_path(self.path)
        f = None
        ctype = self.guess_type(path)
        try:
            f = open(path, 'rb')
        except IOError:
            self.send_error(404, 'File not found')
            return None

        fs = os.fstat(f.fileno())
        file_len = fs[6]
        if first >= file_len:
            self.send_error(416, 'Requested Range Not Satisfiable')
            return None

        self.send_response(206)
        self.send_header('Content-type', ctype)

        if last is None or last >= file_len:
            last = file_len - 1
        response_length = last - first + 1

        self.send_header('Content-Range',
                         'bytes %s-%s/%s' % (first, last, file_len))
        self.send_header('Content-Length', str(response_length))
        self.send_header('Last-Modified', self.date_time_string(fs.st_mtime))
        self.end_headers()
        return f

    def copyfile(self, source, outputfile):
        if not self.range:
            return SimpleHTTPRequestHandler.copyfile(self, source, outputfile)

        # SimpleHTTPRequestHandler uses shutil.copyfileobj, which doesn't let
        # you stop the copying before the end of the file.
        start, stop = self.range  # set in send_head()
        copy_byte_range(source, outputfile, start, stop)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Expose-Headers', '*')
        self.send_header('Accept-Ranges', 'bytes')
        # self.send_header('Content-Type', 'application/octet-stream')
        SimpleHTTPRequestHandler.end_headers(self)

    def translate_path(self, path):
        path = SimpleHTTPRequestHandler.translate_path(self, path)
        relpath = os.path.relpath(path, os.getcwd())
        fullpath = os.path.join(self.server.base_path, relpath)
        return fullpath


class DevServer(HTTPServer):
    def __init__(self, base_path, server_address,
                 RequestHandlerClass=CustomRequestHandler):
        self.base_path = base_path
        HTTPServer.__init__(self, server_address, RequestHandlerClass)


def serve(data_path, **kwargs):
    """
    Launches a development http server. It is not recommended
    for production.

    e.g
    serve('./path/to/data', port=8080, host='localhost')

    :param str data_path: path to file directory to serve
        defaults to the current working dir
    :param int port: (optional) port to utilize when running
        the dev server, defaults to 8080
    :param str host: (optional) host to utilize when running
        the dev server, default to localhost
    """
    print("=============================================")
    print("Warning: \n"
          "This is a development environment.\n"
          "This is not recommended for production.")
    port = kwargs.get('port', 8080)
    host = kwargs.get('host', "localhost")
    # data_path = kwargs.get('path', ".")
    # print('data', data_path)
    # dir_path = os.path.join(os.path.dirname(__file__), data_path)
    # print('dir path', dir_path)
    # print('relative ', os.path.relpath(data_path, os.getcwd()))
    # print('join', os.path.join(os.getcwd(), data_path))
    httpd = DevServer(data_path, (host, port))
    server = f'http://{host}:{port}'
    print("=============================================")
    print(f'Server is now running at \n "{server}"')
    httpd.serve_forever()
