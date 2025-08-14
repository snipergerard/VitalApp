import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import Calendar
from db import conectar_db

def ver_citas_pendientes(id_medico, ventana_anterior):
    ctk.set_appearance_mode("light") 
    ctk.set_default_color_theme("blue")

    ventana = ctk.CTkToplevel()
    ventana.title("Citas Pendientes")
    ventana.geometry("800x600")

    ventana_anterior.withdraw()  # Oculta la ventana anterior

    def regresar():
        ventana.destroy()
        ventana_anterior.deiconify()

    titulo = ctk.CTkLabel(ventana, text="Citas Pendientes", font=("Arial", 20, "bold"))
    titulo.pack(pady=20)

    boton_regresar = ctk.CTkButton(ventana, text= "Regresar al Menú", command=regresar)
    boton_regresar.pack(pady=10)

    try:
        db = conectar_db()
        cursor = db.cursor()
        cursor.execute("""
            SELECT c.idCita, p.Nombre_Paciente, c.Fecha_cita, h.Hora, c.Estado
            FROM Citas c
            JOIN Pacientes p ON c.idPaciente = p.idPaciente
            JOIN Horario h ON c.idHorario = h.idHorario
            WHERE c.idMedico = %s AND c.Estado = 'Pendiente'
            ORDER BY c.Fecha_cita, h.Hora
        """, (id_medico,))
        citas = cursor.fetchall()
        db.close()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron obtener las citas: {e}")
        return

    if not citas:
        ctk.CTkLabel(ventana, text="No hay citas pendientes.", font=("Arial", 14), text_color="gray").pack(pady=20)
        return

    frame_scroll = ctk.CTkScrollableFrame(ventana, width=750, height=500, fg_color="white")
    frame_scroll.pack(padx=20, pady=10)

    for id_cita, nombre_paciente, fecha, hora, estado in citas:
        frame = ctk.CTkFrame(frame_scroll, fg_color="#f0f0f0", corner_radius=8)
        frame.pack(fill="x", padx=5, pady=5)

        texto = f"{nombre_paciente} | {fecha.date()} {hora} | Estado: {estado}"
        ctk.CTkLabel(frame, text=texto, font=("Arial", 14), anchor="w").pack(pady=5, padx=10, side="left", expand=True)

        btns_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btns_frame.pack(side="right", padx=10)

        ctk.CTkButton(btns_frame, text="Modificar", width=80, height=28,
                      command=lambda c=id_cita: modificar_cita(c)).pack(side="left", padx=5)
        ctk.CTkButton(btns_frame, text="Realizada", width=80, height=28,
                      command=lambda c=id_cita: actualizar_estado_cita(c, "Realizada")).pack(side="left", padx=5)
        ctk.CTkButton(btns_frame, text="Cancelar", width=80, height=28,
                      command=lambda c=id_cita: actualizar_estado_cita(c, "Cancelada")).pack(side="left", padx=5)


    #ventana.mainloop()
    
def modificar_cita(id_cita):
    ventana = ctk.CTkToplevel()
    ventana.title("Modificar Cita")
    ventana.geometry("400x350")

    ctk.CTkLabel(ventana, text="Nueva Fecha:", font=("Arial", 14)).pack(pady=10)
    calendario = Calendar(ventana, date_pattern='yyyy-mm-dd')
    calendario.pack(pady=5)

    ctk.CTkLabel(ventana, text="Nuevo Horario:", font=("Arial", 14)).pack(pady=10)
    horario_var = ctk.StringVar()
    horarios = []

    try:
        db = conectar_db()
        cursor = db.cursor()
        cursor.execute("SELECT idHorario, Hora FROM Horario ORDER BY Hora")
        resultados = cursor.fetchall()
        db.close()
        horarios = [f"{id} - {hora}" for id, hora in resultados]
        if horarios:
            horario_var.set(horarios[0])
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar los horarios: {e}")
        return

    option_menu = ctk.CTkOptionMenu(ventana, variable=horario_var, values=horarios, width=250)
    option_menu.pack(pady=10)

    def guardar_modificacion():
        nueva_fecha = calendario.get_date()
        seleccionado = horario_var.get()
        nuevo_id_horario = seleccionado.split(" - ")[0]

        try:
            db = conectar_db()
            cursor = db.cursor()
            cursor.execute("UPDATE Citas SET Fecha_cita=%s, idHorario=%s WHERE idCita=%s",
                           (nueva_fecha, nuevo_id_horario, id_cita))
            db.commit()
            db.close()
            messagebox.showinfo("Éxito", "Cita modificada correctamente.")
            ventana.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo modificar la cita: {e}")

    ctk.CTkButton(ventana, text="Guardar Cambios", command=guardar_modificacion).pack(pady=20)


def actualizar_estado_cita(id_cita, nuevo_estado):
    try:
        db = conectar_db()
        cursor = db.cursor()
        cursor.execute("UPDATE Citas SET Estado=%s WHERE idCita=%s", (nuevo_estado, id_cita))
        db.commit()
        db.close()
        messagebox.showinfo("Éxito", f"Cita marcada como {nuevo_estado}.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo actualizar el estado: {e}")