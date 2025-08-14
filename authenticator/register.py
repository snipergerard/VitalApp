import customtkinter as ctk
from tkcalendar import DateEntry
from tkinter import messagebox
from db import conectar_db

def abrir_registro():
    ctk.set_appearance_mode("light")  # o "dark"
    ctk.set_default_color_theme("blue")

    ventana = ctk.CTkToplevel()
    ventana.title("Registro de Paciente - VitalApp")
    ventana.geometry("500x700")
    ventana.resizable(False, False)

    scroll_frame = ctk.CTkScrollableFrame(ventana, width=480, height=680)
    scroll_frame.pack(padx=10, pady=10, fill="both", expand=True)

    ctk.CTkLabel(scroll_frame, text="Registro de Paciente", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=15)

    def crear_entrada(texto):
        ctk.CTkLabel(scroll_frame, text=texto).pack(pady=(10, 0))
        entrada = ctk.CTkEntry(scroll_frame, width=300)
        entrada.pack()
        return entrada

    entrada_nombre = crear_entrada("Nombre Completo:")
    entrada_correo = crear_entrada("Correo:")
    entrada_contra = crear_entrada("Contraseña:")
    entrada_contra.configure(show="*")

    ctk.CTkLabel(scroll_frame, text="Fecha de Nacimiento:").pack(pady=(10, 0))
    entrada_fecha = DateEntry(scroll_frame, date_pattern="yyyy-mm-dd")
    entrada_fecha.pack(pady=5)

    ctk.CTkLabel(scroll_frame, text="Género:").pack(pady=(10, 0))
    genero_var = ctk.StringVar(value="Masculino")
    genero_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
    genero_frame.pack()
    ctk.CTkRadioButton(genero_frame, text="Masculino", variable=genero_var, value="Masculino").pack(side="left", padx=10)
    ctk.CTkRadioButton(genero_frame, text="Femenino", variable=genero_var, value="Femenino").pack(side="left", padx=10)

    entrada_telefono = crear_entrada("Teléfono:")
    entrada_direccion = crear_entrada("Dirección:")

    ctk.CTkLabel(scroll_frame, text="--- Historial Médico ---", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=15)

    entrada_peso = crear_entrada("Peso (kg):")
    entrada_altura = crear_entrada("Altura (cm):")
    entrada_gruposanguineo = crear_entrada("Grupo Sanguíneo:")
    entrada_enfermedades = crear_entrada("Enfermedades Crónicas:")
    entrada_alergias = crear_entrada("Alergias:")
    entrada_historialfamiliar = crear_entrada("Historial Familiar:")
    entrada_habitos = crear_entrada("Hábitos (Tabaquismo, Alcohol, Dieta, Ejercicio):")

    def registrar():
        nombre = entrada_nombre.get()
        correo = entrada_correo.get()
        contrasena = entrada_contra.get()
        fecha = entrada_fecha.get()
        genero = genero_var.get()
        telefono = entrada_telefono.get()
        direccion = entrada_direccion.get()
        peso = entrada_peso.get()
        altura = entrada_altura.get()
        grupo_sanguineo = entrada_gruposanguineo.get()
        enfermedades = entrada_enfermedades.get()
        alergias = entrada_alergias.get()
        historialfamiliar = entrada_historialfamiliar.get()
        habitos = entrada_habitos.get()

        if not (nombre and correo and contrasena and fecha and genero and telefono and direccion):
            messagebox.showwarning("Campos Vacíos", "Por favor completa todos los campos obligatorios.")
            return

        try:
            db = conectar_db()
            cursor = db.cursor()

            cursor.execute("""
                INSERT INTO Usuarios (Nombre, Correo, Contraseña, idRol) 
                VALUES (%s, %s, %s, %s)
            """, (nombre, correo, contrasena, 3))  # idRol = 3 (paciente)

            id_usuario = cursor.lastrowid

            cursor.execute("""
                INSERT INTO Pacientes 
                (idUsuario, Nombre_Paciente, Fecha_nacimiento, Genero, Telefono, Direccion, Correo)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (id_usuario, nombre, fecha, genero, telefono, direccion, correo))

            id_paciente = cursor.lastrowid

            cursor.execute("""
                INSERT INTO HistorialMedico 
                (idPaciente, Peso, Altura, GrupoSanguineo, EnfermedadesCronicas, Alergias, HistorialFamiliar, Habitos)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (id_paciente, peso, altura, grupo_sanguineo, enfermedades, alergias, historialfamiliar, habitos))

            db.commit()
            db.close()

            messagebox.showinfo("Éxito", "Paciente registrado correctamente.")
            ventana.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar paciente: {e}")

    ctk.CTkButton(scroll_frame, text="Registrarse", command=registrar, width=300).pack(pady=30)

    ventana.mainloop()