import customtkinter as ctk
from patient.add_appointments import agendar_cita
from patient.check_appointments import consultar_citas
from patient.view_treatments import ver_tratamientos
from db import conectar_db
from main import lanzar_vitalapp


def obtener_datos_paciente(id_usuario):
    db = conectar_db()
    try:
        cursor = db.cursor()
        cursor.execute("""
            SELECT p.idPaciente, u.Nombre
            FROM Pacientes p
            JOIN Usuarios u ON p.idUsuario = u.idUsuario
            WHERE p.idUsuario = %s
        """, (id_usuario,))
        resultado = cursor.fetchone()
        if resultado:
            return resultado[0], resultado[1]  # idPaciente, nombre
        else:
            print("No se encontró el paciente.")
            return None, None
    except Exception as e:
        print(f"Error al obtener datos del paciente: {e}")
        return None, None
    finally:
        db.close()


def abrir_patient(id_paciente, nombre_paciente):
    # Configurar el modo y tema de la app
    ctk.set_appearance_mode("Light")  # Opciones: "Light", "Dark", "System"
    ctk.set_default_color_theme("green")  # Opciones: "green", "dark-blue", "blue"

    ventana = ctk.CTk()
    ventana.title("Panel Paciente")
    ventana.geometry("900x600")
    ventana.resizable(False, False)

    # Título de bienvenida
    titulo = ctk.CTkLabel(
        ventana,
        text=f"Bienvenid@ {nombre_paciente}",
        font=ctk.CTkFont(size=24, weight="bold")
    )
    titulo.pack(pady=(40, 20))

    def volver_a_inicio():
        ventana.destroy()
        lanzar_vitalapp()

    def abrir_agendar_cita():
        ventana.withdraw()
        agendar_cita(id_paciente, ventana)

    def abrir_consultar_citas():
        ventana.withdraw()
        consultar_citas(id_paciente, ventana)

    def abrir_ver_recetas():
        ventana.withdraw()
        ver_tratamientos(id_paciente, ventana)

    # Botones principales
    botones = [
        ("Creación de Citas", abrir_agendar_cita),
        ("Consultar Citas", abrir_consultar_citas),
        ("Ver Recetas", abrir_ver_recetas)
    ]

    for texto, accion in botones:
        ctk.CTkButton(
            ventana,
            text=texto,
            width=220,
            height=40,
            command=accion,
            hover=True
        ).pack(pady=10)

    # Botón para volver al inicio
    boton_volver = ctk.CTkButton(
        ventana,
        text="Volver al Inicio",
        width=160,
        height=45,
        command=volver_a_inicio,
        fg_color="#D9534F",  # Rojo suave
        hover_color="#C9302C"
    )
    boton_volver.pack(pady=(30, 10))

    ventana.mainloop()