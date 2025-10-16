import mysql.connector
from mysql.connector import Error

def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='technodes1'
        )
        if conexion.is_connected():
            return conexion
    except Error as e:
        print(f"❌ Error al conectar con la base de datos: {e}")
    raise Exception("No se pudo establecer la conexión con la base de datos.")

def crear_tablas_si_no_existen():
    conn = None
    try:
        # Intentamos conectar; si la base de datos no existe, creamos la BD y volvemos a conectar
        try:
            conn = obtener_conexion()
        except Exception as e:
            # intentar crear la base de datos si no existe
            try:
                tmp = mysql.connector.connect(host='localhost', user='root', password='')
                cur = tmp.cursor()
                cur.execute("CREATE DATABASE IF NOT EXISTS technodes CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
                cur.close()
                tmp.close()
                conn = obtener_conexion()
            except Exception as e2:
                print("❌ No se pudo crear la base de datos automáticament:", e2)
                raise

        cur = conn.cursor()

        # Usuarios
        cur.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            tipo ENUM('alumno','administrador','tecnico') NOT NULL,
            username VARCHAR(100) NULL,
            password VARCHAR(255) NULL,
            edad INT NULL,
            carrera VARCHAR(100) NULL,
            matricula VARCHAR(50) NULL,
            especialidad ENUM('redes','hardware','software') NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB;
        """)

        # Computadoras
        cur.execute("""
        CREATE TABLE IF NOT EXISTS computadoras (
            codigo VARCHAR(50) PRIMARY KEY,
            ubicacion VARCHAR(100) NULL,
            estado ENUM('disponible','en_mantenimiento','no_disponible') DEFAULT 'disponible',
            observaciones TEXT NULL,
            ultimo_mantenimiento TIMESTAMP NULL
        ) ENGINE=InnoDB;
        """)

        # Tickets
        cur.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INT AUTO_INCREMENT PRIMARY KEY,
            alumno_nombre VARCHAR(100) NOT NULL,
            alumno_edad INT NULL,
            alumno_carrera VARCHAR(100) NULL,
            alumno_matricula VARCHAR(50) NULL,
            computadora_id VARCHAR(50) NOT NULL,
            descripcion TEXT,
            estado ENUM('pendiente','asignado','en_proceso','completado') DEFAULT 'pendiente',
            tecnico_id INT NULL,
            creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            actualizado_en TIMESTAMP NULL,
            FOREIGN KEY (tecnico_id) REFERENCES usuarios(id) ON DELETE SET NULL
        ) ENGINE=InnoDB;
        """)

        # Mantenimientos
        cur.execute("""
        CREATE TABLE IF NOT EXISTS mantenimientos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            computadora_id VARCHAR(50) NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            descripcion TEXT
        ) ENGINE=InnoDB;
        """)

        conn.commit()
        cur.close()
        print("✅ Tablas creadas/verificadas correctamente.")
    except Exception as e:
        if conn:
            conn.rollback()
        print("❌ Error al crear tablas:", e)
        raise
    finally:
        if conn and conn.is_connected():
            conn.close()
