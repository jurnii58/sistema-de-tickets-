from database import obtener_conexion
from typing import Optional

class Usuario:
    def __init__(self, id: Optional[int], nombre: str, tipo_usuario: str, contraseña: Optional[str] = None,
                 edad: Optional[int] = None, carrera: Optional[str] = None, matricula: Optional[str] = None, especialidad: Optional[str] = None):
        self.id = id
        self.nombre = nombre
        self.tipo_usuario = tipo_usuario
        self.contraseña = contraseña
        self.edad = edad
        self.carrera = carrera
        self.matricula = matricula
        self.especialidad = especialidad

    @staticmethod
    def crear_usuario(nombre, tipo_usuario, contraseña=None, edad=None, carrera=None, matricula=None, especialidad=None):
        conn = obtener_conexion()
        try:
            cur = conn.cursor()
            sql = """
                INSERT INTO usuarios (nombre, tipo_usuario, password, edad, carrera, matricula, especialidad)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
            """
            cur.execute(sql, (nombre, tipo_usuario, contraseña, edad, carrera, matricula, especialidad))
            conn.commit()
            uid = cur.lastrowid
            cur.close()
            return uid
        finally:
            conn.close()

    @staticmethod
    def obtener_por_username_y_contraseña(username, contraseña):
        conn = obtener_conexion()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute(
                "SELECT * FROM usuarios WHERE username = %s AND password = %s",
                (username, contraseña)
            )
            row = cur.fetchone()
            cur.close()
            return row
        finally:
            conn.close()


    @staticmethod
    def eliminar_usuario_por_id(uid):
        conn = obtener_conexion()
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM usuarios WHERE id = %s", (uid,))
            conn.commit()
            cur.close()
        finally:
            conn.close()
