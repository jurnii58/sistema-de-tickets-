import tkinter as tk
from tkinter import ttk, messagebox
from alumno import Alumno

class AlumnoWindow:
    def __init__(self, master, main_menu_callback):
        self.master = master
        self.main_menu_callback = main_menu_callback

        master.title('TechNodes - Alumno')
        master.geometry('900x600')
        master.configure(bg="#2c3e50")  # Fondo azul oscuro

        # ======= Estilos =======
        boton_estilo = {"bg": "yellow", "fg": "black", "font": ("Arial", 10, "bold"), "relief": "raised"}
        label_estilo = {"bg": "#2c3e50", "fg": "white", "font": ("Arial", 10)}

        # Botón volver al menú
        tk.Button(master, text='Volver al menú', command=self.volver_menu,
                  bg="red", fg="white", font=("Arial", 10, "bold")).pack(pady=5)

        # Frame superior
        frame_top = tk.LabelFrame(master, text='Levantar ticket / Ver computadoras',
                                  bg="#2c3e50", fg="white", font=("Arial", 10, "bold"))
        frame_top.pack(side='top', fill='x', padx=8, pady=8)

        # Formulario
        tk.Label(frame_top, text='Nombre:', **label_estilo).grid(row=0, column=0, sticky='w')
        self.al_nombre = tk.Entry(frame_top); self.al_nombre.grid(row=0, column=1)
        tk.Label(frame_top, text='Edad:', **label_estilo).grid(row=0, column=2, sticky='w')
        self.al_edad = tk.Entry(frame_top); self.al_edad.grid(row=0, column=3)
        tk.Label(frame_top, text='Carrera:', **label_estilo).grid(row=1, column=0, sticky='w')
        self.al_carrera = tk.Entry(frame_top); self.al_carrera.grid(row=1, column=1)
        tk.Label(frame_top, text='Matrícula:', **label_estilo).grid(row=1, column=2, sticky='w')
        self.al_matricula = tk.Entry(frame_top); self.al_matricula.grid(row=1, column=3)
        tk.Label(frame_top, text='Código equipo:', **label_estilo).grid(row=2, column=0, sticky='w')
        self.al_codigo = tk.Entry(frame_top); self.al_codigo.grid(row=2, column=1)
        tk.Label(frame_top, text='Descripción:', **label_estilo).grid(row=3, column=0, sticky='nw')
        self.al_desc = tk.Text(frame_top, height=4, width=60); self.al_desc.grid(row=3, column=1, columnspan=3)
        tk.Button(frame_top, text='Levantar ticket', command=self.levantar_ticket, **boton_estilo).grid(row=4, column=1, pady=6)

        # Lista de computadoras
        frame_list = tk.LabelFrame(master, text='Computadoras',
                                   bg="#2c3e50", fg="white", font=("Arial", 10, "bold"))
        frame_list.pack(fill='both', expand=True, padx=8, pady=8)

        cols = ('codigo','ubicacion','estado','ultimo_mantenimiento')
        self.tree_comp = ttk.Treeview(frame_list, columns=cols, show='headings')
        for c in cols:
            self.tree_comp.heading(c, text=c)
        vsb = ttk.Scrollbar(frame_list, orient='vertical', command=self.tree_comp.yview)
        self.tree_comp.configure(yscroll=vsb.set)
        self.tree_comp.pack(side='left', fill='both', expand=True)
        vsb.pack(side='right', fill='y')

        tk.Button(master, text='Refrescar lista', command=self.cargar_computadoras, **boton_estilo).pack(pady=6)

        # Historial
        frame_hist = tk.LabelFrame(master, text='Historial de último mantenimiento (por código)',
                                   bg="#2c3e50", fg="white", font=("Arial", 10, "bold"))
        frame_hist.pack(fill='x', padx=8, pady=8)

        self.hist_codigo = tk.Entry(frame_hist)
        self.hist_codigo.grid(row=0, column=0, padx=4, pady=4)
        tk.Button(frame_hist, text='Ver historial', command=self.ver_historial, **boton_estilo).grid(row=0, column=1, padx=6)
        self.lbl_hist = tk.Label(frame_hist, text='Último mantenimiento: -', **label_estilo)
        self.lbl_hist.grid(row=1, column=0, columnspan=2, sticky='w')

        self.cargar_computadoras()

    def volver_menu(self):
        self.master.destroy()
        self.main_menu_callback()

    def levantar_ticket(self):
        nombre = self.al_nombre.get().strip()
        edad = self.al_edad.get().strip() or None
        carrera = self.al_carrera.get().strip() or None
        matricula = self.al_matricula.get().strip() or None
        codigo = self.al_codigo.get().strip()
        descripcion = self.al_desc.get('1.0', 'end').strip()
        if not (nombre and codigo and descripcion):
            messagebox.showwarning('Datos incompletos','Proporciona nombre, código y descripción.')
            return
        try:
            tid = Alumno.levantar_ticket(nombre, edad, carrera, matricula, codigo, descripcion)
            messagebox.showinfo('Ticket creado', f'Ticket #{tid} creado.')
            # Limpiar campos
            self.al_nombre.delete(0,'end'); self.al_edad.delete(0,'end')
            self.al_carrera.delete(0,'end'); self.al_matricula.delete(0,'end')
            self.al_codigo.delete(0,'end'); self.al_desc.delete('1.0','end')
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def cargar_computadoras(self):
        for r in self.tree_comp.get_children():
            self.tree_comp.delete(r)
        rows = Alumno.listar_computadoras()
        for rr in rows:
            self.tree_comp.insert('', 'end', values=(
                rr['codigo'],
                rr.get('ubicacion'),
                rr.get('estado'),
                rr.get('ultimo_mantenimiento')
            ))

    def ver_historial(self):
        codigo = self.hist_codigo.get().strip()
        if not codigo:
            messagebox.showwarning('Error','Ingresa código de equipo.')
            return
        row = Alumno.obtener_ultimo_mantenimiento(codigo)
        if not row:
            self.lbl_hist.config(text='No hay historial para ese equipo.')
        else:
            self.lbl_hist.config(text=f"Fecha: {row.get('fecha')}\nDescripción: {row.get('descripcion')}")
