from database import obtener_conexion

class Computadora:
    def __init__(self, codigo, ubicacion=None, estado='disponible', observaciones=None, ultimo_mantenimiento=None):
        self.codigo = codigo
        self.ubicacion = ubicacion
        self.estado = estado
        self.observaciones = observaciones
        self.ultimo_mantenimiento = ultimo_mantenimiento

    def guardar(self):
        conn = obtener_conexion()
        try:
            cur = conn.cursor()
            sql = (
                "INSERT INTO computadoras (codigo, ubicacion, estado, observaciones, ultimo_mantenimiento) "
                "VALUES (%s,%s,%s,%s,%s) "
                "ON DUPLICATE KEY UPDATE ubicacion=VALUES(ubicacion), estado=VALUES(estado), "
                "observaciones=VALUES(observaciones), ultimo_mantenimiento=VALUES(ultimo_mantenimiento)"
            )
            cur.execute(sql, (self.codigo, self.ubicacion, self.estado, self.observaciones, self.ultimo_mantenimiento))
            conn.commit()
            cur.close()
        finally:
            conn.close()

    @staticmethod
    def eliminar(codigo):
        conn = obtener_conexion()
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM computadoras WHERE codigo = %s", (codigo,))
            conn.commit()
            cur.close()
        finally:
            conn.close()

    @staticmethod
    def listar():
        conn = obtener_conexion()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT * FROM computadoras")
            rows = cur.fetchall()
            cur.close()
            return rows
        finally:
            conn.close()

    @staticmethod
    def obtener_por_codigo(codigo):
        conn = obtener_conexion()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT * FROM computadoras WHERE codigo = %s", (codigo,))
            row = cur.fetchone()
            cur.close()
            return row
        finally:
            conn.close()

    @staticmethod
    def obtener_por_id(cid):
        conn = obtener_conexion()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT * FROM computadoras WHERE id = %s", (cid,))
            row = cur.fetchone()
            cur.close()
            return row
        finally:
            conn.close()
