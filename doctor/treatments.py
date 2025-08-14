import customtkinter as ctk
from tkinter import messagebox
from db import conectar_db

def agregar_tratamiento(id_medico, ventana_anterior):
    ctk.set_appearance_mode("light")  # o "dark"
    ctk.set_default_color_theme("blue")

    ventana = ctk.CTkToplevel()
    ventana.title("Agregar Tratamiento")
    ventana.geometry("700x500")

    ventana_anterior.withdraw()  # Oculta la ventana anterior

    def regresar():
        ventana.destroy()
        ventana_anterior.deiconify()

    titulo = ctk.CTkLabel(ventana, text="Agregar Tratamiento", font=("Arial", 24, "bold"))
    titulo.pack(pady=20)

    boton_regresar = ctk.CTkButton(ventana, text="Regresar al Menú", command=regresar)
    boton_regresar.pack(pady=10)

    try:
        db = conectar_db()
        cursor = db.cursor()
        cursor.execute("""
            SELECT c.idCita, p.Nombre_Paciente, c.Fecha_cita
            FROM Citas c
            JOIN Pacientes p ON c.idPaciente = p.idPaciente
            LEFT JOIN Tratamientos t ON c.idCita = t.idCita
            WHERE c.idMedico = %s AND c.Estado = 'Realizada' AND t.idTratamientos IS NULL
            ORDER BY c.Fecha_cita
        """, (id_medico,))
        citas = cursor.fetchall()
        db.close()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron obtener las citas realizadas: {e}")
        return

    if not citas:
        ctk.CTkLabel(ventana, text="No hay citas realizadas sin tratamiento.",
                     font=("Arial", 14), text_color="gray").pack(pady=20)
        return

    scroll_frame = ctk.CTkScrollableFrame(ventana, width=650, height=380)
    scroll_frame.pack(pady=10, padx=10)

    for id_cita, nombre_paciente, fecha in citas:
        frame = ctk.CTkFrame(scroll_frame, fg_color="#f0f0f0", corner_radius=8)
        frame.pack(fill="x", padx=5, pady=5)

        ctk.CTkLabel(frame, text=f"{nombre_paciente} | {fecha.date()}",
                     font=("Arial", 14), anchor="w").pack(side="left", padx=10)

        ctk.CTkButton(frame, text="Agregar Tratamiento", width=180,
                      command=lambda c=id_cita, f=frame: ventana_tratamiento(c, f)).pack(side="right", padx=10)


def ventana_tratamiento(id_cita, frame_cita):
    nueva_ventana = ctk.CTkToplevel()
    nueva_ventana.title("Nuevo Tratamiento")
    nueva_ventana.geometry("500x450")

    ctk.CTkLabel(nueva_ventana, text="Descripción:", font=("Arial", 14)).pack(pady=(15, 5))
    entry_descripcion = ctk.CTkEntry(nueva_ventana, width=400)
    entry_descripcion.pack(pady=5)

    ctk.CTkLabel(nueva_ventana, text="Medicamentos:", font=("Arial", 14)).pack(pady=(15, 5))
    entry_medicamentos = ctk.CTkEntry(nueva_ventana, width=400)
    entry_medicamentos.pack(pady=5)

    ctk.CTkLabel(nueva_ventana, text="Dosis:", font=("Arial", 14)).pack(pady=(15, 5))
    entry_dosis = ctk.CTkEntry(nueva_ventana, width=400)
    entry_dosis.pack(pady=5)

    ctk.CTkLabel(nueva_ventana, text="Duración:", font=("Arial", 14)).pack(pady=(15, 5))
    entry_duracion = ctk.CTkEntry(nueva_ventana, width=400)
    entry_duracion.pack(pady=5)

    def guardar_tratamiento():
        descripcion = entry_descripcion.get()
        medicamentos = entry_medicamentos.get()
        dosis = entry_dosis.get()
        duracion = entry_duracion.get()

        if not descripcion or not medicamentos or not dosis or not duracion:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            return

        try:
            db = conectar_db()
            cursor = db.cursor()
            cursor.execute("""
                INSERT INTO Tratamientos (idCita, Descripcion, Medicamentos, Dosis, Duracion)
                VALUES (%s, %s, %s, %s, %s)
            """, (id_cita, descripcion, medicamentos, dosis, duracion))
            db.commit()
            db.close()
            messagebox.showinfo("Éxito", "Tratamiento guardado correctamente.")
            nueva_ventana.destroy()
            frame_cita.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el tratamiento: {e}")

    ctk.CTkButton(nueva_ventana, text="Guardar Tratamiento",
                  command=guardar_tratamiento, width=200).pack(pady=20)