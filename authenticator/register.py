from tkinter import *
from tkinter import messagebox
from db import conectar_db

def abrir_registro():
    ventana = Tk()
    ventana.title("Registro de Paciente - VitalApp")
    ventana.geometry("400x400")

    Label(ventana, text="Nombre Completo:").pack(pady=5)
    entrada_nombre = Entry(ventana)
    entrada_nombre.pack()

    Label(ventana, text="Correo:").pack(pady=5)
    entrada_correo = Entry(ventana)
    entrada_correo.pack()

    Label(ventana, text="Contraseña:").pack(pady=5)
    entrada_contra = Entry(ventana, show="*")
    entrada_contra.pack()

    def registrar():
        nombre = entrada_nombre.get()
        correo = entrada_correo.get()
        contrasena = entrada_contra.get()

        if not (nombre and correo and contrasena):
            messagebox.showwarning("Campos Vacíos", "Por favor completa todos los campos.")
            return

        try:
            db = conectar_db()
            cursor = db.cursor()
            cursor.execute("INSERT INTO Usuarios (Nombre, Correo, Contraseña, idRol) VALUES (%s, %s, %s, %s)",
                           (nombre, correo, contrasena, 3)) 
            db.commit()
            db.close()
            messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
            ventana.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar usuario: {e}")

    Button(ventana, text="Registrarse", command=registrar).pack(pady=20)
    ventana.mainloop()
