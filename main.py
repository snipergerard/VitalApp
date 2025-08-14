from tkinter import *
from tkinter import messagebox
from authenticator.login import abrir_login
#from admin.admin_view import abrir_admin
#from doctor.doctor_view import abrir_doctor, obtener_id_medico
#from patient.patient_view import abrir_patient, obtener_datos_paciente
from authenticator.register import abrir_registro
from PIL import Image, ImageTk 

# Lógica de redirección según el rol
def callback_por_rol(rol, id_usuario):
    if rol == 1:
        from admin.admin_view import abrir_admin
        abrir_admin(id_usuario)
    elif rol == 2:
        from doctor.doctor_view import abrir_doctor, obtener_id_medico
        id_medico = obtener_id_medico(id_usuario)
        abrir_doctor(id_medico)
    elif rol == 3:
        from patient.patient_view import abrir_patient, obtener_datos_paciente
        id_paciente, nombre_paciente = obtener_datos_paciente(id_usuario)
        if id_paciente and nombre_paciente:
            abrir_patient(id_paciente, nombre_paciente)
        else:
            messagebox.showerror("Error", "No se encontró el paciente.")
    else:
        messagebox.showerror("Error", "Rol no válido.")

# Clase para la ventana principal
class VentanaPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("VitalApp")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f4f7")
        self.setup_ui()

    def setup_ui(self):
        frame = Frame(self.root, bg="#f0f4f7")
        frame.place(relx=0.5, rely=0.3, anchor=CENTER)

        imagen = Image.open(r"C:\Users\gerar\Downloads\VitalApp-main\VitalApp-main\Logo.png")
        imagen = imagen.resize((200, 200))
        self.imagen_tk = ImageTk.PhotoImage(imagen) 

        Label(frame, image=self.imagen_tk, bg="#f0f4f7").pack(pady=10)

        Label(
            frame,
            text="Bienvenido a VitalApp",
            font=("Helvetica", 20, "bold"),
            bg="#f0f4f7",
            fg="#2c3e50"
        ).pack(pady=30)

        Button(
            frame,
            text="Iniciar Sesión",
            command=self.mostrar_login,
            font=("Helvetica", 12),
            width=25,
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            relief="flat",
            pady=5
        ).pack(pady=10)

        Button(
            frame,  
            text="Crear Cuenta (Paciente)",
            command=self.mostrar_registro,
            font=("Jura", 12),
            width=25,
            bg="#2ecc71",
            fg="white",
            activebackground="#27ae60",
            relief="flat",
            pady=5
        ).pack(pady=10)

    def mostrar_login(self):
        self.root.destroy()
        abrir_login(callback_por_rol)

    def mostrar_registro(self):
        self.root.destroy()
        abrir_registro()


# ✅ FUNCIÓN GLOBAL que puede llamarse desde otros módulos (como admin_view)
def lanzar_vitalapp():
    root = Tk()
    app = VentanaPrincipal(root)
    root.mainloop()


# Punto de entrada
if __name__ == "__main__":
    lanzar_vitalapp()