import customtkinter as ctk
from tkinter import messagebox
from db import conectar_db
ventana_actual = None  # Variable global para la ventana abierta actualmente

def abrir_nueva_ventana(func):
    global ventana_actual
    if ventana_actual is not None:
        ventana_actual.destroy()
    ventana_actual = func()

def volver_al_menu(ventana):
    global ventana_actual
    ventana.destroy()
    ventana_actual = None
    gestionar_usuarios(ventana_anterior=None)  # Aquí puedes pasar la ventana anterior si es necesario

def gestionar_usuarios(ventana_anterior):
    if ventana_anterior is not None:
        ventana_anterior.withdraw() # Oculta la ventana anterior

    ventana = ctk.CTkToplevel()
    ventana.title("Gestionar Usuarios")
    ventana.geometry("400x400")
    ventana.resizable(False, False)

    def regresar():
        print("Ventana anterior:", ventana_anterior)
        ventana.destroy()
        if ventana_anterior:
            ventana_anterior.deiconify()
        else:
            print("No hay ventana anterior para mostrar.")
        # Si hay una ventana abierta, la cerramos

    btn_regresar = ctk.CTkButton(ventana, text="Volver al menú", command=regresar)
    btn_regresar.pack(pady=5)

    #ctk.CTkButton(ventana, text="Volver al Menú", command=lambda: volver_al_menu(ventana)).pack(pady=5)


    label = ctk.CTkLabel(ventana, text="Gestión de Usuarios", font=("Helvetica", 20, "bold"))
    label.pack(pady=20)

    btn_doctores = ctk.CTkButton(ventana, text="Ver Doctores", command=lambda: abrir_nueva_ventana(mostrar_doctores))
    btn_doctores.pack(pady=10, fill="x", padx=40)

    btn_admins = ctk.CTkButton(ventana, text="Ver Administradores", command=lambda: abrir_nueva_ventana(mostrar_administradores))
    btn_admins.pack(pady=10, fill="x", padx=40)

    btn_pacientes = ctk.CTkButton(ventana, text="Ver Pacientes", command=lambda: abrir_nueva_ventana(mostrar_pacientes))
    btn_pacientes.pack(pady=10, fill="x", padx=40)

    btn_nuevo_admin = ctk.CTkButton(ventana, text="Agregar Administrador", command=lambda: abrir_nueva_ventana(crear_administrador))
    btn_nuevo_admin.pack(pady=10, fill="x", padx=40)

    btn_nuevo_medico = ctk.CTkButton(ventana, text="Agregar Médico", command=lambda: abrir_nueva_ventana(crear_medico))
    btn_nuevo_medico.pack(pady=10, fill="x", padx=40)

    global ventana_actual
    ventana_actual = ventana  # Actualiza la variable global con la nueva ventana
    return ventana

def crear_administrador():
    ventana = ctk.CTkToplevel()
    ventana.title("Nuevo Administrador")
    ventana.geometry("400x400")

    ctk.CTkButton(ventana, text="Volver al Menú", command=lambda: volver_al_menu(ventana)).pack(pady=10)

    ctk.CTkLabel(ventana, text="Nombre:").pack(pady=5)
    entrada_nombre = ctk.CTkEntry(ventana)
    entrada_nombre.pack(pady=5)

    ctk.CTkLabel(ventana, text="Correo:").pack(pady=5)
    entrada_correo = ctk.CTkEntry(ventana)
    entrada_correo.pack(pady=5)

    ctk.CTkLabel(ventana, text="Contraseña:").pack(pady=5)
    entrada_contra = ctk.CTkEntry(ventana, show="*")
    entrada_contra.pack(pady=5)

    def guardar_admin():
        nombre = entrada_nombre.get()
        correo = entrada_correo.get()
        contra = entrada_contra.get()

        try:
            db = conectar_db()
            cursor = db.cursor()
            cursor.execute("""
                INSERT INTO Usuarios (Nombre, Correo, Contraseña, idRol)
                VALUES (%s, %s, %s, 1)
            """, (nombre, correo, contra))
            db.commit()
            db.close()
            messagebox.showinfo("Éxito", "Administrador creado correctamente.")
            ventana.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear el administrador: {e}")

    ctk.CTkButton(ventana, text="Guardar", command=guardar_admin).pack(pady=20)

    global ventana_actual
    ventana_actual = ventana  # Actualiza la variable global con la nueva ventana
    return ventana

