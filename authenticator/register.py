from tkinter import *
from tkinter import messagebox
from db import conectar_db

def abrir_registro():
    ventana = Tk()
    ventana.title("Registro de Paciente - VitalApp")
    ventana.geometry("400x600")

    # CAMPOS DEL FORMULARIO
    Label(ventana, text="Nombre Completo:").pack(pady=5)
    entrada_nombre = Entry(ventana)
    entrada_nombre.pack()

    Label(ventana, text="Correo:").pack(pady=5)
    entrada_correo = Entry(ventana)
    entrada_correo.pack()

    Label(ventana, text="Contraseña:").pack(pady=5)
    entrada_contra = Entry(ventana, show="*")
    entrada_contra.pack()

    Label(ventana, text="Fecha de Nacimiento (YYYY-MM-DD):").pack(pady=5)
    entrada_fecha = Entry(ventana)
    entrada_fecha.pack()

    Label(ventana, text="Genero:").pack(pady=5)
    entrada_genero = Entry(ventana)
    entrada_genero.pack()

    Label(ventana, text="Telefono:").pack(pady=5)
    entrada_telefono = Entry(ventana)
    entrada_telefono.pack()

    Label(ventana, text="Direccion:").pack(pady=5)
    entrada_direccion = Entry(ventana)
    entrada_direccion.pack()

    def registrar():
        nombre = entrada_nombre.get()
        correo = entrada_correo.get()
        contrasena = entrada_contra.get()
        fecha = entrada_fecha.get()
        genero = entrada_genero.get()
        telefono = entrada_telefono.get()
        direccion = entrada_direccion.get()

        if not (nombre and correo and contrasena and fecha and genero and telefono and direccion):
            messagebox.showwarning("Campos Vacios", "Por favor completa todos los campos.")
            return

        try:
            db = conectar_db()
            cursor = db.cursor()

            # 1. Insertar en tabla Usuarios
            cursor.execute("""
                INSERT INTO Usuarios (Nombre, Correo, Contraseña, idRol) 
                VALUES (%s, %s, %s, %s)
            """, (nombre, correo, contrasena, 3))  # idRol = 3 (paciente)
            id_usuario = cursor.lastrowid

            # 2. Insertar en tabla Pacientes
            cursor.execute("""
                INSERT INTO Pacientes 
                (idUsuario, Nombre_Paciente, Fecha_nacimiento, Genero, Telefono, Direccion, Correo)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (id_usuario, nombre, fecha, genero, telefono, direccion, correo))

            db.commit()
            db.close()

            messagebox.showinfo("Éxito", "Paciente registrado correctamente.")
            ventana.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar paciente: {e}")

    Button(ventana, text="Registrarse", command=registrar).pack(pady=20)
    ventana.mainloop()

