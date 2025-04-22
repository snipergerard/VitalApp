from tkinter import *
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

def agendar_cita(id_paciente):
    ventana = Tk()
    ventana.title("Agendar Cita - VitalApp")
    ventana.geometry("400x600")

    Label(ventana, text="Selecciona la Especialidad Médica:").pack(pady=5)
    especialidades = obtener_especialidades()
    especialidad_var = StringVar()
    if especialidades:
        especialidad_var.set(especialidades[0])
    especialidad_menu = OptionMenu(ventana, especialidad_var, *especialidades)
    especialidad_menu.pack()

    Label(ventana, text="Selecciona el Médico:").pack(pady=5)
    medico_var = StringVar()
    medico_menu = OptionMenu(ventana, medico_var, '')
    medico_menu.pack()

    Label(ventana, text="Fecha de la Cita:").pack(pady=5)
    entrada_fecha_cita = DateEntry(ventana, date_pattern='yyyy-mm-dd')
    entrada_fecha_cita.pack()

    Label(ventana, text="Selecciona el Horario:").pack(pady=5)
    horario_var = StringVar()
    horario_menu = OptionMenu(ventana, horario_var, '')
    horario_menu.pack()

    Label(ventana, text="Motivo de la Consulta:").pack(pady=5)
    entrada_motivo = Entry(ventana)
    entrada_motivo.pack()

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

        medico_menu['menu'].delete(0, 'end')
        opciones_medico.clear()

        for id_medico, nombre in medicos:
            medico_menu['menu'].add_command(label=nombre, command=lambda value=nombre: medico_var.set(value))
            opciones_medico[nombre] = id_medico

        if medicos:
            medico_var.set(medicos[0][1])  # Nombre del primero
        else:
            medico_var.set('')

    def actualizar_horarios(*args):
        nombre_medico = medico_var.get()
        fecha_cita = entrada_fecha_cita.get_date()
        id_medico = opciones_medico.get(nombre_medico)

        if not (id_medico and fecha_cita):
            return

        horarios = obtener_horarios(id_medico, fecha_cita)

        menu = horario_menu['menu']
        menu.delete(0, 'end')

        if horarios:
            for id_horario, hora in horarios:
                hora_str = hora.strftime('%H:%M') if isinstance(hora, datetime.time) else str(hora)
                menu.add_command(label=hora_str, command=lambda value=hora_str: horario_var.set(value))
            primer_horario = horarios[0][1]
            horario_var.set(primer_horario.strftime('%H:%M') if isinstance(primer_horario, datetime.time) else str(primer_horario))
        else:
            horario_var.set('')

    def agendar_cita_db():
        especialidad = especialidad_var.get()
        medico = medico_var.get()
        fecha_cita = entrada_fecha_cita.get_date()
        horario = horario_var.get()
        motivo = entrada_motivo.get()

        # Aquí, deberías insertar la cita en la base de datos
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

    # Asociar eventos
    especialidad_var.trace("w", actualizar_medicos)
    medico_var.trace("w", actualizar_horarios)
    entrada_fecha_cita.bind("<<DateEntrySelected>>", lambda event: actualizar_horarios())

    Button(ventana, text="Agendar Cita", command=agendar_cita_db).pack(pady=20)

    ventana.mainloop()
