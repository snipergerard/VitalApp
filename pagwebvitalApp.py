import tkinter as tk
from tkinter import messagebox

# Funciones de botones
def agendar():
    messagebox.showinfo("Agendar", "Abrir Agendar Cita")

def historial():
    messagebox.showinfo("Historial Medico", "Abrir Historial Médico")

def crear_cuenta():
    messagebox.showinfo("Crear Cuenta", "Abrir Registro de Cuenta")

def iniciar_sesion():
    messagebox.showinfo("Iniciar Sesion", "Abrir Login")

# Ventana principal
root = tk.Tk()
root.title("VitalApp")
root.geometry("800x600")
root.configure(bg="white")

#  Barrita de navegacion 
navbar = tk.Frame(root, bg="#CDE9F3", height=87)
navbar.pack(fill="x")

logo = tk.Label(navbar, text="VitalApp", bg="#CDE9F3", fg="#057D9F", font=("Jura", 24, "bold"))
logo.pack(side="left", padx=30)

nav_buttons = tk.Frame(navbar, bg="#CDE9F3")
nav_buttons.pack(side="right", padx=40)

btn_agendar = tk.Button(nav_buttons, text="Agendar", font=("Jura", 14), command=agendar, bg="#057D9F", fg="white")
btn_agendar.pack(side="left", padx=10)

btn_historial = tk.Button(nav_buttons, text="Historial Medico", font=("Jura", 14), command=historial, bg="#057D9F", fg="white")
btn_historial.pack(side="left", padx=10)

btn_registro = tk.Button(nav_buttons, text="Crear Cuenta", font=("Jura", 14), command=crear_cuenta, bg="#057D9F", fg="white")
btn_registro.pack(side="left", padx=10)

btn_login = tk.Button(nav_buttons, text="Iniciar Sesión", font=("Jura", 14), command=iniciar_sesion, bg="#057D9F", fg="white")
btn_login.pack(side="left", padx=10)

# === Contenido principal ===
main_content = tk.Frame(root, bg="white")
main_content.pack(expand=True, fill="both")
main_label = tk.Label(main_content, text="Bienvenido a VitalApp", font=("Jura", 20), bg="white", fg="#057D9F")
main_label.pack(pady=50)

# === Pie de pagina ===
footer = tk.Frame(root, bg="#CDE9F3", height=50)
footer.pack(fill="x", side="bottom")

footer_text = tk.Label(footer, text="© 2025 VitalApp — Sobre nosotros | Contacto", bg="#CDE9F3", fg="#057D9F", font=("Jura", 12))
footer_text.pack(pady=10)

root.mainloop()