def crear_medico():
    ventana = ctk.CTkToplevel()
    ventana.title("Nuevo Médico")
    ventana.geometry("400x600")

    ctk.CTkButton(ventana, text="Volver al Menú", command=lambda: volver_al_menu(ventana)).pack(pady=5)

    ctk.CTkLabel(ventana, text="Nombre:").pack(pady=5)
    entrada_nombre = ctk.CTkEntry(ventana)
    entrada_nombre.pack(pady=5)

    ctk.CTkLabel(ventana, text="Correo:").pack(pady=5)
    entrada_correo = ctk.CTkEntry(ventana)
    entrada_correo.pack(pady=5)

    ctk.CTkLabel(ventana, text="Contraseña:").pack(pady=5)
    entrada_contra = ctk.CTkEntry(ventana, show="*")
    entrada_contra.pack(pady=5)

    ctk.CTkLabel(ventana, text="Teléfono:").pack(pady=5)
    entrada_telefono = ctk.CTkEntry(ventana)
    entrada_telefono.pack(pady=5)

    # Obtener especialidades
    try:
        db = conectar_db()
        cursor = db.cursor()
        cursor.execute("SELECT idEspecialidad, Nombre_Especialidad FROM Especialidad")
        especialidades = cursor.fetchall()
        db.close()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar especialidades: {e}")
        ventana.destroy()
        return

    if not especialidades:
        messagebox.showwarning("Advertencia", "No hay especialidades registradas.")
        ventana.destroy()
        return

    especialidades_dict = {nombre: id_ for id_, nombre in especialidades}
    nombres_especialidades = list(especialidades_dict.keys())

    especialidad_var = ctk.StringVar(value=nombres_especialidades[0])
    ctk.CTkLabel(ventana, text="Especialidad:").pack(pady=5)
    dropdown = ctk.CTkOptionMenu(ventana, variable=especialidad_var, values=nombres_especialidades)
    dropdown.pack(pady=5)


    def guardar_medico():
        nombre = entrada_nombre.get()
        correo = entrada_correo.get()
        contra = entrada_contra.get()
        telefono = entrada_telefono.get()
        especialidad_id = especialidades_dict[especialidad_var.get()]

        try:
            db = conectar_db()
            cursor = db.cursor()

            # Insertar en Usuarios
            cursor.execute("""
                INSERT INTO Usuarios (Nombre, Correo, Contraseña, idRol)
                VALUES (%s, %s, %s, 2)
            """, (nombre, correo, contra))

            id_usuario = cursor.lastrowid

            # Insertar en Médicos
            cursor.execute("""
                INSERT INTO Medicos (idEspecialidad, idUsuario, Nombre_medico, Telefono, Correo)
                VALUES (%s, %s, %s, %s, %s)
            """, (especialidad_id, id_usuario, nombre, telefono, correo))

            db.commit()
            db.close()
            messagebox.showinfo("Éxito", "Médico creado correctamente.")
            ventana.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear el médico: {e}")

    ctk.CTkButton(ventana, text="Guardar", command=guardar_medico).pack(pady=20)

    global ventana_actual
    ventana_actual = ventana  # Actualiza la variable global con la nueva ventana
    return ventana

def mostrar_doctores():
    ventana = ctk.CTkToplevel()
    ventana.title("Doctores Registrados")
    ventana.geometry("600x500")

    ctk.CTkButton(ventana, text="Volver al Menú", command=lambda: volver_al_menu(ventana)).pack(pady=5)


    try:
        db = conectar_db()
        cursor = db.cursor()
        cursor.execute("""
            SELECT u.Nombre, u.Correo, m.Telefono, e.Nombre_Especialidad
            FROM Usuarios u
            JOIN Medicos m ON u.idUsuario = m.idUsuario
            JOIN Especialidad e ON m.idEspecialidad = e.idEspecialidad
            WHERE u.idRol = 2
        """)
        doctores = cursor.fetchall()
        db.close()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron obtener los doctores: {e}")
        return

    for nombre, correo, telefono, especialidad in doctores:
        frame = ctk.CTkFrame(ventana)
        frame.pack(pady=8, padx=15, fill="x")

        label_info = ctk.CTkLabel(frame, text=f"{nombre} | {correo} | {telefono} | {especialidad}")
        label_info.pack(side="left", padx=5)

        boton_modificar = ctk.CTkButton(frame, text="Modificar", width=80, command=lambda c=correo, e=especialidad: modificar_individual_doctor(c, e))
        boton_modificar.pack(side="right", padx=5)


