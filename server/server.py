# Across the Aisle (across-the-aisle)
# July 2019
 
from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
import json
from urllib.parse import parse_qs
from AcrossAisle import interpretPage

# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
 
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    # GET
    def do_GET(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type','application/json')
        self.end_headers()

        # Send message back to client
        message = "Hello world!"
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return

    def do_POST(self):
        self._set_headers()
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'}
        )
        url = form.getvalue("url")
        print(url)
        ret = interpretPage(url)
        print(ret)

        self.wfile.write((json.dumps(ret)).encode())

def run():
    print('starting server...')

    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server, you need root access
    server_address = ('127.0.0.1', 8081)
    httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
    print('running server on port 8081')
    httpd.serve_forever()
 
 
run()