import os
import smtplib
from fpdf import FPDF
from tkinter import messagebox, simpledialog
from email.message import EmailMessage
import customtkinter as ctk
from tkinter import ttk
from db import conectar_db

def enviar_pdf_por_correo(destinatario, ruta_pdf):
    remitente = 'cutarte0@gmail.com'
    contraseña = 'uvatmxptkzeeuumd'

    mensaje = EmailMessage()
    mensaje['Subject'] = 'VitalApp'
    mensaje['From'] = remitente
    mensaje['To'] = destinatario
    mensaje.set_content('Adjunto se encuentra su documento de tratamientos.')

    with open(ruta_pdf, 'rb') as f:
        mensaje.add_attachment(f.read(), maintype='application', subtype='pdf', filename=os.path.basename(ruta_pdf))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(remitente, contraseña)
            smtp.send_message(mensaje)
        messagebox.showinfo("Éxito", "Correo enviado exitosamente.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo enviar el correo: {e}")

def ver_tratamientos(id_paciente, ventana_anterior):
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")

    ventana = ctk.CTk()
    ventana.title("VitalApp - Tratamientos")
    ventana.geometry("900x600")
    ventana.resizable(False, False)

    ventana_anterior.withdraw()

    def regresar():
        ventana.destroy()
        ventana_anterior.deiconify()

    ctk.CTkLabel(ventana, text="Tratamientos Asignados", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=15)

    boton_regresar = ctk.CTkButton(ventana, text="Regresar", command=regresar, width=200, height=40)
    boton_regresar.pack(pady=10)

    frame = ctk.CTkFrame(ventana)
    frame.pack(fill="both", expand=True, padx=20, pady=10)

    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview", rowheight=30, font=("Arial", 11))
    style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

    tree = ttk.Treeview(frame, columns=("Descripcion", "Medicamentos", "Dosis", "Duracion"), show="headings")
    tree.heading("Descripcion", text="Descripción")
    tree.heading("Medicamentos", text="Medicamentos")
    tree.heading("Dosis", text="Dosis")
    tree.heading("Duracion", text="Duración")

    for col in ("Descripcion", "Medicamentos"):
        tree.column(col, width=250)
    tree.column("Dosis", width=100, anchor="center")
    tree.column("Duracion", width=100, anchor="center")

    tree.pack(fill="both", expand=True, pady=10)

    tratamientos = []

    def generar_pdf():
        if not tratamientos:
            messagebox.showwarning("Advertencia", "No hay tratamientos para exportar.")
            return

        nombre_pdf = simpledialog.askstring("Nombre del archivo", "Ingrese el nombre para el PDF (sin extensión):")
        if not nombre_pdf:
            return

        ruta_pdf = os.path.join(os.path.expanduser("~"), "Downloads", f"{nombre_pdf}.pdf")

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "Tratamientos - VitalApp", ln=True, align="C")
        pdf.ln(10)

        pdf.set_font("Arial", "B", 12)
        headers = ["Descripción", "Medicamentos", "Dosis", "Duración"]
        col_widths = [60, 60, 30, 30]

        for i, header in enumerate(headers):
            pdf.cell(col_widths[i], 10, header, border=1, align="C")
        pdf.ln()

        pdf.set_font("Arial", "", 11)

        def get_max_height(texts, widths):
            return max([max(1, int(pdf.get_string_width(text) / widths[i])) for i, text in enumerate(texts)]) * 8

        for tratamiento in tratamientos:
            row = list(tratamiento)
            height = get_max_height(row, col_widths)
            x, y = pdf.get_x(), pdf.get_y()

            pdf.multi_cell(col_widths[0], 8, row[0], border=1)
            pdf.set_xy(x + col_widths[0], y)
            pdf.multi_cell(col_widths[1], 8, row[1], border=1)
            pdf.set_xy(x + col_widths[0] + col_widths[1], y)
            pdf.multi_cell(col_widths[2], 8, row[2], border=1)
            pdf.set_xy(x + col_widths[0] + col_widths[1] + col_widths[2], y)
            pdf.multi_cell(col_widths[3], 8, row[3], border=1)
            pdf.ln(height - 8)

        try:
            pdf.output(ruta_pdf)
            messagebox.showinfo("Éxito", f"Tratamientos exportados a:\n{ruta_pdf}")
            if messagebox.askyesno("Enviar PDF", "¿Desea enviar el PDF por correo electrónico?"):
                correo = simpledialog.askstring("Correo destino", "Ingrese el correo electrónico de destino:")
                if correo:
                    enviar_pdf_por_correo(correo, ruta_pdf)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el PDF: {e}")

    ctk.CTkButton(ventana, text="Exportar a PDF", command=generar_pdf, width=200, height=40).pack(pady=15)

    try:
        db = conectar_db()
        cursor = db.cursor()
        cursor.execute("""
            SELECT t.Descripcion, t.Medicamentos, t.Dosis, t.Duracion
            FROM Tratamientos t
            INNER JOIN Citas c ON t.idCita = c.idCita
            WHERE c.idPaciente = %s AND c.Estado = 'Realizada'
        """, (id_paciente,))
        tratamientos = cursor.fetchall()
        db.close()

        if tratamientos:
            for tratamiento in tratamientos:
                tree.insert("", "end", values=tratamiento)
        else:
            messagebox.showinfo("Sin Tratamientos", "No tienes tratamientos asignados aún.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al consultar tratamientos: {e}")

    ventana.mainloop()