def modificar_individual_doctor(correo, especialidad):
    ventana = ctk.CTkToplevel()
    ventana.title("Modificar Doctor")
    ventana.geometry("400x400")

    ctk.CTkLabel(ventana, text=f"Correo actual: {correo}").pack(pady=10)

    ctk.CTkLabel(ventana, text="Nuevo Nombre:").pack()
    entrada_nombre = ctk.CTkEntry(ventana)
    entrada_nombre.pack(pady=5)

    ctk.CTkLabel(ventana, text="Nuevo Teléfono:").pack()
    entrada_telefono = ctk.CTkEntry(ventana)
    entrada_telefono.pack(pady=5)

    try:
        db = conectar_db()
        cursor = db.cursor()
        cursor.execute("SELECT idEspecialidad, Nombre_Especialidad FROM Especialidad")
        especialidades = cursor.fetchall()
        db.close()

        if especialidades:
            especialidades_dict = {nombre: id_ for id_, nombre in especialidades}
            nombres_especialidades = list(especialidades_dict.keys())

            especialidad_var = ctk.StringVar(value=nombres_especialidades[0])

            ctk.CTkLabel(ventana, text="Nueva Especialidad:").pack()
            dropdown = ctk.CTkOptionMenu(ventana, variable=especialidad_var, values=nombres_especialidades)
            dropdown.pack(pady=5)

        else:
            messagebox.showwarning("Sin datos", "No hay especialidades registradas.")
            ventana.destroy()
            return

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar las especialidades: {e}")
        return

    def guardar_cambios():
        nuevo_nombre = entrada_nombre.get()
        nuevo_telefono = entrada_telefono.get()
        nueva_especialidad = especialidad_var.get()

        try:
            db = conectar_db()
            cursor = db.cursor()
            cursor.execute("UPDATE Usuarios SET Nombre=%s WHERE Correo=%s", (nuevo_nombre, correo))
            cursor.execute("UPDATE Medicos SET Telefono=%s WHERE Correo=%s", (nuevo_telefono, correo))

            nueva_especialidad_id = especialidades_dict[nueva_especialidad]
            cursor.execute("UPDATE Medicos SET idEspecialidad=%s WHERE Correo=%s", (nueva_especialidad_id, correo))
            db.commit()
            db.close()
            messagebox.showinfo("Éxito", "Doctor actualizado correctamente.")
            ventana.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo modificar: {e}")

    ctk.CTkButton(ventana, text="Guardar cambios", command=guardar_cambios).pack(pady=20)

    global ventana_actual
    ventana_actual = ventana  # Actualiza la variable global con la nueva ventana
    return ventana

def mostrar_administradores():
    ventana_validacion = ctk.CTkToplevel()
    ventana_validacion.title("Validar Administrador")
    ventana_validacion.geometry("300x200")

    ctk.CTkButton(ventana_validacion, text="Volver al Menú", command=lambda: volver_al_menu(ventana_validacion)).pack(pady=5)


    ctk.CTkLabel(ventana_validacion, text="Ingresa contraseña de seguridad:").pack(pady=10)
    entrada_contra = ctk.CTkEntry(ventana_validacion, show="*")
    entrada_contra.pack(pady=10)

    def validar_y_abrir():
        if entrada_contra.get() != "MAYORADMIN":
            messagebox.showerror("Acceso denegado", "Contraseña incorrecta.")
            return
        ventana_validacion.destroy()
        ventana_lista = ctk.CTkToplevel()
        ventana_lista.title("Administradores")
        ventana_lista.geometry("500x400")

        try:
            db = conectar_db()
            cursor = db.cursor()
            cursor.execute("SELECT Nombre, Correo FROM Usuarios WHERE idRol=1")
            admins = cursor.fetchall()
            db.close()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron obtener los administradores: {e}")
            return

        for nombre, correo in admins:
            frame = ctk.CTkFrame(ventana_lista)
            frame.pack(pady=8, padx=15, fill="x")

            label_info = ctk.CTkLabel(frame, text=f"{nombre} | {correo}")
            label_info.pack(side="left", padx=5)

            boton_modificar = ctk.CTkButton(frame, text="Modificar", width=80, command=lambda c=correo: modificar_individual_admin(c))
            boton_modificar.pack(side="right", padx=5)

    ctk.CTkButton(ventana_validacion, text="Aceptar", command=validar_y_abrir).pack(pady=15)


