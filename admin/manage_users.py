from tkinter import *
from tkinter import messagebox
from db import conectar_db


def gestionar_usuarios():
    ventana = Toplevel()
    ventana.title("Gestión de Usuarios")

    # Botón para crear un Doctor
    Button(ventana, text="Crear cuenta de Doctor", command=crear_usuario_doctor).pack(pady=10)

    # Botón para modificar Doctor
    Button(ventana, text="Modificar Doctor", command=modificar_usuario_doctor).pack(pady=10)

    # Botón para crear Administrador
    Button(ventana, text="Crear Administrador", command=crear_admin).pack(pady=10)

    # Botón para modificar Administrador
    Button(ventana, text="Modificar Administrador", command=modificar_admin).pack(pady=10)
    
    ventana.mainloop()


def crear_usuario_doctor():
    ventana = Toplevel()
    ventana.title("Crear usuario - Doctor")

    Label(ventana, text="Nombre:").pack()
    entrada_nombre = Entry(ventana)
    entrada_nombre.pack()

    Label(ventana, text="Correo:").pack()
    entrada_correo = Entry(ventana)
    entrada_correo.pack()

    Label(ventana, text="Contraseña:").pack()
    entrada_contra = Entry(ventana, show="*")
    entrada_contra.pack()

    Label(ventana, text="Telefono:").pack()
    entrada_telefono = Entry(ventana)
    entrada_telefono.pack()

    Label(ventana, text="Especialidad:").pack()
    especialidad_var = StringVar()
    especialidades_dict = {}

    try:
        db = conectar_db()
        cursor = db.cursor()
        cursor.execute("SELECT idEspecialidad, Nombre_Especialidad FROM Especialidad")
        especialidades = cursor.fetchall()
        db.close()

        if especialidades:
            # Crear diccionario: nombre → id
            especialidades_dict = {nombre: id_ for id_, nombre in especialidades}
            nombres_especialidades = list(especialidades_dict.keys())
            especialidad_var.set(nombres_especialidades[0])  # Valor por defecto

            OptionMenu(ventana, especialidad_var, *nombres_especialidades).pack()
        else:
            messagebox.showwarning("Sin datos", "No hay especialidades registradas.")
            ventana.destroy()
            return

    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar las especialidades: {e}")
        ventana.destroy()
        return

    def guardar():
        nombre = entrada_nombre.get()
        correo = entrada_correo.get()
        contrasena = entrada_contra.get()
        telefono = entrada_telefono.get()
        nombre_especialidad = especialidad_var.get()

        if not (nombre and correo and contrasena and telefono and nombre_especialidad):
            messagebox.showwarning("Campos Vacíos", "Por favor completa todos los campos.")
            return

        try:
            id_especialidad = especialidades_dict[nombre_especialidad]

            db = conectar_db()
            cursor = db.cursor()

            # Insertar en Usuarios
            cursor.execute("""
                INSERT INTO Usuarios (Nombre, Correo, Contraseña, idRol) 
                VALUES (%s, %s, %s, %s)
            """, (nombre, correo, contrasena, 2))
            id_usuario = cursor.lastrowid

            # Insertar en Medicos
            cursor.execute("""
                INSERT INTO Medicos (idEspecialidad, idUsuario, Nombre_medico, Telefono, Correo)
                VALUES (%s, %s, %s, %s, %s)
            """, (id_especialidad, id_usuario, nombre, telefono, correo))

            db.commit()
            db.close()

            messagebox.showinfo("Éxito", "Doctor registrado correctamente.")
            ventana.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar al Doctor: {e}")

    Button(ventana, text="Registrar", command=guardar).pack(pady=20)
    ventana.mainloop()


