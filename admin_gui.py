import tkinter as tk
from tkinter import ttk, messagebox
from administrador import Administrador
from computadora import Computadora
from database import obtener_conexion

class AdminWindow:
    def __init__(self, master, user, volver_callback):
        self.master = master
        self.user = user
        self.volver_callback = volver_callback

        master.title('TechNodes - Administrador')
        master.geometry('1300x650')

        # ===== Estilos =====
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", font=('Arial', 11, 'bold'), background="#004080", foreground="white")
        style.configure("Treeview", font=('Arial', 10), rowheight=24)
        style.map("Treeview", background=[("selected", "#66a3ff")])

        # Estilo personalizado para botones amarillos
        style.configure("Yellow.TButton",
                        background="#FFD700",
                        foreground="black",
                        font=('Arial', 10, 'bold'),
                        padding=6)
        style.map("Yellow.TButton",
                  background=[("active", "#FFC300")])

        # ===== Layout principal =====
        main_frame = tk.Frame(master, bg="#E6F0FF")
        main_frame.pack(fill="both", expand=True)

        # ==== Panel izquierdo (tablas) ====
        left_frame = tk.Frame(main_frame, bg="#E6F0FF")
        left_frame.pack(side="left", fill="both", expand=True, padx=8, pady=8)

        # Tickets pendientes
        frame_top = ttk.LabelFrame(left_frame, text='📌 Tickets pendientes por asignar', padding=6)
        frame_top.pack(fill='both', expand=True, pady=5)

        cols_pend = ('id','alumno_nombre','computadora_id','descripcion','estado','tecnico_id')
        self.tree_tickets_pend = ttk.Treeview(frame_top, columns=cols_pend, show='headings', height=8)
        for c in cols_pend:
            self.tree_tickets_pend.heading(c, text=c.capitalize())
            self.tree_tickets_pend.column(c, width=150, anchor="center")
        self.tree_tickets_pend.pack(side='left', fill='both', expand=True)
        vsb1 = ttk.Scrollbar(frame_top, orient='vertical', command=self.tree_tickets_pend.yview)
        self.tree_tickets_pend.configure(yscroll=vsb1.set)
        vsb1.pack(side='right', fill='y')

        # Todos los tickets
        frame_all = ttk.LabelFrame(left_frame, text='📊 Estado de todos los tickets', padding=6)
        frame_all.pack(fill='both', expand=True, pady=5)

        cols_all = ('id','alumno_nombre','codigo_equipo','descripcion','tecnico_nombre','estado')
        self.tree_tickets_all = ttk.Treeview(frame_all, columns=cols_all, show='headings', height=8)
        for c in cols_all:
            self.tree_tickets_all.heading(c, text=c.capitalize())
            self.tree_tickets_all.column(c, width=160, anchor="center")
        self.tree_tickets_all.pack(side='left', fill='both', expand=True)
        vsb2 = ttk.Scrollbar(frame_all, orient='vertical', command=self.tree_tickets_all.yview)
        self.tree_tickets_all.configure(yscroll=vsb2.set)
        vsb2.pack(side='right', fill='y')

        # ==== Panel derecho (botones) ====
        right_frame = tk.Frame(main_frame, bg="#E6F0FF")
        right_frame.pack(side="right", fill="y", padx=8, pady=8)

        ttk.Button(right_frame, text='🔄 Refrescar', style="Yellow.TButton", command=self.refrescar_tablas, width=25).pack(pady=10)
        ttk.Button(right_frame, text='📈 Estadísticas', style="Yellow.TButton", command=self.abrir_estadisticas, width=25).pack(pady=10)
        ttk.Button(right_frame, text='✏️ Asignar Ticket', style="Yellow.TButton", command=self.abrir_asignar_ticket, width=25).pack(pady=10)
        ttk.Button(right_frame, text='⚙️ Gestión', style="Yellow.TButton", command=self.abrir_gestion, width=25).pack(pady=10)
        ttk.Button(right_frame, text='⬅️ Volver al menú', style="Yellow.TButton", command=self.volver_callback, width=25).pack(pady=30)

        # Cargar datos iniciales
        self.refrescar_tablas()

    def refrescar_tablas(self):
        self.cargar_tickets_pendientes()
        self.cargar_todos_tickets()

    def cargar_tickets_pendientes(self):
        for r in self.tree_tickets_pend.get_children():
            self.tree_tickets_pend.delete(r)
        rows = Administrador.listar_tickets_pendientes()
        for rr in rows:
            self.tree_tickets_pend.insert('', 'end', values=(
                rr['id'], rr.get('alumno_nombre'), rr.get('computadora_id'),
                (rr.get('descripcion') or '')[:80], rr.get('estado'), rr.get('tecnico_id')
            ))

    def cargar_todos_tickets(self):
        for r in self.tree_tickets_all.get_children():
            self.tree_tickets_all.delete(r)
        rows = Administrador.listar_todos_los_tickets()
        for rr in rows:
            self.tree_tickets_all.insert('', 'end', values=(
                rr['id'], rr.get('alumno_nombre'), rr.get('codigo_equipo'),
                (rr.get('descripcion') or '')[:80], rr.get('tecnico_nombre'), rr.get('estado')
            ))

    def abrir_asignar_ticket(self):
        AsignarTicketWindow(self)

    def abrir_gestion(self):
        GestionWindow(self)

    def abrir_estadisticas(self):
        EstadisticasWindow(self)

