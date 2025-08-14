import customtkinter as ctk
from tkinter import messagebox
from db import conectar_db
from datetime import datetime

def gestionar_historiales_medicos(id_medico,ventana_anterior):
    ctk.set_appearance_mode("light")  # Puedes cambiar a "dark"
    ctk.set_default_color_theme("blue")

    ventana = ctk.CTkToplevel()
    ventana.title("Gestionar Historiales Médicos")
    ventana.geometry("800x600")

    ventana_anterior.withdraw()

    def regresar():
        ventana.destroy()
        ventana_anterior.deiconify()

    titulo = ctk.CTkLabel(ventana, text="Historiales Médicos", font=("Arial", 24, "bold"))
    titulo.pack(pady=20)

    boton_regresar = ctk.CTkButton(ventana, text="Regresar al Menú", command=regresar)
    boton_regresar.pack(pady=10)

    try:
        db = conectar_db()
        cursor = db.cursor()
        cursor.execute("""
            SELECT p.idPaciente, p.Nombre_Paciente, h.Peso, h.Altura, h.GrupoSanguineo, 
                   h.EnfermedadesCronicas, h.Alergias, h.HistorialFamiliar, h.Habitos,
                   h.EstadoGeneral, h.Observaciones
            FROM Citas c
            JOIN Pacientes p ON c.idPaciente = p.idPaciente
            LEFT JOIN HistorialMedico h ON p.idPaciente = h.idPaciente
            WHERE c.idMedico = %s AND c.Estado = 'Realizada'
            ORDER BY p.Nombre_Paciente
        """, (id_medico,))
        pacientes = cursor.fetchall()
        db.close()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron obtener los pacientes: {e}")
        return

    if not pacientes:
        ctk.CTkLabel(ventana, text="No hay pacientes con citas realizadas.", text_color="gray", font=("Arial", 14)).pack(pady=20)
        return

    scroll = ctk.CTkScrollableFrame(ventana, width=750, height=450)
    scroll.pack(pady=10, padx=10)

    for paciente in pacientes:
        id_paciente, nombre, peso, altura, grupo, enfermedades, alergias, historial_fam, habitos, estado, observaciones = paciente

        frame = ctk.CTkFrame(scroll, corner_radius=10)
        frame.pack(fill="x", padx=10, pady=8)

        info = f"{nombre}\n"
        info += f"Peso: {peso or 'No registrado'} kg | Altura: {altura or 'No registrado'} m | Grupo: {grupo or 'No registrado'}\n"
        info += f"Enfermedades: {enfermedades or 'No registrado'}\n"
        info += f"Alergias: {alergias or 'No registrado'}\n"
        info += f"Historial Familiar: {historial_fam or 'No registrado'}\n"
        info += f"Hábitos: {habitos or 'No registrado'}\n"
        info += f"Estado General: {estado or 'No registrado'}\n"
        info += f"Observaciones: {observaciones or 'No registrado'}"

        ctk.CTkLabel(frame, text=info, anchor="w", justify="left", font=("Arial", 12)).pack(side="left", padx=10, fill="both", expand=True)

        ctk.CTkButton(frame, text="Editar", width=120,
                      command=lambda idp=id_paciente, f=frame: ventana_editar_historial(idp, f)).pack(side="right", padx=10)


def ventana_editar_historial(id_paciente, frame_paciente):
    nueva_ventana = ctk.CTkToplevel()
    nueva_ventana.title("Editar Historial Médico")
    nueva_ventana.geometry("600x700")

    campos = {
        "Peso (kg)": ctk.StringVar(),
        "Altura (m)": ctk.StringVar(),
        "Grupo Sanguineo": ctk.StringVar(),
        "Enfermedades Cronicas": ctk.StringVar(),
        "Alergias": ctk.StringVar(),
        "Historial Familiar": ctk.StringVar(),
        "Habitos": ctk.StringVar(),
        "Estado General": ctk.StringVar(),
        "Observaciones": ctk.StringVar()
    }

    ctk.CTkLabel(nueva_ventana, text="Editar Historial Médico", font=("Arial", 20, "bold")).pack(pady=20)

    frame_campos = ctk.CTkFrame(nueva_ventana)
    frame_campos.pack(pady=10, padx=20, fill="both", expand=True)

    for idx, (campo, var) in enumerate(campos.items()):
        ctk.CTkLabel(frame_campos, text=campo + ":", anchor="w", width=150).grid(row=idx, column=0, sticky="e", padx=10, pady=8)
        ctk.CTkEntry(frame_campos, textvariable=var, width=300).grid(row=idx, column=1, padx=10, pady=8)

    def cargar_datos():
        try:
            db = conectar_db()
            cursor = db.cursor()
            cursor.execute("""
                SELECT Peso, Altura, GrupoSanguineo, EnfermedadesCronicas, 
                       Alergias, HistorialFamiliar, Habitos, EstadoGeneral, Observaciones
                FROM HistorialMedico
                WHERE idPaciente = %s
            """, (id_paciente,))
            datos = cursor.fetchone()
            db.close()

            if datos:
                for i, value in enumerate(datos):
                    list(campos.values())[i].set(value)
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar historial médico: {e}")

    def guardar_cambios():
        valores = [var.get() for var in campos.values()]
        if any(not v for v in valores):
            messagebox.showwarning("Advertencia", "Todos los campos deben estar completos.")
            return
        try:
            db = conectar_db()
            cursor = db.cursor()

            cursor.execute("SELECT idHistorial FROM HistorialMedico WHERE idPaciente = %s", (id_paciente,))
            existe = cursor.fetchone()

            if existe:
                cursor.execute("""
                    UPDATE HistorialMedico
                    SET Peso=%s, Altura=%s, GrupoSanguineo=%s, EnfermedadesCronicas=%s,
                        Alergias=%s, HistorialFamiliar=%s, Habitos=%s, EstadoGeneral=%s, 
                        Observaciones=%s, UltimaVisita=%s
                    WHERE idPaciente=%s
                """, (*valores, datetime.now().date(), id_paciente))
            else:
                cursor.execute("""
                    INSERT INTO HistorialMedico (idPaciente, Peso, Altura, GrupoSanguineo, 
                        EnfermedadesCronicas, Alergias, HistorialFamiliar, Habitos, EstadoGeneral, 
                        Observaciones, UltimaVisita)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (id_paciente, *valores, datetime.now().date()))

            db.commit()
            db.close()
            messagebox.showinfo("Éxito", "Historial médico guardado correctamente.")
            nueva_ventana.destroy()
            frame_paciente.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar historial médico: {e}")

    ctk.CTkButton(nueva_ventana, text="Guardar Cambios", command=guardar_cambios,
                  width=200, height=40, font=("Arial", 14)).pack(pady=20)

    cargar_datos()