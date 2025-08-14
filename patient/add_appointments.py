import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import DateEntry
import datetime
from db import conectar_db

def obtener_especialidades():
    db = conectar_db()
    cursor = db.cursor()
    cursor.execute("SELECT nombre_especialidad FROM Especialidad")
    especialidades = [row[0] for row in cursor.fetchall()]
    db.close()
    return especialidades

def obtener_horarios(id_medico, fecha_cita):
    db = conectar_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT h.idHorario, h.Hora
        FROM Horario h
        WHERE h.Disponible = 1 AND h.idHorario NOT IN (
            SELECT c.idHorario 
            FROM Citas c
            WHERE c.idMedico = %s AND DATE(c.Fecha_cita) = %s AND c.Estado = 'Pendiente'
        )
    """, (id_medico, fecha_cita))
    horarios = cursor.fetchall()
    db.close()
    return horarios

def agendar_cita(id_paciente,ventana_anterior):
    ctk.set_appearance_mode("Light")  # Opcional: "Light" o "Dark"
    ctk.set_default_color_theme("green")  # Opcional: "green", "dark-blue", etc.

    ventana = ctk.CTkToplevel()
    ventana.title("Agendar Cita - VitalApp")
    ventana.geometry("500x650")
    ventana.resizable(False, False)

    ventana_anterior.withdraw()  # Ocultar la ventana anterior

    def regresar():
        ventana.destroy()
        ventana_anterior.deiconify()

    frame = ctk.CTkFrame(ventana)
    frame.pack(padx=20, pady=20, fill="both", expand=True)

    boton_regresar = ctk.CTkButton(frame, text="Regresar", command=regresar)
    boton_regresar.pack(pady=10)

    ctk.CTkLabel(frame, text="Selecciona la Especialidad Médica:", font=ctk.CTkFont(size=16)).pack(pady=5)
    especialidades = obtener_especialidades()
    especialidad_var = ctk.StringVar()
    especialidad_menu = ctk.CTkOptionMenu(frame, variable=especialidad_var, values=especialidades if especialidades else [""])
    especialidad_menu.pack(pady=5)

    ctk.CTkLabel(frame, text="Selecciona el Médico:", font=ctk.CTkFont(size=16)).pack(pady=5)
    medico_var = ctk.StringVar()
    medico_menu = ctk.CTkOptionMenu(frame, variable=medico_var, values=[""])
    medico_menu.pack(pady=5)

    ctk.CTkLabel(frame, text="Fecha de la Cita:", font=ctk.CTkFont(size=16)).pack(pady=5)
    entrada_fecha_cita = DateEntry(frame, date_pattern='yyyy-mm-dd')
    entrada_fecha_cita.pack(pady=5)

    ctk.CTkLabel(frame, text="Selecciona el Horario:", font=ctk.CTkFont(size=16)).pack(pady=5)
    horario_var = ctk.StringVar()
    horario_menu = ctk.CTkOptionMenu(frame, variable=horario_var, values=[""])
    horario_menu.pack(pady=5)

    ctk.CTkLabel(frame, text="Motivo de la Consulta:", font=ctk.CTkFont(size=16)).pack(pady=5)
    entrada_motivo = ctk.CTkEntry(frame, width=300)
    entrada_motivo.pack(pady=5)

    opciones_medico = {}

    def actualizar_medicos(*args):
        especialidad = especialidad_var.get()
        db = conectar_db()
        cursor = db.cursor()
        cursor.execute("""
            SELECT idMedico, Nombre_medico
            FROM Medicos
            WHERE idEspecialidad = (SELECT idEspecialidad FROM Especialidad WHERE nombre_especialidad = %s)
        """, (especialidad,))
        medicos = cursor.fetchall()
        db.close()

        medico_menu.configure(values=[nombre for _, nombre in medicos])
        opciones_medico.clear()

        for id_medico, nombre in medicos:
            opciones_medico[nombre] = id_medico

        if medicos:
            medico_var.set(medicos[0][1])  # Primer médico
        else:
            medico_var.set('')

    def actualizar_horarios(*args):
        nombre_medico = medico_var.get()
        fecha_cita = entrada_fecha_cita.get_date()
        id_medico = opciones_medico.get(nombre_medico)

        if not (id_medico and fecha_cita):
            return

        horarios = obtener_horarios(id_medico, fecha_cita)

        if horarios:
            horas_str = [hora.strftime('%H:%M') if isinstance(hora, datetime.time) else str(hora) for _, hora in horarios]
            horario_menu.configure(values=horas_str)
            horario_var.set(horas_str[0])
        else:
            horario_menu.configure(values=[""])
            horario_var.set('')

    def agendar_cita_db():
        especialidad = especialidad_var.get()
        medico = medico_var.get()
        fecha_cita = entrada_fecha_cita.get_date()
        horario = horario_var.get()
        motivo = entrada_motivo.get()

        id_medico = opciones_medico.get(medico)
        if not (id_medico and fecha_cita and horario and motivo):
            messagebox.showwarning("Campos Incompletos", "Por favor, completa todos los campos.")
            return

        db = conectar_db()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO Citas (idPaciente, idMedico, Fecha_cita, idHorario, Motivo_consulta, Estado)
            VALUES (%s, %s, %s, (SELECT idHorario FROM Horario WHERE Hora = %s LIMIT 1), %s, 'Pendiente')
        """, (id_paciente, id_medico, fecha_cita, horario, motivo))
        db.commit()
        db.close()

        messagebox.showinfo("Cita Agendada", "Tu cita ha sido agendada correctamente.")
        ventana.destroy()

    # Asociar eventos
    especialidad_var.trace_add("write", actualizar_medicos)
    medico_var.trace_add("write", actualizar_horarios)
    entrada_fecha_cita.bind("<<DateEntrySelected>>", lambda event: actualizar_horarios())

    boton_agendar = ctk.CTkButton(frame, text="Agendar Cita", command=agendar_cita_db, width=200)
    boton_agendar.pack(pady=20)

    ventana.mainloop()