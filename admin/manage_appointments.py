from tkinter import *
from tkinter import ttk, messagebox
from db import conectar_db

def mostrar_citas():
    ventana = Toplevel()
    ventana.title("Citas Pendientes")
    ventana.geometry("800x400")

    Label(ventana, text="Citas Pendientes", font=("Arial", 14)).pack(pady=10)

    columnas = ("id", "fecha", "paciente", "medico", "motivo", "estado")
    tabla = ttk.Treeview(ventana, columns=columnas, show="headings")

    for col in columnas:
        tabla.heading(col, text=col.capitalize())
        tabla.column(col, anchor="center")

    tabla.pack(expand=True, fill="both", padx=10, pady=10)

    try:
        db = conectar_db()
        cursor = db.cursor()

        consulta = """
            SELECT c.idCita, c.Fecha_cita, p.Nombre_Paciente AS paciente, m.Nombre_Medico AS medico,
                   c.Motivo_consulta, c.Estado
            FROM Citas c
            JOIN Pacientes p ON c.idPaciente = p.idPaciente
            JOIN Medicos m ON c.idMedico = m.idMedico
            WHERE c.Estado = 'Pendiente'
            ORDER BY c.Fecha_cita
        """

        cursor.execute(consulta)
        citas = cursor.fetchall()
        db.close()

        for cita in citas:
            tabla.insert("", "end", values=cita)

    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron obtener las citas: {e}")
