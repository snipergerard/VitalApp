import tkinter as tk

def guardar_datos():
    datos = {
        
        "Enfermedades cronicas": entrada_enfermedades.get(),
        "Habitos": entrada_habitos.get(),
        "Historial de consultas": entrada_historial.get("1.0", "end").strip(),
        "Peso": entrada_peso.get(),
        "Altura": entrada_altura.get()
    }

    print("\n===== HISTORIAL MÉDICO GUARDADO =====")
    for campo, valor in datos.items():
        print(f"{campo}: {valor}")
    print("======================================")

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Formulario Historial Médico")
ventana.geometry("600x700")
ventana.configure(padx=20, pady=20)

# Función para crear filas de etiqueta + entrada
def crear_entrada(fila, texto, ancho=40):
    etiqueta = tk.Label(ventana, text=texto, anchor="w")
    etiqueta.grid(row=fila, column=0, sticky="w", pady=4)
    entrada = tk.Entry(ventana, width=ancho)
    entrada.grid(row=fila, column=1, pady=4)
    return entrada

# Crear campos
entrada_nombre = crear_entrada(0, "Nombre completo:")
entrada_fecha = crear_entrada(1, "Fecha de nacimiento:")
entrada_sexo = crear_entrada(2, "Sexo:")
entrada_direccion = crear_entrada(3, "Direccion:")
entrada_telefono = crear_entrada(4, "Telefono:")
entrada_enfermedades = crear_entrada(5, "Enfermedades cronicas:")
entrada_habitos = crear_entrada(6, "Habitos (tabaquismo, dieta, etc.):")

# Historial de consultas (cuadro de texto grande)
tk.Label(ventana, text="Historial de consultas previas:", anchor="w").grid(row=7, column=0, sticky="nw", pady=4)
entrada_historial = tk.Text(ventana, width=45, height=5)
entrada_historial.grid(row=7, column=1, pady=4)

entrada_peso = crear_entrada(8, "Peso (kg):")
entrada_altura = crear_entrada(9, "Altura (cm):")

# Boton para guardar
boton_guardar = tk.Button(ventana, text="Guardar datos", command=guardar_datos, bg="#4CAF50", fg="white")
boton_guardar.grid(row=10, column=0, columnspan=2, pady=20)

ventana.mainloop()
