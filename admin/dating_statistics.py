import customtkinter as ctk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from db import conectar_db

def mostrar_reporte_estadistico(ventana_anterior):
    ctk.set_appearance_mode("dark")  # También puedes usar "dark"
    ctk.set_default_color_theme("dark-blue")

    ventana = ctk.CTkToplevel()
    ventana.title("Reporte Estadístico de Citas por Doctor")
    ventana.geometry("900x600")
    ventana.resizable(True, True)

    # Oculta la ventana anterior mientras esta está abierta
    ventana_anterior.withdraw()

    def regresar():
        ventana.destroy()
        ventana_anterior.deiconify()

    ctk.CTkLabel(
        ventana,
        text="Reporte Estadístico de Citas por Doctor",
        font=ctk.CTkFont(size=22, weight="bold")
    ).pack(pady=20)

        # Botón de regreso
    boton_regresar = ctk.CTkButton(ventana, text="Regresar al Menú", command=regresar)
    boton_regresar.pack(pady=10)

    tabla_frame = ctk.CTkFrame(ventana)
    tabla_frame.pack(fill="both", expand=True, padx=20, pady=10)

    try:
        db = conectar_db()
        cursor = db.cursor()

        cursor.execute("""
            SELECT u.Nombre, e.Nombre_Especialidad,
                SUM(CASE WHEN c.Estado = 'Realizada' THEN 1 ELSE 0 END) AS Realizadas,
                SUM(CASE WHEN c.Estado = 'Pendiente' THEN 1 ELSE 0 END) AS Pendientes,
                SUM(CASE WHEN c.Estado = 'Cancelada' THEN 1 ELSE 0 END) AS Canceladas
            FROM Medicos m
            JOIN Usuarios u ON m.idUsuario = u.idUsuario
            JOIN Especialidad e ON m.idEspecialidad = e.idEspecialidad
            LEFT JOIN Citas c ON m.idMedico = c.idMedico
            GROUP BY u.Nombre, e.Nombre_Especialidad
            ORDER BY u.Nombre
        """)
        datos = cursor.fetchall()
        db.close()

        if not datos:
            messagebox.showinfo("Sin datos", "No hay citas registradas.")
            return

        df = pd.DataFrame(datos, columns=["Doctor", "Especialidad", "Realizadas", "Pendientes", "Canceladas"])
        df[["Realizadas", "Pendientes", "Canceladas"]] = df[["Realizadas", "Pendientes", "Canceladas"]].astype(int)

        # Scrollbars
        scroll_y = ttk.Scrollbar(tabla_frame, orient="vertical")
        scroll_x = ttk.Scrollbar(tabla_frame, orient="horizontal")

        tree = ttk.Treeview(
            tabla_frame,
            columns=list(df.columns),
            show="headings",
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )

        scroll_y.config(command=tree.yview)
        scroll_x.config(command=tree.xview)

        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        tree.pack(fill="both", expand=True)

        # Estilo visual para Treeview
        estilo = ttk.Style()
        estilo.theme_use("default")
        estilo.configure("Treeview",
                         background="#F9F9F9",
                         foreground="black",
                         rowheight=28,
                         font=('Segoe UI', 10))
        estilo.configure("Treeview.Heading",
                         background="#007ACC",
                         foreground="white",
                         font=('Segoe UI', 11, 'bold'))

        for col in df.columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=130)

        for fila in df.itertuples(index=False):
            tree.insert("", "end", values=fila)

        # Función para mostrar gráfica
        def mostrar_grafica():
            fig, ax = plt.subplots(figsize=(10, 6))
            df.set_index("Doctor")[["Realizadas", "Pendientes", "Canceladas"]].plot(kind="bar", ax=ax)
            ax.set_title("Citas por Doctor")
            ax.set_ylabel("Cantidad de Citas")
            ax.set_xlabel("Doctor")
            ax.legend(title="Estado")
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
            plt.show()

        # Botón para mostrar gráfica
        btn_grafica = ctk.CTkButton(
            ventana,
            text="Mostrar Gráfica",
            command=mostrar_grafica,
            font=ctk.CTkFont(size=14)
        )
        btn_grafica.pack(pady=15)

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo generar el reporte: {e}")
        ventana.destroy()