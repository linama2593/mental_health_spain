import http.server
import socketserver
import threading

PORT = 8000

class MiHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        super().do_GET()

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

with ThreadedTCPServer(("0.0.0.0", PORT), MiHandler) as httpd:
    print("Servidor web en el puerto", PORT)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.shutdown()