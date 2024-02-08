import http.server
import socketserver

# Define el puerto en el que se ejecutará el servidor
PORT = 8000

# Define el manejador del servidor web
class MiHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Maneja las solicitudes GET
        super().do_GET()

# Configura el servidor web con el manejador definido
with socketserver.TCPServer(("0.0.0.0", PORT), MiHandler) as httpd:
    print("Servidor web en el puerto", PORT)
    # Inicia el servidor y espera solicitudes
    httpd.serve_forever()