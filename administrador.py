from database import obtener_conexion
from computadora import Computadora

class Administrador:
    @staticmethod
    def listar_tickets_pendientes():
        conn = obtener_conexion()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("""
                SELECT t.*, tec.nombre AS tecnico_nombre
                FROM tickets t
                LEFT JOIN tecnicos tec ON t.tecnico_id = tec.id
                WHERE t.estado = 'pendiente'
            """)
            rows = cur.fetchall()
            cur.close()
            return rows
        finally:
            conn.close()

    @staticmethod
    def listar_todos_los_tickets():
        conn = obtener_conexion()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("""
                SELECT t.id, t.alumno_nombre, c.codigo AS codigo_equipo,
                       t.descripcion, tec.nombre AS tecnico_nombre, t.estado
                FROM tickets t
                LEFT JOIN computadoras c ON t.computadora_id = c.id
                LEFT JOIN tecnicos tec ON t.tecnico_id = tec.id
                ORDER BY t.id DESC
            """)
            rows = cur.fetchall()
            cur.close()
            return rows
        finally:
            conn.close()

    @staticmethod
    def asignar_ticket(ticket_id, tecnico_id):
        conn = obtener_conexion()
        try:
            cur = conn.cursor()
            cur.execute("""
                UPDATE tickets 
                SET tecnico_id=%s, estado='asignado', actualizado_en = NOW() 
                WHERE id = %s
            """, (tecnico_id, ticket_id))
            conn.commit()
            cur.close()
        finally:
            conn.close()

    @staticmethod
    def agregar_computadora(codigo, ubicacion=None, observaciones=None):
        comp = Computadora(codigo=codigo, ubicacion=ubicacion, observaciones=observaciones)
        comp.guardar()

    @staticmethod
    def eliminar_computadora(codigo):
        Computadora.eliminar(codigo)

    @staticmethod
    def agregar_tecnico(nombre, username, password, especialidad):
        conn = obtener_conexion()
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO tecnicos (nombre, username, password, especialidad)
                VALUES (%s, %s, %s, %s)
            """, (nombre, username, password, especialidad))
            conn.commit()
            tid = cur.lastrowid
            cur.close()
            return tid
        finally:
            conn.close()

    @staticmethod
    def eliminar_tecnico_por_id(tid):
        conn = obtener_conexion()
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM tecnicos WHERE id = %s", (tid,))
            conn.commit()
            cur.close()
        finally:
            conn.close()
