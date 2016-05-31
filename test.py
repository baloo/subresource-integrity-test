from http.server import HTTPServer, SimpleHTTPRequestHandler
import base64
import hashlib

STYLE = b"""
@font-face {
  font-family: 'blah';
  font-style: normal;
  font-weight: 400;
  src: local('blah'), url(inconsolata.woff2) format('woff2');
}

h1 {
  font-family: 'blah';
}
"""

_style_hash = hashlib.new('sha384')
_style_hash.update(STYLE)

INDEX = b"""
<!DOCTYPE html>
<html lang="en">
<head>
<link rel="stylesheet" href="style.css" integrity="sha384-%s"/>
</head>
<body>
<h1>
Hello, world!
</h1>
</body>
</html>
""" % base64.b64encode(_style_hash.digest())


class SubResourceHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            return self.send_content(INDEX, 'text/html')
        if self.path == '/style.css':
            return self.send_content(STYLE, 'text/css')

        super(SubResourceHandler, self).do_GET()

    def send_content(self, content, ct):
        self.send_response(200)
        self.send_header('Content-Length', str(len(content)))
        self.send_header('Content-Type', ct)
        self.end_headers()

        self.wfile.write(content)
        self.wfile.flush()


def run(server_class=HTTPServer, handler_class=SubResourceHandler):
    server_address = ('', 8123)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == '__main__':
    run()