class AsignarTicketWindow:
    def __init__(self, parent):
        self.parent = parent
        win = tk.Toplevel(parent.master)
        win.title("Asignar Ticket")
        win.geometry("350x350")
        win.configure(bg="#E6F0FF")
        win.transient(parent.master)
        win.grab_set()

        ttk.Label(win, text="Ticket ID:").pack(pady=5)
        self.entry_tid = ttk.Entry(win); self.entry_tid.pack(pady=5)
        ttk.Label(win, text="Técnico ID:").pack(pady=5)
        self.entry_tecid = ttk.Entry(win); self.entry_tecid.pack(pady=5)

        ttk.Button(win, text="Asignar", style="Yellow.TButton", command=self.asignar).pack(pady=10)

    def asignar(self):
        tid = self.entry_tid.get().strip()
        tec = self.entry_tecid.get().strip()
        if not (tid and tec):
            messagebox.showwarning("Datos incompletos", "Proporciona Ticket ID y Técnico ID.")
            return
        try:
            Administrador.asignar_ticket(int(tid), int(tec))
            messagebox.showinfo("Asignado", "Ticket asignado correctamente.")
            self.parent.refrescar_tablas()
        except Exception as e:
            messagebox.showerror("Error", str(e))


class GestionWindow:
    def __init__(self, parent):
        self.parent = parent
        win = tk.Toplevel(parent.master)
        win.title("Gestión de Computadoras y Técnicos")
        win.geometry("1200x300")
        win.configure(bg="#E6F0FF")
        win.transient(parent.master)
        win.grab_set()

        frame_gest = ttk.LabelFrame(win, text='⚙️ Gestión - Computadoras / Técnicos', padding=6)
        frame_gest.pack(fill='both', expand=True, padx=8, pady=8)

        # Computadoras
        ttk.Label(frame_gest, text='Código comp:').grid(row=0, column=0)
        self.g_codigo = ttk.Entry(frame_gest); self.g_codigo.grid(row=0, column=1)
        ttk.Label(frame_gest, text='Ubicación:').grid(row=0, column=2)
        self.g_ubic = ttk.Entry(frame_gest); self.g_ubic.grid(row=0, column=3)
        ttk.Button(frame_gest, text='Agregar/Actualizar comp', style="Yellow.TButton", command=self.agregar_computadora).grid(row=0, column=4, padx=6)
        ttk.Button(frame_gest, text='Eliminar comp', style="Yellow.TButton", command=self.eliminar_computadora).grid(row=0, column=5, padx=6)

        # Técnicos
        ttk.Label(frame_gest, text='Nombre técnico:').grid(row=1, column=0)
        self.g_tec_nombre = ttk.Entry(frame_gest); self.g_tec_nombre.grid(row=1, column=1)
        ttk.Label(frame_gest, text='Usuario técnico:').grid(row=1, column=2)
        self.g_tec_user = ttk.Entry(frame_gest); self.g_tec_user.grid(row=1, column=3)
        ttk.Label(frame_gest, text='Contraseña:').grid(row=1, column=4)
        self.g_tec_pass = ttk.Entry(frame_gest, show='*'); self.g_tec_pass.grid(row=1, column=5)
        ttk.Label(frame_gest, text='Especialidad:').grid(row=1, column=6)
        self.g_tec_esp = ttk.Combobox(frame_gest, values=['redes','hardware','software']); self.g_tec_esp.grid(row=1, column=7)
        ttk.Button(frame_gest, text='Agregar técnico', style="Yellow.TButton", command=self.agregar_tecnico).grid(row=1, column=8, padx=6)

        ttk.Label(frame_gest, text='Técnico ID a eliminar:').grid(row=2, column=0)
        self.g_tec_del = ttk.Entry(frame_gest); self.g_tec_del.grid(row=2, column=1)
        ttk.Button(frame_gest, text='Eliminar técnico', style="Yellow.TButton", command=self.eliminar_tecnico).grid(row=2, column=2, padx=6)

    def agregar_computadora(self):
        codigo = self.g_codigo.get().strip()
        ubic = self.g_ubic.get().strip() or None
        if not codigo:
            messagebox.showwarning('Error','Ingresa código de computadora.')
            return
        try:
            comp = Computadora(codigo=codigo, ubicacion=ubic)
            comp.guardar()
            messagebox.showinfo('OK','Computadora agregada/actualizada.')
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def eliminar_computadora(self):
        codigo = self.g_codigo.get().strip()
        if not codigo:
            messagebox.showwarning('Error','Ingresa código a eliminar.')
            return
        try:
            Computadora.eliminar(codigo)
            messagebox.showinfo('OK','Computadora eliminada.')
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def agregar_tecnico(self):
        nombre = self.g_tec_nombre.get().strip()
        user = self.g_tec_user.get().strip()
        pwd = self.g_tec_pass.get().strip()
        esp = self.g_tec_esp.get().strip()
        if not (nombre and user and pwd and esp):
            messagebox.showwarning('Error','Proporciona todos los datos del técnico.')
            return
        try:
            Administrador.agregar_tecnico(nombre, user, pwd, esp)
            messagebox.showinfo('OK','Técnico agregado.')
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def eliminar_tecnico(self):
        tid = self.g_tec_del.get().strip()
        if not tid:
            messagebox.showwarning('Error','Ingresa ID de técnico a eliminar.')
            return
        try:
            Administrador.eliminar_tecnico_por_id(int(tid))
            messagebox.showinfo('OK','Técnico eliminado.')
        except Exception as e:
            messagebox.showerror('Error', str(e))


