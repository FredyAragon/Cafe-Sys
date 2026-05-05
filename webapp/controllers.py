import json
import mysql.connector
from database import get_connection

class AppController:
    
    @staticmethod
    def get_val(data, key):
        """Ayuda a obtener valores de formularios web"""
        return data.get(key, [''])[0]

    @staticmethod
    def responder_json(handler, datos, status=200):
        """Envía respuesta en formato JSON al navegador"""
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(datos).encode('utf-8'))

    @staticmethod
    def responder_html(handler, contenido):
        """Envía respuesta en formato HTML al navegador"""
        handler.send_response(200)
        handler.send_header("Content-type", "text/html; charset=utf-8")
        handler.end_headers()
        handler.wfile.write(contenido.encode('utf-8'))

    # --- LÓGICA DE USUARIOS ---
    def registrar_usuario(self, handler, form):
        nombre = self.get_val(form, 'nombre')
        email = self.get_val(form, 'email')
        password = self.get_val(form, 'password')

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)", (nombre, email, password))
            conn.commit()
            conn.close()
            self.responder_json(handler, {"exito": True})
        except Exception as e:
            self.responder_json(handler, {"exito": False, "mensaje": str(e)}, 500)

    def login_usuario(self, handler, form):
        email = self.get_val(form, 'email')
        password = self.get_val(form, 'password')

        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios WHERE email = %s AND password = %s", (email, password))
            usuario = cursor.fetchone()
            conn.close()

            if usuario:
                self.responder_json(handler, {"exito": True, "nombre": usuario['nombre']})
            else:
                self.responder_json(handler, {"exito": False, "mensaje": "Datos incorrectos"})
        except Exception as e:
            self.responder_json(handler, {"exito": False, "mensaje": str(e)}, 500)

    # --- LÓGICA DE CONTACTO ---
    def guardar_mensaje(self, handler, form):
        nombre = self.get_val(form, 'nombre')
        email = self.get_val(form, 'email')
        mensaje = self.get_val(form, 'mensaje')

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO mensajes (nombre, email, mensaje) VALUES (%s, %s, %s)", (nombre, email, mensaje))
            conn.commit()
            conn.close()
            self.responder_html(handler, "<h1>Mensaje Enviado</h1><a href='/templates/index.html'>Volver</a>")
        except Exception as e:
            print(e)

    # --- LÓGICA DE PEDIDOS ---
    def crear_pedido(self, handler, datos_json):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            sql = "INSERT INTO pedidos (cliente_nombre, detalle_productos, total) VALUES (%s, %s, %s)"
            cursor.execute(sql, (datos_json['cliente'], json.dumps(datos_json['productos']), datos_json['total']))
            conn.commit()
            conn.close()
            self.responder_json(handler, {"status": "ok"})
        except Exception as e:
            print(e)
            handler.send_error(500, str(e))

    # --- PANELES ADMIN ---
    def ver_pedidos(self, handler):
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM pedidos ORDER BY fecha DESC")
            pedidos = cursor.fetchall()
            conn.close()

            filas = ""
            for p in pedidos:
                # Intento de formatear bonito el JSON de productos
                try: 
                    prods = json.loads(p['detalle_productos'])
                    txt = "".join([f"<li>{x['nombre']} (${x['precio']})</li>" for x in prods])
                except (json.JSONDecodeError, KeyError, TypeError): 
                    txt = p['detalle_productos']

                filas += f"<tr><td>{p['cliente_nombre']}</td><td><ul>{txt}</ul></td><td>${p['total']}</td></tr>"
            
            html = f"""<html><head><link rel='stylesheet' href='/static/css/global.css'></head><body>
                    <div class='container'><h1>Pedidos</h1><table border='1' width='100%'>{filas}</table>
                    <br><a href='/templates/index.html' class='btn'>Volver</a></div></body></html>"""
            self.responder_html(handler, html)
        except Exception as e:
            self.responder_html(handler, f"Error: {e}")

    def ver_mensajes(self, handler):
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM mensajes ORDER BY fecha DESC")
            mensajes = cursor.fetchall()
            conn.close()

            filas = ""
            for m in mensajes:
                filas += f"<tr><td>{m['nombre']}</td><td>{m['email']}</td><td>{m['mensaje']}</td><td>{m['fecha']}</td></tr>"

            html = f"""<html><head><link rel='stylesheet' href='/static/css/global.css'></head><body>
                    <div class='container'><h1>Mensajes</h1><table border='1' width='100%'><tr><th>Nombre</th><th>Email</th><th>Mensaje</th><th>Fecha</th></tr>{filas}</table>
                    <br><a href='/templates/index.html' class='btn'>Volver</a></div></body></html>"""
            self.responder_html(handler, html)
        except Exception as e:
            self.responder_html(handler, f"Error: {e}")

    