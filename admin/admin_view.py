from tkinter import *
from admin.manage_users import gestionar_usuarios 
from admin.manage_appointments import mostrar_citas
#from admin.doctor_reports import mostrar_reportes
#from admin.patient_history import mostrar_historial

def abrir_admin():
    ventana = Tk()
    ventana.title("Panel Administrador")
    ventana.geometry("400x400")

    Label(ventana, text="Bienvenido, Administrador", font=("Arial", 16)).pack(pady=10)

    # Botón para abrir la ventana de gestión de usuarios
    Button(ventana, text="Gestión de Usuarios", width=30, command=gestionar_usuarios).pack(pady=5)
    Button(ventana, text="Ver Citas Disponibles", width=30, command=mostrar_citas).pack(pady=5)
    # Button(ventana, text="Ver Reportes Médicos", width=30, command=mostrar_reportes).pack(pady=5)
    # Button(ventana, text="Historial de Pacientes", width=30, command=mostrar_historial).pack(pady=5)

    ventana.mainloop()
