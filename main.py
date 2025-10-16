import tkinter as tk
from database import crear_tablas_si_no_existen
from login import LoginWindow
from alumno_gui import AlumnoWindow
from admin_gui import AdminWindow
from tecnico_gui import TecnicoWindow


def abrir_ventana_alumno(root):
    root.withdraw()
    win = tk.Toplevel(root)
    AlumnoWindow(win, lambda: volver_al_menu(root, win))


def abrir_login(root, rol):
    root.withdraw()
    login_win = tk.Toplevel(root)  # Ventana de login

    def on_success(user):
        if user.get('tipo_usuario') == 'administrador':
            win = tk.Toplevel(root)
            AdminWindow(win, user, lambda: volver_al_menu(root, win))
        elif user.get('tipo_usuario') == 'tecnico':
            win = tk.Toplevel(root)
            TecnicoWindow(win, user, lambda: volver_al_menu(root, win))

    # Pasamos la ventana de login real al callback
    LoginWindow(
        login_win,
        on_success,
        rol_fijo=rol,
        volver_callback=lambda: volver_al_menu(root, login_win)
    )


def volver_al_menu(root, ventana_actual):
    ventana_actual.destroy()
    root.deiconify()


def main():
    try:
        crear_tablas_si_no_existen()
    except Exception as e:
        print('No se pudo preparar la base de datos:', e)
        return

    root = tk.Tk()
    root.title('TECHNODES - Menú')
    root.geometry('350x250')
    root.configure(bg="#2c3e50")  # Fondo azul oscuro

    frm = tk.Frame(root, padx=10, pady=10, bg="#2c3e50")
    frm.pack(fill='both', expand=True)

    tk.Label(frm, text='TECHNODES - SELECCIONA TU OPCIÓN',
             bg="#2c3e50", fg="white", font=("Arial", 12, "bold")).pack(pady=10)

    boton_estilo = {"bg": "yellow", "fg": "black", "font": ("Arial", 10, "bold"), "relief": "raised"}

    tk.Button(frm, text='ALUMNO',
              command=lambda: abrir_ventana_alumno(root), **boton_estilo).pack(fill='x', pady=5)

    tk.Button(frm, text='ADMINISTRADOR',
              command=lambda: abrir_login(root, 'administrador'), **boton_estilo).pack(fill='x', pady=5)

    tk.Button(frm, text='TECNICO',
              command=lambda: abrir_login(root, 'tecnico'), **boton_estilo).pack(fill='x', pady=5)

    tk.Button(frm, text='SALIR',
              command=root.destroy, bg="red", fg="white", font=("Arial", 10, "bold")).pack(pady=10)

    root.mainloop()


if __name__ == '__main__':
    main()
