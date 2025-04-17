from tkinter import *
from tkinter import messagebox
from authenticator.login import abrir_login
from admin.admin_view import abrir_admin
from doctor.doctor_view import abrir_doctor
from patient.patient_view import abrir_patient
from authenticator.register import abrir_registro


def callback_por_rol(rol):
   

    if rol == 1:
        abrir_admin()  
    elif rol == 2:
        abrir_doctor()  
    elif rol == 3:
        abrir_patient()  
    else:
        messagebox.showerror("Error", "Rol no válido.")  # Manejo de error en caso de un rol que no exista 

# Función para abrir la pantalla de login
def abrir_main():
  
    def mostrar_login():
        abrir_login(callback_por_rol)

    
    ventana = Tk()
    ventana.title("VitalApp")

    Label(ventana, text="Bienvenido a VitalApp", font=("Arial", 18)).pack(pady=20)
    Button(ventana, text="Iniciar Sesión", command=mostrar_login, width=20).pack(pady=10)
    Button(ventana, text="Crear Cuenta (Paciente)", command=abrir_registro, width=20).pack(pady=10)

    ventana.mainloop()

if __name__ == "__main__":
    abrir_main()
