from http.server import HTTPServer, SimpleHTTPRequestHandler
import base64
import hashlib

STYLE = b"""
body {
  font-family: sans-serif;
}

/* latin-ext */
@font-face {
  font-family: 'Aguafina Script';
  font-style: normal;
  font-weight: 400;
  src: local('Aguafina Script Regular'), local('AguafinaScript-Regular'), url(aguafinascript-regular-latin-ext.woff2) format('woff2');
  unicode-range: U+0100-024F, U+1E00-1EFF, U+20A0-20AB, U+20AD-20CF, U+2C60-2C7F, U+A720-A7FF;
}
/* latin */
@font-face {
  font-family: 'Aguafina Script';
  font-style: normal;
  font-weight: 400;
  src: local('Aguafina Script Regular'), local('AguafinaScript-Regular'), url(aguafinascript-regular-latin.woff2) format('woff2');
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02C6, U+02DA, U+02DC, U+2000-206F, U+2074, U+20AC, U+2212, U+2215, U+E0FF, U+EFFD, U+F000;
}


h1 {
  font-family: 'Aguafina Script', cursive;
  font-style: normal;
  font-weight: 400;
}
"""

_style_hash = hashlib.new('sha384')
_style_hash.update(STYLE)

INDEX = b"""
<!DOCTYPE html>
<html lang="en">
<head>
<link rel="stylesheet" type="text/css" href="style.css" integrity="sha384-%s"/>
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
