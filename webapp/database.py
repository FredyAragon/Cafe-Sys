import mysql.connector
import os
import time # Importante para las pausas

DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'db'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', ''), 
    'database': os.environ.get('DB_NAME', 'cafeteria_db')
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def inicializar_db():
    print(f">> 🛠️ Verificando Base de Datos en host: {DB_CONFIG['host']}...")
    
    intentos = 0
    max_intentos = 10
    
    while intentos < max_intentos:
        try:
            # 1. Intentar conectar al host
            conn_base = mysql.connector.connect(
                host=DB_CONFIG['host'], 
                user=DB_CONFIG['user'], 
                password=DB_CONFIG['password']
            )
            cursor_base = conn_base.cursor()
            cursor_base.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
            conn_base.close()

            # 2. Crear Tablas
            conn = get_connection()
            cursor = conn.cursor()
            
            tablas = [
                """CREATE TABLE IF NOT EXISTS usuarios (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    email VARCHAR(100) NOT NULL UNIQUE,
                    password VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )""",
                """CREATE TABLE IF NOT EXISTS mensajes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    email VARCHAR(100) NOT NULL,
                    mensaje TEXT NOT NULL,
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )""",
                """CREATE TABLE IF NOT EXISTS pedidos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    cliente_nombre VARCHAR(100),
                    detalle_productos TEXT,
                    total DECIMAL(10, 2),
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )"""
            ]

            for sql in tablas:
                cursor.execute(sql)

            conn.commit()
            conn.close()
            print("✅ Base de datos lista y tablas verificadas.")
            return # Salir del bucle si todo salió bien

        except mysql.connector.Error as err:
            intentos += 1
            print(f"⏳ MySQL no está listo aún (intento {intentos}/{max_intentos}). Esperando...")
            time.sleep(5) # Esperar 5 segundos antes de reintentar
            
    print("❌ No se pudo conectar a MySQL tras varios intentos.")