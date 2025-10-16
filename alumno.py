from database import obtener_conexion
from computadora import Computadora

class Alumno:
    @staticmethod
    def listar_computadoras():
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
    def levantar_ticket(nombre, edad, carrera, matricula, codigo_equipo, descripcion):
        # Buscar computadora por código
        comp = Computadora.obtener_por_codigo(codigo_equipo)
        if not comp:
            raise Exception(f"No existe la computadora con código {codigo_equipo}")

        computadora_id = comp["id"]  # obtener el id real

        conn = obtener_conexion()
        try:
            cur = conn.cursor()
            sql = ("INSERT INTO tickets (alumno_nombre, alumno_edad, alumno_carrera, alumno_matricula, computadora_id, descripcion, estado) "
                   "VALUES (%s,%s,%s,%s,%s,%s,'pendiente')")
            cur.execute(sql, (nombre, edad, carrera, matricula, computadora_id, descripcion))
            conn.commit()
            tid = cur.lastrowid
            cur.close()
            return tid
        finally:
            conn.close()

    @staticmethod
    def obtener_ultimo_mantenimiento(codigo_equipo):
        # Buscar computadora por código
        comp = Computadora.obtener_por_codigo(codigo_equipo)
        if not comp:
            raise Exception(f"No existe la computadora con código {codigo_equipo}")

        computadora_id = comp["id"]

        conn = obtener_conexion()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT * FROM mantenimientos WHERE computadora_id = %s ORDER BY fecha DESC LIMIT 1", (computadora_id,))
            row = cur.fetchone()
            cur.close()
            return row
        finally:
            conn.close()
