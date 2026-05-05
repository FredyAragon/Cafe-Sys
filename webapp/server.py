import http.server
import socketserver
import urllib.parse
import json
import os

# IMPORTACIONES (Asegúrate de que los archivos estén en la misma carpeta)
from database import inicializar_db
from controllers import AppController

PORT = 80
controller = AppController()

# Inicializamos DB al arrancar el servidor
inicializar_db()

class MiHandler(http.server.SimpleHTTPRequestHandler):
    
    def do_GET(self):
        # Redirección raíz
        if self.path == '/': self.path = '/templates/index.html'
        
        # Rutas Admin
        if self.path == '/ver_pedidos':
            controller.ver_pedidos(self)
            return

        if self.path == '/ver_mensajes':
            controller.ver_mensajes(self)
            return

        # Corrección de rutas templates
        if self.path.endswith('.html') and not self.path.startswith('/templates/'):
             self.path = '/templates' + self.path
        
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(length).decode('utf-8')
        
        # CASO 1: API JSON (Pedidos)
        if self.path == '/api/pedido':
            try:
                data = json.loads(post_data)
                controller.crear_pedido(self, data)
            except json.JSONDecodeError:
                self.send_error(400, "JSON Invalido")
            return

        # CASO 2: Formularios Normales
        form_data = urllib.parse.parse_qs(post_data)

        if self.path == '/register':
            controller.registrar_usuario(self, form_data)
        elif self.path == '/login':
            controller.login_usuario(self, form_data)
        elif self.path == '/enviar_mensaje':
            controller.guardar_mensaje(self, form_data)
        else:
            self.send_error(404, "Ruta desconocida")

print(f"☕ Servidor Modular corriendo en http://localhost:{PORT}")
socketserver.TCPServer.allow_reuse_address = True 
with socketserver.TCPServer(("", PORT), MiHandler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido.")
        httpd.server_close()