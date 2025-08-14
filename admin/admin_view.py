import customtkinter as ctk
from admin.manage_users import gestionar_usuarios
from admin.manage_appointments import mostrar_citas
from admin.dating_statistics import mostrar_reporte_estadistico
from admin.show_medical_history import vista_general_historiales
from tkinter import messagebox
from main import lanzar_vitalapp

def abrir_admin(id_usuario):
    # Configuración general de apariencia
    ctk.set_appearance_mode("Dark")  # Opciones: "System", "Dark", "Light"
    ctk.set_default_color_theme("dark-blue")  # También: "green", "dark-blue", etc.

    ventana = ctk.CTk()
    ventana.title("Panel Administrador")
    ventana.geometry("900x600")
    ventana.resizable(False, False)

    # Frame principal
    frame_principal = ctk.CTkFrame(master=ventana, corner_radius=15)
    frame_principal.pack(pady=20, padx=60, fill="both", expand=True)

    # Título
    titulo = ctk.CTkLabel(frame_principal, text="Bienvenido, Administrador", font=("Helvetica", 24, "bold"))
    titulo.pack(pady=20)

    def volver_a_inicio():
        ventana.destroy()
        lanzar_vitalapp()

     # Funciones para cerrar ventana antes de abrir otra
    def abrir_gestion_usuarios():
        gestionar_usuarios(ventana)  # ✅ Pasa la ventana actual como argumento
        ventana.withdraw()  # ✅ Oculta en lugar de destruir


    def abrir_mostrar_citas():
        ventana.withdraw()  # Oculta la ventana actual
        mostrar_citas(ventana)

    def abrir_reporte_estadistico():
        ventana.withdraw()
        mostrar_reporte_estadistico(ventana)

    def abrir_historiales():
        ventana.withdraw()
        vista_general_historiales(ventana)

    # Botones principales
    ctk.CTkButton(
        frame_principal, 
        text="Gestión de Usuarios", 
        width=250, 
        height=40, 
        command=abrir_gestion_usuarios
    ).pack(pady=10)

    ctk.CTkButton(
        frame_principal, 
        text="Ver Citas Disponibles", 
        width=250, 
        height=40, 
        command=abrir_mostrar_citas
    ).pack(pady=10)

    ctk.CTkButton(
        frame_principal, 
        text="Ver Reportes de los Médicos", 
        width=250, 
        height=40, 
        command=abrir_reporte_estadistico
    ).pack(pady=10)

    ctk.CTkButton(
        frame_principal, 
        text="Historial de Pacientes", 
        width=250, 
        height=40, 
        command=abrir_historiales
    ).pack(pady=10)

    ctk.CTkButton(
        frame_principal, 
        text="Cerrar Sesión / Volver al Inicio", 
        width=150, 
        height=65, 
        command=volver_a_inicio
    ).pack(pady=20)
    
    ventana.mainloop()