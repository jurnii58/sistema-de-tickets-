import tkinter as tk
from tkinter import ttk, messagebox
from database import obtener_conexion

class LoginWindow:
    def __init__(self, master, on_success, rol_fijo=None, volver_callback=None):
        self.master = master
        self.on_success = on_success
        self.rol_fijo = rol_fijo
        self.volver_callback = volver_callback

        master.title('TechNodes - Login')
        master.geometry('350x200')

        frm = ttk.Frame(master, padding=10)
        frm.pack(fill='both', expand=True)

        ttk.Label(frm, text='Usuario:').grid(row=0, column=0, sticky='w')
        self.ent_user = ttk.Entry(frm)
        self.ent_user.grid(row=0, column=1)

        ttk.Label(frm, text='Contraseña:').grid(row=1, column=0, sticky='w')
        self.ent_pass = ttk.Entry(frm, show='*')
        self.ent_pass.grid(row=1, column=1)

        if not rol_fijo:
            ttk.Label(frm, text='Rol:').grid(row=2, column=0, sticky='w')
            self.cmb_role = ttk.Combobox(frm, values=['administrador', 'tecnico'])
            self.cmb_role.grid(row=2, column=1)
        else:
            ttk.Label(frm, text=f'Rol: {rol_fijo}').grid(row=2, column=0, columnspan=2)

        ttk.Button(frm, text='Entrar', command=self.login).grid(row=3, column=0, columnspan=2, pady=8)

        if self.volver_callback:
            ttk.Button(frm, text='Volver al menú', command=self.volver).grid(row=4, column=0, columnspan=2, pady=4)

    def login(self):
        username = self.ent_user.get().strip()
        contraseña = self.ent_pass.get().strip()

        if self.rol_fijo:
            rol = self.rol_fijo
        else:
            rol = self.cmb_role.get().strip()

        if not (username and contraseña and rol):
            messagebox.showwarning('Datos incompletos', 'Proporciona usuario, contraseña y rol.')
            return

        conn = obtener_conexion()
        try:
            cur = conn.cursor(dictionary=True)
            if rol == 'administrador':
                cur.execute("SELECT * FROM administradores WHERE username=%s AND password=%s", (username, contraseña))
            else:
                cur.execute("SELECT * FROM tecnicos WHERE username=%s AND password=%s", (username, contraseña))
            user = cur.fetchone()
            cur.close()
        finally:
            conn.close()

        if not user:
            messagebox.showerror('Acceso denegado', 'Usuario o contraseña incorrectos.')
            return

        user['tipo_usuario'] = rol
        self.on_success(user)
        self.master.destroy()

    def volver(self):
        self.master.destroy()
        if self.volver_callback:
            self.volver_callback()
