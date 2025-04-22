from tkinter import *
from tkinter import messagebox
from db import conectar_db

def consultar_citas(id_paciente):
    ventana = Toplevel()  # Creamos una nueva ventana
    ventana.title("Mis Citas")
    ventana.geometry("400x600")
    
    # Etiqueta
    Label(ventana, text="Citas Programadas", font=("Arial", 16)).pack(pady=20)
    
    # Obtener citas del paciente desde la base de datos
    db = conectar_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT c.Fecha_cita, m.Nombre_medico, c.Motivo_consulta, c.Estado
        FROM Citas c
        JOIN Medicos m ON c.idMedico = m.idMedico
        WHERE c.idPaciente = %s
    """, (id_paciente,))
    
    citas = cursor.fetchall()
    db.close()

    if citas:
        # Mostrar las citas en la ventana
        for fecha, medico, motivo, estado in citas:
            cita_info = f"Fecha: {fecha}, Médico: {medico}, Motivo: {motivo}, Estado: {estado}"
            Label(ventana, text=cita_info).pack(pady=5)
    else:
        Label(ventana, text="No tienes citas programadas.").pack(pady=20)
    
    ventana.mainloop()