from tkinter import *
from tkinter import messagebox
from db import conectar_db

def verificar_login(usuario, contrasena):
    db = conectar_db()
    if db is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
        return None
    try:
        cursor = db.cursor()
        cursor.execute("""
            SELECT idRol FROM Usuarios 
            WHERE (Correo=%s OR Nombre=%s) AND Contraseña=%s
        """, (usuario, usuario, contrasena))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else None
    except Exception as e:
        messagebox.showerror("Error", f"Error al verificar el login:\n{e}")
        return None
    finally:
        db.close()


def abrir_login(callback_por_rol):
    ventana = Tk()
    ventana.title("Login - VitalApp")
    ventana.geometry("300x220")
    ventana.resizable(False, False)

    Label(ventana, text="Correo o Nombre de Usuario:").pack(pady=5)
    entrada_usuario = Entry(ventana)
    entrada_usuario.pack()

    Label(ventana, text="Contraseña:").pack(pady=5)
    entrada_contra = Entry(ventana, show="*")
    entrada_contra.pack()

    def login():
        usuario = entrada_usuario.get()
        contra = entrada_contra.get()
        rol = verificar_login(usuario, contra)
        if rol:
            ventana.destroy()
            callback_por_rol(rol)
        else:
            messagebox.showerror("Error", "Correo o nombre de usuario y/o contraseña incorrectos.")

    Button(ventana, text="Iniciar Sesión", command=login).pack(pady=15)
    ventana.mainloop()
