from tkinter import *
from tkinter import messagebox

def ventana_paciente():
    root = Tk()
    root.title("Panel del Paciente")
    root.geometry("400x600")

    Label(root, text="Bienvenido al Portal del Paciente", font=("Helvetica", 14, "bold")).pack(pady=20)

    Button(root, text="Agendar Cita", width=30, command=agendar_cita).pack(pady=10)
    Button(root, text="Ver/Crear Historial Médico", width=30, command=historial_medico).pack(pady=10)
    Button(root, text="Consultar o Modificar Citas", width=30, command=consultar_citas).pack(pady=10)
    Button(root, text="Descargar Recetas Médicas", width=30, command=descargar_recetas).pack(pady=10)
    Button(root, text="Ver Perfil del Médico", width=30, command=ver_perfil_medico).pack(pady=10)
    Button(root, text="Calificar al Doctor", width=30, command=calificar_doctor).pack(pady=10)
    Button(root, text="Ver Perfil del Paciente", width=30, command=ver_perfil_paciente).pack(pady=10)

    root.mainloop()

# --- FUNCIONES PARA CADA SECCIÓN ---

def agendar_cita():
    ventana = Toplevel()
    ventana.title("Agendar Cita")
    Label(ventana, text="Aquí se mostrarían los horarios disponibles").pack()

def historial_medico():
    ventana = Toplevel()
    ventana.title("Historial Médico")
    Label(ventana, text="Aquí se mostrará el historial o se podrá agregar nuevo").pack()

def consultar_citas():
    ventana = Toplevel()
    ventana.title("Consultar o Modificar Citas")
    Label(ventana, text="Aquí se mostrarán las citas del paciente").pack()

def descargar_recetas():
    ventana = Toplevel()
    ventana.title("Descargar Recetas")
    Label(ventana, text="Aquí se listarán las recetas médicas con opción de descarga").pack()

def ver_perfil_medico():
    ventana = Toplevel()
    ventana.title("Perfil del Médico")
    Label(ventana, text="Aquí se mostrará la información del médico que lo atenderá").pack()

def calificar_doctor():
    ventana = Toplevel()
    ventana.title("Calificar Doctor")
    Label(ventana, text="Deje su calificación (1-5)").pack()
    Entry(ventana).pack()
    Button(ventana, text="Enviar").pack(pady=10)

def ver_perfil_paciente():
    ventana = Toplevel()
    ventana.title("Perfil del Paciente")

    Label(ventana, text="Nombre: Juan Pérez").pack()
    Label(ventana, text="Edad: 35").pack()
    Label(ventana, text="Género: Masculino").pack()
    Label(ventana, text="Antecedentes Médicos: Hipertensión").pack()
    Label(ventana, text="Calificación promedio: 4.7").pack()
    Label(ventana, text="Teléfono: 555-123456").pack()

ventana_paciente()
