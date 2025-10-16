import tkinter as tk
from tkinter import messagebox
from tecnico import Tecnico

class TecnicoWindow:
    def __init__(self, master, user, main_menu_callback):
        self.master = master
        self.user = user
        self.main_menu_callback = main_menu_callback

        master.title('TechNodes - Técnico')
        master.geometry('1200x600')
        master.configure(bg="#2c3e50")  # Fondo azul oscuro

        # ======= Estilos =======
        boton_estilo = {"bg": "yellow", "fg": "black", "font": ("Arial", 10, "bold"), "relief": "raised"}
        label_estilo = {"bg": "#2c3e50", "fg": "white", "font": ("Arial", 10)}

        # Botón volver al menú
        tk.Button(master, text='Volver al menú', command=self.volver_menu,
                  bg="red", fg="white", font=("Arial", 10, "bold")).pack(pady=5)

        # Marco superior con nombre del técnico
        frame_top = tk.LabelFrame(master, text=f'Técnico: {user.get("nombre")} (ID: {user.get("id")})',
                                  bg="#2c3e50", fg="white", font=("Arial", 10, "bold"))
        frame_top.pack(fill='x', padx=8, pady=8)

        tk.Button(frame_top, text='Cargar mis tickets', command=self.cargar_tickets, **boton_estilo).pack(side='left', padx=6, pady=4)

        # Tabla de tickets
        cols = ('id','alumno_nombre','computadora_id','descripcion','estado')
        self.tree_tec = tk.ttk.Treeview(master, columns=cols, show='headings', height=14)
        for c in cols:
            self.tree_tec.heading(c, text=c)
            self.tree_tec.column(c, anchor="center")
        self.tree_tec.pack(fill='both', expand=True, padx=8, pady=8)

        # Marco de acciones
        frame_actions = tk.Frame(master, bg="#2c3e50")
        frame_actions.pack(fill='x', padx=8, pady=8)

        tk.Label(frame_actions, text='Ticket ID:', **label_estilo).grid(row=0, column=0, padx=4, pady=4, sticky="e")
        self.tec_ticket_id = tk.Entry(frame_actions)
        self.tec_ticket_id.grid(row=0, column=1, padx=4, pady=4)

        tk.Label(frame_actions, text='Estado:', **label_estilo).grid(row=0, column=2, padx=4, pady=4, sticky="e")
        self.tec_estado = tk.ttk.Combobox(frame_actions, values=['en_proceso','completado'])
        self.tec_estado.grid(row=0, column=3, padx=4, pady=4)

        tk.Button(frame_actions, text='Actualizar estado',
                  command=self.actualizar_estado_ticket, **boton_estilo).grid(row=0, column=4, padx=6)

    def volver_menu(self):
        self.master.destroy()
        self.main_menu_callback()

    def cargar_tickets(self):
        for r in self.tree_tec.get_children():
            self.tree_tec.delete(r)
        rows = Tecnico.listar_tickets_asignados(self.user.get('id'))
        for rr in rows:
            self.tree_tec.insert('', 'end', values=(
                rr['id'],
                rr.get('alumno_nombre'),
                rr.get('computadora_id'),
                (rr.get('descripcion') or '')[:120],
                rr.get('estado')
            ))

    def actualizar_estado_ticket(self):
        tid = self.tec_ticket_id.get().strip()
        estado = self.tec_estado.get().strip()
        if not (tid and estado):
            messagebox.showwarning('Error','Proporciona ticket ID y estado.')
            return
        try:
            Tecnico.actualizar_estado(int(tid), estado)
            messagebox.showinfo('OK','Estado actualizado.')
            self.cargar_tickets()
        except Exception as e:
            messagebox.showerror('Error', str(e))