def modificar_individual_admin(correo):
    ventana = ctk.CTkToplevel()
    ventana.title("Modificar Administrador")
    ventana.geometry("400x300")

    ctk.CTkLabel(ventana, text=f"Correo actual: {correo}").pack(pady=10)

    ctk.CTkLabel(ventana, text="Nuevo Nombre:").pack()
    entrada_nombre = ctk.CTkEntry(ventana)
    entrada_nombre.pack(pady=5)

    ctk.CTkLabel(ventana, text="Nuevo Correo:").pack()
    entrada_correo = ctk.CTkEntry(ventana)
    entrada_correo.pack(pady=5)

    def guardar():
        nuevo_nombre = entrada_nombre.get()
        nuevo_correo = entrada_correo.get()
        try:
            db = conectar_db()
            cursor = db.cursor()
            cursor.execute("UPDATE Usuarios SET Nombre=%s, Correo=%s WHERE Correo=%s AND idRol=1", (nuevo_nombre, nuevo_correo, correo))
            db.commit()
            db.close()
            messagebox.showinfo("Éxito", "Administrador modificado correctamente.")
            ventana.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo modificar: {e}")

    ctk.CTkButton(ventana, text="Guardar cambios", command=guardar).pack(pady=20)

    global ventana_actual
    ventana_actual = ventana  # Actualiza la variable global con la nueva ventana
    return ventana

def mostrar_pacientes():
    ventana = ctk.CTkToplevel()
    ventana.title("Pacientes Registrados")
    ventana.geometry("600x500")
    ctk.CTkButton(ventana, text="Volver al Menú", command=lambda: volver_al_menu(ventana)).pack(pady=5)


    try:
        db = conectar_db()
        cursor = db.cursor()
        cursor.execute("""
            SELECT idPaciente, Nombre_Paciente, Correo, Telefono, Genero, Direccion
            FROM Pacientes
        """)
        pacientes = cursor.fetchall()
        db.close()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron obtener los pacientes: {e}")
        return

    for id_paciente, nombre, correo, telefono, genero, direccion in pacientes:
        frame = ctk.CTkFrame(ventana)
        frame.pack(pady=8, padx=15, fill="x")

        label_info = ctk.CTkLabel(frame, text=f"{nombre} | {correo} | {telefono} | {genero} | {direccion}")
        label_info.pack(side="left", padx=5)

        boton_modificar = ctk.CTkButton(frame, text="Modificar", width=80, command=lambda c=correo: modificar_individual_paciente(c))
        boton_modificar.pack(side="right", padx=5)


def modificar_individual_paciente(correo):
    ventana = ctk.CTkToplevel()
    ventana.title("Modificar Paciente")
    ventana.geometry("400x400")

    ctk.CTkLabel(ventana, text=f"Correo actual: {correo}").pack(pady=10)

    ctk.CTkLabel(ventana, text="Nuevo Nombre:").pack()
    entrada_nombre = ctk.CTkEntry(ventana)
    entrada_nombre.pack(pady=5)

    ctk.CTkLabel(ventana, text="Nuevo Teléfono:").pack()
    entrada_telefono = ctk.CTkEntry(ventana)
    entrada_telefono.pack(pady=5)

    ctk.CTkLabel(ventana, text="Nueva Dirección:").pack()
    entrada_direccion = ctk.CTkEntry(ventana)
    entrada_direccion.pack(pady=5)

    def guardar_cambios():
        nuevo_nombre = entrada_nombre.get()
        nuevo_telefono = entrada_telefono.get()
        nueva_direccion = entrada_direccion.get()

        try:
            db = conectar_db()
            cursor = db.cursor()
            cursor.execute("""
                UPDATE Pacientes 
                SET Nombre_Paciente=%s, Telefono=%s, Direccion=%s 
                WHERE Correo=%s
            """, (nuevo_nombre, nuevo_telefono, nueva_direccion, correo))
            db.commit()
            db.close()
            messagebox.showinfo("Éxito", "Paciente actualizado correctamente.")
            ventana.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo modificar: {e}")

    ctk.CTkButton(ventana, text="Guardar cambios", command=guardar_cambios).pack(pady=20)

    global ventana_actual
    ventana_actual = ventana  # Actualiza la variable global con la nueva ventana
    return ventana