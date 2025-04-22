from tkinter import *
from tkinter import messagebox
from authenticator import login
from db import conectar_db
import tkinter as tk


def ventana_paciente():
    root = Tk()
    root.title("Panel del Paciente")
    root.geometry("400x600")

    
    Label(root, text="Bienvenido al Portal del Paciente", font=("Helvetica", 14, "bold")).pack(pady=20)

    Button(root, text="Agendar Cita", width=30, command=agendar_cita).pack(pady=10)
    #Button(root, text="Ver/Crear Historial Médico", width=30, command=historial_medico).pack(pady=10)
    Button(root, text="Consultar o Modificar Citas", width=30, command=consultar_citas).pack(pady=10)
    Button(root, text="Descargar Recetas Médicas", width=30, command=descargar_recetas).pack(pady=10)
    Button(root, text="Ver Perfil del Médico", width=30, command=ver_perfil_medico).pack(pady=10)
    Button(root, text="Calificar al Doctor", width=30, command=calificar_doctor).pack(pady=10)
    Button(root, text="Ver Perfil del Paciente", width=30, command=ver_perfil_paciente).pack(pady=10)

    root.mainloop()

# --- FUNCIONES PARA CADA SECCIÓN ---

import tkinter as tk
from tkinter import Toplevel, Label, Entry, Button

def agendar_cita():
    ventana = Toplevel()
    ventana.title("Agendar Cita")

    # Etiqueta
    Label(ventana, text="Buscar por Especialidad:").grid(row=0, column=0, padx=5, pady=5)
    # Campo de entrada
    entrada_texto = Entry(ventana, width=30)
    entrada_texto.grid(row=0, column=1, padx=5, pady=5)
    doctor_var = StringVar()
    doctor_dropdown = None
    doctores_dict = {}

    horario_var = StringVar()
    horario_dropdown = None
    horarios_dict = {}

    # Acción del botón
    def buscar():
        texto_busqueda = entrada_texto.get()
        print(f"Especialidad: {texto_busqueda}")
        # Aquí puedes agregar lógica para mostrar los horarios según la especialidad

    # Botón de búsqueda
    Button(ventana, text="Buscar", command=buscar).grid(row=0, column=2, padx=5, pady=5)
    doctor_var = StringVar()
    doctor_dropdown = None
    doctores_dict = {}  # para guardar nombre → id

    def buscar():
        especialidad = entrada_texto.get()
        if not especialidad:
            messagebox.showwarning("Campo vacío", "Por favor ingresa una especialidad.")
            return

        try:
            db = conectar_db()
            cursor = db.cursor()
            cursor.execute("""
                SELECT idMedico, Nombre_Medico 
                FROM Medicos 
                WHERE Especialidad = %s
            """, (especialidad,))
            resultados = cursor.fetchall()
            db.close()

            if not resultados:
                messagebox.showinfo("Sin resultados", "No hay doctores disponibles para esta especialidad.")
                return

            # Guardamos los doctores
            doctores_dict.clear()
            for id_, nombre in resultados:
                doctores_dict[nombre] = id_

            # Crear dropdown dinámicamente
            opciones = list(doctores_dict.keys())
            doctor_var.set(opciones[0])  # Primer doctor como selección por defecto

            nonlocal doctor_dropdown  # Acceder a la variable externa
            if doctor_dropdown:
                doctor_dropdown.destroy()  # Si ya existía, eliminarlo

            doctor_dropdown = OptionMenu(ventana, doctor_var, *opciones)
            doctor_dropdown.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

            # Botón para seleccionar doctor
            Button(ventana, text="Seleccionar Doctor", command=seleccionar_doctor).grid(row=3, column=0, columnspan=2, pady=10)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron buscar los doctores: {e}")



    def seleccionar_doctor():
        nombre_doctor = doctor_var.get()
        id_doctor = doctores_dict.get(nombre_doctor)

        messagebox.showinfo("Doctor seleccionado", f"Has seleccionado al Dr. {nombre_doctor}")


        try:
            db = conectar_db()
            cursor = db.cursor()
            cursor.execute("""
                SELECT idHorario, Fecha_cita 
                FROM Horario 
                WHERE idMedico = %s AND Disponible = 1
            """, (id_doctor,))
            horarios = cursor.fetchall()
            db.close()

            if not horarios:
                messagebox.showinfo("Sin horarios", "Este doctor no tiene horarios disponibles.")
                return

            horarios_dict.clear()
            opciones_horario = []
            for id_horario, fecha in horarios:
                texto = f"{fecha}"
                horarios_dict[texto] = id_horario
                opciones_horario.append(texto)


            horario_var.set(opciones_horario[0])

            nonlocal horario_dropdown
            if horario_dropdown:
                horario_dropdown.destroy()

            horario_dropdown = OptionMenu(ventana, horario_var, *opciones_horario)
            horario_dropdown.grid(row=4, column=0, columnspan=2, padx=5, pady=10)

            Button(ventana, text="Agendar Cita", command=agendar).grid(row=5, column=0, columnspan=2, pady=10)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los horarios: {e}")

    def agendar():
        horario_texto = horario_var.get()
        id_horario = horarios_dict.get(horario_texto)

        try:
            db = conectar_db()
            cursor = db.cursor()

            # Aquí se supone que tienes el id del paciente ya autenticado. Cambiar por el real:
            id_paciente = 1  # ejemplo fijo

            # Insertar la cita
            cursor.execute("""
                INSERT INTO Citas (idHorario, idPaciente, Estado) 
                VALUES (%s, %s, 'Pendiente')
            """, (id_horario, id_paciente))

            # Marcar el horario como no disponible
            cursor.execute("UPDATE Horarios SET Disponible = 0 WHERE idHorario = %s", (id_horario,))

            db.commit()
            db.close()

            messagebox.showinfo("Éxito", "Cita agendada correctamente.")
            ventana.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agendar la cita: {e}")

    Button(ventana, text="Buscar", command=buscar).grid(row=0, column=2, padx=5, pady=5)

#def historial_medico():
    #ventana = Toplevel()
    #ventana.title("Historial Médico")
    #Label(ventana, text="Aquí se mostrará el historial o se podrá agregar nuevo").pack()

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
