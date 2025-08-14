import customtkinter as ctk
from tkinter import messagebox, simpledialog
from db import conectar_db
import datetime

def consultar_citas(id_paciente, ventana_anterior):
    # Conectar a la base de datos
    db = conectar_db()
    cursor = db.cursor()
    citas = []
    cita_seleccionada = [None]  # lista mutable para actualizar dentro de closures

    def cargar_citas():
        for widget in scroll_frame.winfo_children():
            widget.destroy()

        citas.clear()
        cursor.execute("""
            SELECT c.idCita, c.Fecha_cita, h.Hora, m.Nombre_medico, c.Motivo_consulta, c.Estado
            FROM Citas c
            JOIN Medicos m ON c.idMedico = m.idMedico
            JOIN Horario h ON c.idHorario = h.idHorario
            WHERE c.idPaciente = %s
        """, (id_paciente,))
        citas_db = cursor.fetchall()
        for index, cita in enumerate(citas_db):
            citas.append(cita)
            idCita, fecha, hora, medico, motivo, estado = cita
            texto = f"{fecha.date()} {hora} | {medico} | {motivo} | {estado}"

            btn = ctk.CTkButton(
                scroll_frame,
                text=texto,
                command=lambda i=index: seleccionar_cita(i),
                width=600,
                fg_color="#95a5a6" if cita_seleccionada[0] != index else "#27ae60"
            )
            btn.pack(pady=5)

    def seleccionar_cita(index):
        cita_seleccionada[0] = index
        cargar_citas()  # refresca la UI para reflejar la selección

    def cancelar_cita():
        index = cita_seleccionada[0]
        if index is None:
            messagebox.showwarning("Seleccionar cita", "Selecciona una cita para cancelar.")
            return
        id_cita = citas[index][0]
        if messagebox.askyesno("Confirmar", "¿Seguro que quieres cancelar esta cita?"):
            cursor.execute("UPDATE Citas SET Estado = 'Cancelada' WHERE idCita = %s", (id_cita,))
            db.commit()
            messagebox.showinfo("Cancelado", "La cita fue cancelada.")
            cita_seleccionada[0] = None
            cargar_citas()

    def modificar_fecha():
        index = cita_seleccionada[0]
        if index is None:
            messagebox.showwarning("Seleccionar cita", "Selecciona una cita para modificar.")
            return
        id_cita = citas[index][0]
        nueva_fecha = simpledialog.askstring("Modificar Fecha", "Nueva fecha (YYYY-MM-DD):")
        if nueva_fecha:
            try:
                datetime.datetime.strptime(nueva_fecha, "%Y-%m-%d")
                cursor.execute("UPDATE Citas SET Fecha_cita = %s WHERE idCita = %s", (nueva_fecha, id_cita))
                db.commit()
                messagebox.showinfo("Modificado", "La fecha fue actualizada.")
                cargar_citas()
            except ValueError:
                messagebox.showerror("Formato inválido", "Formato de fecha inválido. Usa YYYY-MM-DD.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al modificar fecha:\n{e}")

    def modificar_horario():
        index = cita_seleccionada[0]
        if index is None:
            messagebox.showwarning("Seleccionar cita", "Selecciona una cita para modificar.")
            return
        id_cita = citas[index][0]

        cursor.execute("SELECT idHorario, Hora FROM Horario WHERE Disponible = 1")
        horarios = cursor.fetchall()
        if not horarios:
            messagebox.showinfo("Sin horarios", "No hay horarios disponibles.")
            return

        opciones = [f"{idH} - {hora}" for idH, hora in horarios]
        seleccion = simpledialog.askstring("Modificar Horario", "Selecciona nuevo horario:\n" + "\n".join(opciones))
        if seleccion:
            try:
                nuevo_id = int(seleccion.split('-')[0].strip())
                cursor.execute("UPDATE Citas SET idHorario = %s WHERE idCita = %s", (nuevo_id, id_cita))
                db.commit()
                messagebox.showinfo("Modificado", "El horario fue actualizado.")
                cargar_citas()
            except Exception as e:
                messagebox.showerror("Error", f"Error al modificar horario:\n{e}")

    def regresar():
        ventana.destroy()
        ventana_anterior.deiconify()

    # Configuración de la ventana
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")

    ventana = ctk.CTkToplevel()
    ventana.title("Mis Citas")
    ventana.geometry("750x600")
    ventana.resizable(False, False)

    ventana_anterior.withdraw()

    frame = ctk.CTkFrame(ventana)
    frame.pack(padx=20, pady=20, fill="both", expand=True)

    ctk.CTkLabel(frame, text="Citas Programadas", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=10)

    scroll_frame = ctk.CTkScrollableFrame(frame, height=350)
    scroll_frame.pack(padx=10, pady=10, fill="both", expand=True)

    boton_frame = ctk.CTkFrame(frame, fg_color="transparent")
    boton_frame.pack(pady=10)

    ctk.CTkButton(boton_frame, text="Cancelar Cita", command=cancelar_cita, fg_color="#e74c3c").grid(row=0, column=0, padx=5)
    ctk.CTkButton(boton_frame, text="Modificar Fecha", command=modificar_fecha, fg_color="#3498db").grid(row=0, column=1, padx=5)
    ctk.CTkButton(boton_frame, text="Modificar Horario", command=modificar_horario, fg_color="#2ecc71").grid(row=0, column=2, padx=5)

    ctk.CTkButton(frame, text="Regresar", command=regresar).pack(pady=10)

    cargar_citas()
    ventana.protocol("WM_DELETE_WINDOW", regresar)  # Si cierra con la X, también regresa

    ventana.mainloop()
    db.close()