from database import obtener_conexion
from computadora import Computadora

class Ticket:
    @staticmethod
    def listar_por_estado(estado):
        conn = obtener_conexion()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("""
                SELECT t.*, tec.nombre as tecnico_nombre
                FROM tickets t
                LEFT JOIN tecnicos tec ON t.tecnico_id = tec.id
                WHERE t.estado = %s
            """, (estado,))
            rows = cur.fetchall()
            cur.close()
            return rows
        finally:
            conn.close()

    @staticmethod
    def obtener_por_id(tid):
        conn = obtener_conexion()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT * FROM tickets WHERE id = %s", (tid,))
            row = cur.fetchone()
            cur.close()
            return row
        finally:
            conn.close()