class EstadisticasWindow:
    def __init__(self, parent):
        self.parent = parent
        self.win = tk.Toplevel(parent.master)
        self.win.title('Estadísticas de Tickets')
        self.win.geometry('900x600')
        self.win.configure(bg='#2c3e50')
        self.win.transient(parent.master)
        self.win.grab_set()

        tk.Label(self.win, text='📊 Estadísticas de Tickets (cantidad por fecha)', font=('Arial', 14, 'bold'),
                 bg='#2c3e50', fg='white').pack(pady=10)

        # frame para grafico
        frame_grafico = tk.Frame(self.win, bg='#2c3e50')
        frame_grafico.pack(fill='both', expand=True, padx=12, pady=8)

        # importar matplotlib aquí para no cargarlo si no se usa
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        import numpy as np
        from collections import Counter
        from datetime import datetime

        self.figura, self.ax = plt.subplots(figsize=(9,4))
        self.figura.patch.set_facecolor('#ecf0f1')
        self.canvas = FigureCanvasTkAgg(self.figura, master=frame_grafico)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

        btn_frame = tk.Frame(self.win, bg='#2c3e50')
        btn_frame.pack(pady=8)
        ttk.Button(btn_frame, text='Actualizar Gráfico', style='Yellow.TButton', command=self.cargar_datos).pack(padx=6, pady=6)

        self.cargar_datos()

    def cargar_datos(self):
        # obtener fechas de creado_en de tickets
        conn = None
        try:
            conn = obtener_conexion()
            cur = conn.cursor()
            cur.execute("SELECT creado_en FROM tickets")
            filas = cur.fetchall()
            cur.close()
        finally:
            if conn:
                conn.close()

        # contar por fecha (solo fecha, sin hora)
        from collections import Counter
        from datetime import datetime
        contador = Counter()
        for (fecha_val,) in filas:
            if fecha_val is None:
                continue
            if isinstance(fecha_val, str):
                # intentar parsear
                try:
                    dt = datetime.strptime(fecha_val, '%Y-%m-%d %H:%M:%S')
                except Exception:
                    try:
                        dt = datetime.strptime(fecha_val, '%Y-%m-%d')
                    except Exception:
                        continue
            else:
                dt = fecha_val  # ya es datetime
            fecha = dt.date()
            contador[fecha] += 1

        self.ax.clear()
        if not contador:
            self.ax.set_title('No hay datos para mostrar')
            self.canvas.draw()
            return

        fechas_ordenadas = sorted(contador.items())
        fechas_x = [f for f, _ in fechas_ordenadas]
        valores_y = [c for _, c in fechas_ordenadas]

        # plot scatter
        fechas_ordinales = [d.toordinal() for d in fechas_x]
        # scatter: not specifying colors (matplotlib default will be used)
        self.ax.scatter(fechas_x, valores_y, alpha=0.7, label='Tickets')

        # linea de tendencia (polyfit sobre ordinales)
        coef = np.polyfit(fechas_ordinales, valores_y, 1)
        poly = np.poly1d(coef)
        tendencia_y = poly(fechas_ordinales)
        # plot trend line
        self.ax.plot(fechas_x, tendencia_y, linestyle='--', linewidth=2, label='Tendencia')

        self.ax.set_title('Tickets por fecha')
        self.ax.set_xlabel('Fecha')
        self.ax.set_ylabel('Cantidad de tickets')
        self.ax.legend()
        self.figura.autofmt_xdate()
        self.canvas.draw()
