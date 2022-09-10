#!/usr/bin/env python3
import os
import re
from http.server import HTTPServer, SimpleHTTPRequestHandler, test

'''
This server takes inspiration from multiple solutions to provide:
* CORS enabled HTTPServer
    - https://gist.github.com/acdha/925e9ffc3d74ad59c3ea
* Allowing Range Request Server
    - https://github.com/danvk/RangeHTTPServer/blob/master/RangeHTTPServer
* Adding specific directory
    - https://stackoverflow.com/a/46332163
'''
class CustomRequestHandler (SimpleHTTPRequestHandler):
    """
    Creating a small HTTP request server
    """
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.send_header('Accept-Ranges', 'bytes')
        # self.send_header('Content-Type', 'application/octet-stream')
        SimpleHTTPRequestHandler.end_headers(self)
        
    def translate_path(self, path):
        path = SimpleHTTPRequestHandler.translate_path(self, path)
        relpath = os.path.relpath(path, os.getcwd())
        fullpath = os.path.join(self.server.base_path, relpath)
        return fullpath
    
    def copyfile(self, source, outputfile, start_byte=None, end_byte=None):
        if start_byte is not None and end_byte is not None:
            source.seek(start_byte)
            outputfile.write(source.read(end_byte))
        else:
            shutil.copyfileobj(source, outputfile)

class DevServer(HTTPServer):
    def __init__(self, base_path, server_address, RequestHandlerClass=CustomRequestHandler):
        self.base_path = base_path
        HTTPServer.__init__(self, server_address, RequestHandlerClass)

def serve(data_path,**kwargs):
    print("Warning, this is a development environment.\n"
          "This is not Recommended for production.")
    port = kwargs.get('port', 8888)
    host = kwargs.get('host', "localhost")
    # data_path = kwargs.get('path', ".")
    
    # print('data', data_path)
    # dir_path = os.path.join(os.path.dirname(__file__), data_path)
    # print('dir path', dir_path)
    # print('relative ', os.path.relpath(data_path, os.getcwd()))
    # print('join', os.path.join(os.getcwd(), data_path))
    httpd = DevServer(data_path, (host, port))
    httpd.serve_forever()
