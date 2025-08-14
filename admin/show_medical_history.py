import customtkinter as ctk
from tkinter import ttk, messagebox
from db import conectar_db

def vista_general_historiales(ventana_anterior):
    ctk.set_appearance_mode("dark")  # o "dark"
    ctk.set_default_color_theme("dark-blue")

    ventana = ctk.CTkToplevel()
    ventana.title("Vista General de Historiales Médicos")
    ventana.geometry("1200x600")
    ventana.resizable(True, True)

    # Oculta la ventana anterior mientras esta está abierta
    ventana_anterior.withdraw()

    def regresar():
        ventana.destroy()
        ventana_anterior.deiconify()


    ctk.CTkLabel(
        ventana, 
        text="Historiales Médicos", 
        font=ctk.CTkFont(size=24, weight="bold")
    ).pack(pady=15)
    
            # Botón de regreso
    boton_regresar = ctk.CTkButton(ventana, text="Regresar al Menú", command=regresar)
    boton_regresar.pack(pady=10)


    frame_tabla = ctk.CTkFrame(ventana)
    frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)

    columnas = [
        "ID", "Nombre", "Peso", "Altura", "Grupo Sanguíneo",
        "Enfermedades", "Alergias", "Historial Familiar",
        "Hábitos", "Estado General", "Observaciones", "Última Visita"
    ]

    # Scrollbars
    scroll_y = ttk.Scrollbar(frame_tabla, orient="vertical")
    scroll_x = ttk.Scrollbar(frame_tabla, orient="horizontal")

    tree = ttk.Treeview(
        frame_tabla,
        columns=columnas,
        show="headings",
        yscrollcommand=scroll_y.set,
        xscrollcommand=scroll_x.set,
        height=20
    )
    scroll_y.config(command=tree.yview)
    scroll_x.config(command=tree.xview)

    scroll_y.pack(side="right", fill="y")
    scroll_x.pack(side="bottom", fill="x")
    tree.pack(fill="both", expand=True)

    # Estilo para Treeview
    estilo = ttk.Style()
    estilo.theme_use("default")
    estilo.configure("Treeview",
                     background="#F5F5F5",
                     foreground="black",
                     rowheight=28,
                     fieldbackground="#F5F5F5",
                     font=('Segoe UI', 10))
    estilo.configure("Treeview.Heading",
                     background="#0078D7",
                     foreground="white",
                     font=('Segoe UI', 11, 'bold'))

    # Definir encabezados
    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=120)

    try:
        db = conectar_db()
        cursor = db.cursor()
        cursor.execute("""
            SELECT p.idPaciente, p.Nombre_Paciente, h.Peso, h.Altura, h.GrupoSanguineo, 
                   h.EnfermedadesCronicas, h.Alergias, h.HistorialFamiliar, h.Habitos,
                   h.EstadoGeneral, h.Observaciones, h.UltimaVisita
            FROM HistorialMedico h
            JOIN Pacientes p ON h.idPaciente = p.idPaciente
            ORDER BY p.Nombre_Paciente
        """)
        historiales = cursor.fetchall()
        db.close()

        if not historiales:
            messagebox.showinfo("Sin datos", "No hay historiales médicos registrados.")
            ventana.destroy()
            return

        for fila in historiales:
            tree.insert("", "end", values=fila)

    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar los historiales médicos:\n{e}")
        ventana.destroy()
