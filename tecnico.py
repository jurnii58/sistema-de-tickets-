from database import obtener_conexion

class Tecnico:
    @staticmethod
    def login(username, password):
        conn = obtener_conexion()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT * FROM tecnicos WHERE username=%s AND password=%s", (username, password))
            row = cur.fetchone()
            cur.close()
            return row
        finally:
            conn.close()

    @staticmethod
    def listar_tickets_asignados(tecnico_id):
        conn = obtener_conexion()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("""
                SELECT t.*, tec.nombre as tecnico_nombre
                FROM tickets t 
                LEFT JOIN tecnicos tec ON t.tecnico_id = tec.id 
                WHERE t.tecnico_id = %s
            """, (tecnico_id,))
            rows = cur.fetchall()
            cur.close()
            return rows
        finally:
            conn.close()

    @staticmethod
    def actualizar_estado(ticket_id, estado):
        if estado not in ('en_proceso','completado'):
            raise Exception('Estado inválido')
        conn = obtener_conexion()
        try:
            cur = conn.cursor()
            cur.execute("UPDATE tickets SET estado=%s, actualizado_en=NOW() WHERE id=%s", (estado, ticket_id))
            conn.commit()
            cur.close()
        finally:
            conn.close()
