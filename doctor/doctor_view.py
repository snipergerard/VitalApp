import customtkinter as ctk
from doctor.pending_appointments import ver_citas_pendientes
from doctor.treatments import agregar_tratamiento
from doctor.medical_history import gestionar_historiales_medicos
from db import conectar_db
from main import lanzar_vitalapp  # Asegúrate que exista

def obtener_id_medico(id_usuario):
    db = conectar_db()
    try:
        cursor = db.cursor()
        cursor.execute("SELECT idMedico FROM Medicos WHERE idUsuario = %s", (id_usuario,))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else None
    except Exception as e:
        print(f"Error al obtener id_medico: {e}")
        return None
    finally:
        db.close()

def abrir_doctor(id_usuario):
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    ventana = ctk.CTk()
    ventana.title("Panel Médico")
    ventana.geometry("900x600")
    ventana.resizable(False, False)

    def volver_a_inicio():
        ventana.destroy()
        lanzar_vitalapp()

    def abrir_ver_citas():
        ventana.withdraw()
        ver_citas_pendientes(id_usuario, ventana)
        
    def abrir_tratamientos():
        ventana.withdraw()
        agregar_tratamiento(id_usuario, ventana)

    def abrir_historiales():
        ventana.withdraw()
        gestionar_historiales_medicos(id_usuario, ventana)

    ctk.CTkLabel(
        ventana,
        text="Bienvenido, Médic@",
        font=("Arial", 24, "bold"),
        text_color="#333333"
    ).pack(pady=40)

    ctk.CTkButton(
        ventana, text="Ver Citas Pendientes",
        width=250, height=40, font=("Arial", 14),
        command=abrir_ver_citas
    ).pack(pady=10)

    ctk.CTkButton(
        ventana, text="Agregar Tratamientos",
        width=250, height=40, font=("Arial", 14),
        command=abrir_tratamientos
    ).pack(pady=10)

    ctk.CTkButton(
        ventana, text="Modificar Historial Médico",
        width=250, height=40, font=("Arial", 14),
        command=abrir_historiales
    ).pack(pady=10)

    ctk.CTkButton(
        ventana, 
        text="Regresar al Menú Principal",
        width=150, 
        height=65, font=("Arial", 14),
        fg_color="#999999", hover_color="#777777",
        command=lambda: volver_a_inicio(ventana)
    ).pack(pady=30)

    ventana.mainloop()