import customtkinter as ctk
import hashlib
from tkinter import messagebox
from db import conectar_db

# Función para verificar login
def verificar_login(usuario, contrasena):
    db = conectar_db()
    if db is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
        return None
    try:
        # Convertimos la contraseña ingresada a SHA-256
        input_hash = hashlib.sha256(contrasena.encode()).hexdigest()
        
        cursor = db.cursor()
        # IMPORTANTE: Ahora comparamos u.Contraseña contra input_hash
        cursor.execute("""
            SELECT u.idUsuario, u.idRol FROM Usuarios u
            WHERE (u.Correo=%s OR u.Nombre=%s) AND u.Contraseña=%s
        """, (usuario, usuario, input_hash))
        
        resultado = cursor.fetchone()
        if resultado:
            id_usuario, id_rol = resultado
            return {'rol': id_rol, 'id_usuario': id_usuario}
        else:
            return None
    except Exception as e:
        messagebox.showerror("Error", f"Error al verificar el login:\n{e}")
        return None
    finally:
        db.close()

# Función para abrir la ventana de login
def abrir_login(callback_por_rol):
    ctk.set_appearance_mode("Light")  # Opciones: "System", "Light", "Dark"
    ctk.set_default_color_theme("blue")  # También "dark-blue", "green", etc.

    ventana = ctk.CTk()
    ventana.title("Login - VitalApp")
    ventana.geometry("400x350")
    ventana.resizable(False, False)

    # Frame principal
    frame = ctk.CTkFrame(master=ventana)
    frame.pack(pady=30, padx=30, fill="both", expand=True)

    # Título
    label_titulo = ctk.CTkLabel(frame, text="Iniciar Sesión", font=("Helvetica", 24, "bold"))
    label_titulo.pack(pady=20)

    # Entrada de usuario
    entrada_usuario = ctk.CTkEntry(frame, placeholder_text="Correo o Nombre de Usuario")
    entrada_usuario.pack(pady=10, fill="x")

    # Entrada de contraseña
    entrada_contra = ctk.CTkEntry(frame, placeholder_text="Contraseña", show="*")
    entrada_contra.pack(pady=10, fill="x")

    # Función de login
    def login():
        usuario = entrada_usuario.get()
        contra = entrada_contra.get()
        datos_usuario = verificar_login(usuario, contra)
        if datos_usuario:
            ventana.destroy()
            callback_por_rol(datos_usuario['rol'], datos_usuario['id_usuario'])
        else:
            # Mensaje más profesional para seguridad
            messagebox.showerror("Error", "Credenciales incorrectas.")

    # Botón de login
    boton_login = ctk.CTkButton(frame, text="Iniciar Sesión", command=login)
    boton_login.pack(pady=20)

    ventana.mainloop()