def modificar_usuario_doctor():
    ventana = Toplevel()
    ventana.title("Modificar Doctor")

    Label(ventana, text="Correo del Doctor a modificar:").pack()
    entrada_correo_buscar = Entry(ventana)
    entrada_correo_buscar.pack()

    Label(ventana, text="Nuevo Nombre:").pack()
    entrada_nombre_nuevo = Entry(ventana)
    entrada_nombre_nuevo.pack()

    Label(ventana, text="Nueva Contraseña:").pack()
    entrada_contra_nueva = Entry(ventana, show="*")
    entrada_contra_nueva.pack()

    Label(ventana, text="Nuevo Teléfono:").pack()
    entrada_telefono_nuevo = Entry(ventana)
    entrada_telefono_nuevo.pack()

    Label(ventana, text="Nueva Especialidad:").pack()
    especialidad_var = StringVar()
    especialidades_dict = {}

    try:
        db = conectar_db()
        cursor = db.cursor()
        cursor.execute("SELECT idEspecialidad, Nombre_Especialidad FROM Especialidad")
        especialidades = cursor.fetchall()
        db.close()

        if especialidades:
            especialidades_dict = {nombre: id_ for id_, nombre in especialidades}
            nombres_especialidades = list(especialidades_dict.keys())
            especialidad_var.set(nombres_especialidades[0])  # Valor por defecto
            OptionMenu(ventana, especialidad_var, *nombres_especialidades).pack()
        else:
            messagebox.showwarning("Sin datos", "No hay especialidades registradas.")
            ventana.destroy()
            return

    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar las especialidades: {e}")
        ventana.destroy()
        return

    def modificar():
        correo = entrada_correo_buscar.get()
        nuevo_nombre = entrada_nombre_nuevo.get()
        nueva_contra = entrada_contra_nueva.get()
        nuevo_telefono = entrada_telefono_nuevo.get()
        nueva_especialidad = especialidad_var.get()

        if not (correo and nuevo_nombre and nueva_contra and nuevo_telefono and nueva_especialidad):
            messagebox.showwarning("Campos Vacíos", "Por favor completa todos los campos.")
            return

        try:
            id_especialidad = especialidades_dict[nueva_especialidad]

            db = conectar_db()
            cursor = db.cursor()

            # Actualizar los datos del usuario
            cursor.execute("""
                UPDATE Usuarios 
                SET Nombre=%s, Contraseña=%s 
                WHERE Correo=%s AND idRol=2
            """, (nuevo_nombre, nueva_contra, correo))

            # Buscar el id del medico con el correo proporcionado
            cursor.execute("""
                SELECT idMedico FROM Medicos 
                WHERE Correo=%s
            """, (correo,))
            medico = cursor.fetchone()

            if medico:
                id_medico = medico[0]
                cursor.execute("""
                    UPDATE Medicos 
                    SET idEspecialidad=%s, Nombre_medico=%s, Telefono=%s, Correo=%s 
                    WHERE idMedico=%s
                """, (id_especialidad, nuevo_nombre, nuevo_telefono, correo, id_medico))
                db.commit()
                db.close()
                messagebox.showinfo("Éxito", "Doctor modificado correctamente.")
                ventana.destroy()
            else:
                messagebox.showwarning("Error", "No se encontró un doctor con ese correo.")

        except Exception as e:
            messagebox.showerror("Error", f"Error al modificar al Doctor: {e}")

    Button(ventana, text="Modificar", command=modificar).pack(pady=20)
    ventana.mainloop()



def crear_admin():
    ventana = Toplevel()
    ventana.title("Crear Administrador")

    Label(ventana, text="Nombre:").pack()
    entrada_nombre = Entry(ventana)
    entrada_nombre.pack()

    Label(ventana, text="Correo:").pack()
    entrada_correo = Entry(ventana)
    entrada_correo.pack()

    Label(ventana, text="Contraseña:").pack()
    entrada_contra = Entry(ventana, show="*")
    entrada_contra.pack()

    def guardar():
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
                           (nombre, correo, contrasena, 1))  # 1 = Administrador
            db.commit()
            db.close()
            messagebox.showinfo("Éxito", "Administrador creado correctamente.")
            ventana.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar al Administrador: {e}")

    Button(ventana, text="Registrar", command=guardar).pack(pady=20)




def modificar_admin():
    ventana = Toplevel()
    ventana.title("Modificar Administrador")

    Label(ventana, text="Correo del Administrador a modificar:").pack()
    entrada_correo_buscar = Entry(ventana)
    entrada_correo_buscar.pack()

    Label(ventana, text="Nuevo Nombre:").pack()
    entrada_nombre_nuevo = Entry(ventana)
    entrada_nombre_nuevo.pack()

    Label(ventana, text="Nueva Contraseña:").pack()
    entrada_contra_nueva = Entry(ventana, show="*")
    entrada_contra_nueva.pack()

    def modificar():
        correo = entrada_correo_buscar.get()
        nuevo_nombre = entrada_nombre_nuevo.get()
        nueva_contra = entrada_contra_nueva.get()

        if not (correo and nuevo_nombre and nueva_contra):
            messagebox.showwarning("Campos Vacíos", "Por favor completa todos los campos.")
            return

        try:
            db = conectar_db()
            cursor = db.cursor()
            cursor.execute("UPDATE Usuarios SET Nombre=%s, Contraseña=%s WHERE Correo=%s AND idRol=1",
                           (nuevo_nombre, nueva_contra, correo))
            db.commit()
            db.close()
            messagebox.showinfo("Éxito", "Administrador modificado correctamente.")
            ventana.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error al modificar al Administrador: {e}")

    Button(ventana, text="Modificar", command=modificar).pack(pady=20)
