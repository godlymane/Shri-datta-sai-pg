"""Serve Shri Datta Sai PG site."""
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os, sys, socket

os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Handler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

port = int(sys.argv[1]) if len(sys.argv) > 1 else 8888

server = HTTPServer(("0.0.0.0", port), Handler)
server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print(f"Shri Datta Sai PG site live on port {port}")
print(f"PC:    http://localhost:{port}")
print(f"Phone: http://192.168.1.12:{port}")
server.serve_forever()
