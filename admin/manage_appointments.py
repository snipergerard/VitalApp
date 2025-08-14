import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk
from db import conectar_db

def mostrar_citas(ventana_anterior):  # <-- ahora recibe la ventana anterior
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    
    ventana = ctk.CTkToplevel()
    ventana.title("Citas Pendientes")
    ventana.geometry("700x500")
    ventana.configure(fg_color="#f2f2f2")

    # Oculta la ventana anterior mientras esta está abierta
    ventana_anterior.withdraw()

    def regresar():
        ventana.destroy()
        ventana_anterior.deiconify()

    titulo = ctk.CTkLabel(ventana, text="Citas Pendientes", font=("Arial", 24, "bold"), text_color="#333333")
    titulo.pack(pady=20)

    # Botón de regreso
    boton_regresar = ctk.CTkButton(ventana, text="Regresar al Menú", command=regresar)
    boton_regresar.pack(pady=10)

    frame_tabla = ctk.CTkFrame(ventana, fg_color="white", corner_radius=10)
    frame_tabla.pack(expand=True, fill="both", padx=20, pady=10)

    columnas = ("id", "fecha", "paciente", "medico", "motivo", "estado")
    tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", style="Custom.Treeview")

    encabezados = {
        "id": "ID",
        "fecha": "Fecha",
        "paciente": "Paciente",
        "medico": "Médico",
        "motivo": "Motivo de Consulta",
        "estado": "Estado"
    }

    for col in columnas:
        tabla.heading(col, text=encabezados[col])
        tabla.column(col, anchor="center", width=140)

    scrollbar_y = ctk.CTkScrollbar(frame_tabla, orientation="vertical", command=tabla.yview)
    scrollbar_x = ctk.CTkScrollbar(frame_tabla, orientation="horizontal", command=tabla.xview)
    tabla.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

    tabla.pack(expand=True, fill="both", side="left")
    scrollbar_y.pack(side="right", fill="y")
    scrollbar_x.pack(side="bottom", fill="x")

    estilo = ttk.Style()
    estilo.theme_use("default")
    estilo.configure("Custom.Treeview",
                     background="white",
                     foreground="black",
                     rowheight=30,
                     fieldbackground="white",
                     font=("Arial", 12))
    estilo.configure("Custom.Treeview.Heading", font=("Arial", 14, "bold"), background="#0066cc", foreground="white")

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
        return