import customtkinter as ctk
from tkinter import messagebox
import hashlib
import sys 
import os
ruta_actual = os.path.dirname(os.path.abspath(__file__))
ruta_padre = os.path.dirname(ruta_actual)
if ruta_padre not in sys.path:
    sys.path.append(ruta_padre)

from db import conectar_db, calcular_hash_usuario

ventana_actual = None

def abrir_nueva_ventana(func):
    global ventana_actual
    if ventana_actual is not None:
        ventana_actual.destroy()
    ventana_actual = func()

def volver_al_menu(ventana):
    global ventana_actual
    ventana.destroy()
    ventana_actual = None
    gestionar_usuarios(ventana_anterior=None)

# --- FUNCIÓN AUXILIAR DE RECONSTRUCCIÓN (LA CLAVE DEL ÉXITO) ---
def resincronizar_cadena_desde(id_inicio, db, cursor):
    """Recalcula todos los hashes desde un ID específico hasta el último registro."""
    # 1. Obtener el hash del usuario inmediatamente anterior para el encadenamiento
    cursor.execute("SELECT hash_actual FROM Usuarios WHERE idUsuario < %s ORDER BY idUsuario DESC LIMIT 1", (id_inicio,))
    res = cursor.fetchone()
    hash_anterior = res[0] if res else "0"

    # 2. Obtener todos los registros desde el punto de conflicto hacia adelante
    cursor.execute("SELECT idUsuario, Nombre, Correo, idRol FROM Usuarios WHERE idUsuario >= %s ORDER BY idUsuario ASC", (id_inicio,))
    usuarios = cursor.fetchall()

    for u in usuarios:
        # u[0]=idUsuario, u[1]=Nombre, u[2]=Correo, u[3]=idRol
        nuevo_hash = calcular_hash_usuario(u[0], u[1], u[2], u[3], hash_anterior)
        cursor.execute("UPDATE Usuarios SET prev_hash=%s, hash_actual=%s WHERE idUsuario=%s", 
                       (hash_anterior, nuevo_hash, u[0]))
        hash_anterior = nuevo_hash
    db.commit()

# --- AUDITORÍA E INTEGRIDAD ---
def auditar_usuarios():
    try:
        db = conectar_db()
        cursor = db.cursor() # Usamos cursor normal para consistencia con tu código
        cursor.execute("SELECT idUsuario, Nombre, Correo, idRol, prev_hash, hash_actual FROM Usuarios ORDER BY idUsuario ASC")
        registros = cursor.fetchall()
        
        hash_anterior_esperado = "0"
        
        for reg in registros:
            id_u, nombre, correo, rol, p_hash, h_actual = reg
            
            if p_hash != hash_anterior_esperado:
                intentar_reparar(id_u, f"Falla en eslabón. Se esperaba conexión con {hash_anterior_esperado[:10]}...")
                return

            hash_recalculado = calcular_hash_usuario(id_u, nombre, correo, rol, p_hash)
            
            if hash_recalculado != h_actual:
                intentar_reparar(id_u, f"La firma digital no coincide con los datos actuales.")
                return
            
            hash_anterior_esperado = h_actual
            
        messagebox.showinfo("Integridad OK", "✅ La Blockchain es íntegra.\nSe ha actualizado el sello de respaldo.")
        from db import sellar_respaldo_seguro
        sellar_respaldo_seguro() 
        db.close()
    except Exception as e:
        messagebox.showerror("Error", f"Fallo en auditoría: {e}")

def intentar_reparar(id_usuario, motivo):
    ventana_alerta = ctk.CTkToplevel()
    ventana_alerta.title("CENTRO DE RECUPERACIÓN - VitalApp")
    ventana_alerta.geometry("450x320")
    ventana_alerta.attributes("-topmost", True)

    ctk.CTkLabel(ventana_alerta, text="⚠️", font=("Helvetica", 60)).pack(pady=10)
    ctk.CTkLabel(ventana_alerta, text="SISTEMA COMPROMETIDO", 
                 font=("Helvetica", 18, "bold"), text_color="#e74c3c").pack(pady=5)
    ctk.CTkLabel(ventana_alerta, text=f"Usuario afectado: ID {id_usuario}\n{motivo}", 
                 font=("Helvetica", 13), wraplength=400).pack(pady=10)

    frame_botones = ctk.CTkFrame(ventana_alerta, fg_color="transparent")
    frame_botones.pack(pady=20)

    def ejecutar_restauracion():
        try:
            db = conectar_db()
            cursor = db.cursor()
            # 1. Recuperar datos originales de la bóveda (idUsuario, Nombre, Correo, idRol, Contraseña)
            cursor.execute("SELECT Nombre, Correo, idRol, Contraseña FROM respaldo_usuarios WHERE idUsuario = %s", (id_usuario,))
            res = cursor.fetchone()
            
            if res:
                # 2. Restaurar datos base en la tabla principal
                cursor.execute("""
                    UPDATE Usuarios SET Nombre=%s, Correo=%s, idRol=%s, Contraseña=%s 
                    WHERE idUsuario=%s
                """, (res[0], res[1], res[2], res[3], id_usuario))
                
                # 3. RE-SELLAR LA BLOCKCHAIN COMPLETA DESDE EL ERROR
                resincronizar_cadena_desde(id_usuario, db, cursor)
                
                db.close()
                ventana_alerta.destroy()
                messagebox.showinfo("Éxito", "✅ Sistema sanado y Blockchain reconstruida.")
            else:
                messagebox.showerror("Error", "No hay respaldo disponible para este ID.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo reparar: {e}")

    btn_reparar = ctk.CTkButton(frame_botones, text="AUTORREPARAR", fg_color="#27ae60", command=ejecutar_restauracion)
    btn_reparar.pack(side="left", padx=10)
    ctk.CTkButton(frame_botones, text="IGNORAR", fg_color="#7f8c8d", command=ventana_alerta.destroy).pack(side="left", padx=10)

def gestionar_usuarios(ventana_anterior):
    if ventana_anterior is not None:
        ventana_anterior.withdraw()
    ventana = ctk.CTkToplevel()
    ventana.title("Gestión de Seguridad")
    ventana.geometry("400x600")

    def iniciar_auditoria():
        btn_auditar.configure(text="🔍 ANALIZANDO...", state="disabled", fg_color="#f39c12")
        ventana.update()
        auditar_usuarios()
        btn_auditar.configure(text="AUDITAR INTEGRIDAD (Blockchain)", state="normal", fg_color="#27ae60")

    btn_regresar = ctk.CTkButton(ventana, text="Volver al menú", command=lambda: (ventana.destroy(), ventana_anterior.deiconify() if ventana_anterior else None))
    btn_regresar.pack(pady=10)

    btn_auditar = ctk.CTkButton(ventana, text="AUDITAR INTEGRIDAD (Blockchain)", command=iniciar_auditoria, fg_color="#27ae60", height=45)
    btn_auditar.pack(pady=10, fill="x", padx=40)

    # ... Resto de botones de visualización (Doctores, Admins, Pacientes)
    ctk.CTkButton(ventana, text="Ver Médicos", command=lambda: abrir_nueva_ventana(mostrar_doctores)).pack(pady=5, fill="x", padx=40)
    ctk.CTkButton(ventana, text="Ver Administradores", command=lambda: abrir_nueva_ventana(mostrar_administradores)).pack(pady=5, fill="x", padx=40)
    ctk.CTkButton(ventana, text="Ver Pacientes", command=lambda: abrir_nueva_ventana(mostrar_pacientes)).pack(pady=5, fill="x", padx=40)
    
    ctk.CTkLabel(ventana, text="--- Alta ---", font=("Helvetica", 12, "italic")).pack(pady=5)
    ctk.CTkButton(ventana, text="Registrar Admin", command=lambda: abrir_nueva_ventana(crear_administrador)).pack(pady=5, fill="x", padx=40)
    ctk.CTkButton(ventana, text="Registrar Médico", command=lambda: abrir_nueva_ventana(crear_medico)).pack(pady=5, fill="x", padx=40)

    return ventana

# --- MODIFICAR USUARIO (CON RE-SELLADO DE BLOCKCHAIN) ---
def modificar_individual_doctor(correo, especialidad):
    # ... (Aquí va tu lógica de interfaz para capturar nuevo_nombre y nuevo_telefono)
    # Al final, en guardar_cambios:
    def guardar_cambios():
        try:
            db = conectar_db()
            cursor = db.cursor()
            # 1. Hacer el UPDATE
            cursor.execute("UPDATE Usuarios SET Nombre=%s WHERE Correo=%s", (nuevo_nombre, correo))
            
            # 2. Obtener el ID para re-sellado
            cursor.execute("SELECT idUsuario FROM Usuarios WHERE Correo=%s", (correo,))
            id_u = cursor.fetchone()[0]
            
            # 3. RE-SELLAR LA BLOCKCHAIN PARA QUE EL CAMBIO SEA LEGÍTIMO
            resincronizar_cadena_desde(id_u, db, cursor)
            
            db.close()
            messagebox.showinfo("Éxito", "Doctor actualizado y Blockchain re-sellada.")
        except Exception as e: messagebox.showerror("Error", str(e))

def crear_administrador():
    ventana = ctk.CTkToplevel()
    ventana.title("Nuevo Administrador")
    ventana.geometry("400x450")

    ctk.CTkButton(ventana, text="Volver al Menú", command=lambda: volver_al_menu(ventana)).pack(pady=10)

    ctk.CTkLabel(ventana, text="Nombre:").pack(pady=5)
    entrada_nombre = ctk.CTkEntry(ventana)
    entrada_nombre.pack(pady=5)

    ctk.CTkLabel(ventana, text="Correo:").pack(pady=5)
    entrada_correo = ctk.CTkEntry(ventana)
    entrada_correo.pack(pady=5)

    ctk.CTkLabel(ventana, text="Contraseña:").pack(pady=5)
    entrada_contra = ctk.CTkEntry(ventana, show="*")
    entrada_contra.pack(pady=5)

    def guardar_admin():
        nombre = entrada_nombre.get()
        correo = entrada_correo.get()
        contra = entrada_contra.get()

        try:
            db = conectar_db()
            cursor = db.cursor()

            # 1. CIFRADO: Hashear la contraseña del Admin
            contra_hasheada = hashlib.sha256(contra.encode()).hexdigest()

            # LÓGICA BLOCKCHAIN: Obtener el último hash
            cursor.execute("SELECT hash_actual FROM Usuarios ORDER BY idUsuario DESC LIMIT 1")
            res = cursor.fetchone()
            prev_hash = res[0] if res else "0"

            # Inserción con la contraseña ya cifrada
            cursor.execute("""
                INSERT INTO Usuarios (Nombre, Correo, Contraseña, idRol, prev_hash, hash_actual)
                VALUES (%s, %s, %s, 1, %s, '0')
            """, (nombre, correo, contra_hasheada, prev_hash))
            
            id_usuario = cursor.lastrowid
            h_actual = calcular_hash_usuario(id_usuario, nombre, correo, 1, prev_hash)
            
            cursor.execute("UPDATE Usuarios SET hash_actual=%s WHERE idUsuario=%s", (h_actual, id_usuario))

            db.commit()
            db.close()
            messagebox.showinfo("Éxito", f"Administrador creado.\nHash: {h_actual[:15]}...")
            ventana.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear el administrador: {e}")

    ctk.CTkButton(ventana, text="Guardar", command=guardar_admin).pack(pady=20)
    global ventana_actual
    ventana_actual = ventana
    return ventana

def crear_medico():
    ventana = ctk.CTkToplevel()
    ventana.title("Nuevo Médico")
    ventana.geometry("400x600")

    ctk.CTkButton(ventana, text="Volver al Menú", command=lambda: volver_al_menu(ventana)).pack(pady=5)

    ctk.CTkLabel(ventana, text="Nombre:").pack(pady=5)
    entrada_nombre = ctk.CTkEntry(ventana)
    entrada_nombre.pack(pady=5)

    ctk.CTkLabel(ventana, text="Correo:").pack(pady=5)
    entrada_correo = ctk.CTkEntry(ventana)
    entrada_correo.pack(pady=5)

    ctk.CTkLabel(ventana, text="Contraseña:").pack(pady=5)
    entrada_contra = ctk.CTkEntry(ventana, show="*")
    entrada_contra.pack(pady=5)

    ctk.CTkLabel(ventana, text="Teléfono:").pack(pady=5)
    entrada_telefono = ctk.CTkEntry(ventana)
    entrada_telefono.pack(pady=5)

    # Carga de especialidades
    try:
        db = conectar_db()
        cursor = db.cursor()
        cursor.execute("SELECT idEspecialidad, Nombre_Especialidad FROM Especialidad")
        especialidades = cursor.fetchall()
        db.close()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar especialidades: {e}")
        ventana.destroy()
        return

    especialidades_dict = {nombre: id_ for id_, nombre in especialidades}
    nombres_especialidades = list(especialidades_dict.keys())
    especialidad_var = ctk.StringVar(value=nombres_especialidades[0])

    ctk.CTkLabel(ventana, text="Especialidad:").pack(pady=5)
    ctk.CTkOptionMenu(ventana, variable=especialidad_var, values=nombres_especialidades).pack(pady=5)

    def guardar_medico():
        nombre = entrada_nombre.get()
        correo = entrada_correo.get()
        contra = entrada_contra.get()
        telefono = entrada_telefono.get()
        especialidad_id = especialidades_dict[especialidad_var.get()]

        try:
            db = conectar_db()
            cursor = db.cursor()

            # 1. CIFRADO: Hashear la contraseña del Médico
            contra_hasheada = hashlib.sha256(contra.encode()).hexdigest()

            # LÓGICA BLOCKCHAIN: Obtener el último hash
            cursor.execute("SELECT hash_actual FROM Usuarios ORDER BY idUsuario DESC LIMIT 1")
            res = cursor.fetchone()
            prev_hash = res[0] if res else "0"

            # Insertar en Usuarios con la contraseña ya cifrada
            cursor.execute("""
                INSERT INTO Usuarios (Nombre, Correo, Contraseña, idRol, prev_hash, hash_actual)
                VALUES (%s, %s, %s, 2, %s, '0')
            """, (nombre, correo, contra_hasheada, prev_hash))

            id_usuario = cursor.lastrowid
            h_actual = calcular_hash_usuario(id_usuario, nombre, correo, 2, prev_hash)
            cursor.execute("UPDATE Usuarios SET hash_actual=%s WHERE idUsuario=%s", (h_actual, id_usuario))

            # Insertar en Médicos
            cursor.execute("""
                INSERT INTO Medicos (idEspecialidad, idUsuario, Nombre_medico, Telefono, Correo)
                VALUES (%s, %s, %s, %s, %s)
            """, (especialidad_id, id_usuario, nombre, telefono, correo))

            db.commit()
            db.close()
            messagebox.showinfo("Éxito", f"Médico creado.\nHash: {h_actual[:15]}...")
            ventana.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear el médico: {e}")

    ctk.CTkButton(ventana, text="Guardar", command=guardar_medico).pack(pady=20)
    global ventana_actual
    ventana_actual = ventana
    return ventana

# --- LAS FUNCIONES DE MOSTRAR Y MODIFICAR SE MANTIENEN IGUAL ---
# (Omitidas por brevedad pero deben estar en tu archivo)
def mostrar_doctores():
    ventana = ctk.CTkToplevel()
    ventana.title("Doctores Registrados")
    ventana.geometry("600x500")
    
    # ESTO HACE QUE APAREZCA AL FRENTE
    ventana.lift()
    ventana.focus_force()
    ventana.attributes("-topmost", True) # Opcional: la mantiene siempre arriba

    ctk.CTkButton(ventana, text="Volver al Menú", command=lambda: volver_al_menu(ventana)).pack(pady=5)
    
    try:
        db = conectar_db()
        cursor = db.cursor()
        cursor.execute("""
            SELECT u.idUsuario, u.Nombre, u.Correo, m.Telefono, e.Nombre_Especialidad 
            FROM Usuarios u 
            JOIN Medicos m ON u.idUsuario = m.idUsuario 
            JOIN Especialidad e ON m.idEspecialidad = e.idEspecialidad 
            WHERE u.idRol = 2
        """)
        doctores = cursor.fetchall()
        db.close()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron obtener los doctores: {e}")
        return

    for id_u, nombre, correo, telefono, especialidad in doctores:
        frame = ctk.CTkFrame(ventana)
        frame.pack(pady=8, padx=15, fill="x")
        label_info = ctk.CTkLabel(frame, text=f"{nombre} | {correo}")
        label_info.pack(side="left", padx=5)
        
        # Pasamos el ID del usuario para poder re-sellar la cadena después
        btn = ctk.CTkButton(frame, text="Modificar", width=80, 
                             command=lambda i=id_u, c=correo: modificar_individual_doctor(i, c))
        btn.pack(side="right", padx=5)
def modificar_individual_doctor(id_usuario, nombre_actual, correo):
    ventana = ctk.CTkToplevel()
    ventana.title("Modificar Datos del Doctor")
    ventana.geometry("400x350")
    
    ventana.lift()
    ventana.focus_force()
    ventana.attributes("-topmost", True)

    ctk.CTkLabel(ventana, text="Doctor:", font=("Helvetica", 12, "bold")).pack(pady=(20, 0))
    ctk.CTkLabel(ventana, text=nombre_actual, text_color="gray").pack(pady=(0, 10))

    ctk.CTkLabel(ventana, text="Nuevo Nombre:").pack(pady=5)
    ent_nombre = ctk.CTkEntry(ventana)
    ent_nombre.pack(pady=5)

    def guardar():
        try:
            db = conectar_db()
            cursor = db.cursor()
            # Actualizar en Usuarios y en Médicos (por si acaso el nombre se replica)
            cursor.execute("UPDATE Usuarios SET Nombre=%s WHERE idUsuario=%s", (ent_nombre.get(), id_usuario))
            cursor.execute("UPDATE Medicos SET Nombre_medico=%s WHERE idUsuario=%s", (ent_nombre.get(), id_usuario))
            
            resincronizar_cadena_desde(id_usuario, db, cursor)
            
            db.close()
            messagebox.showinfo("Éxito", "Datos del médico actualizados correctamente.")
            ventana.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    ctk.CTkButton(ventana, text="Confirmar", command=guardar).pack(pady=20)

def mostrar_administradores():
    ventana_validacion = ctk.CTkToplevel()
    ventana_validacion.title("Validar Acceso")
    ventana_validacion.geometry("300x200")
    ventana_validacion.lift()
    ventana_validacion.focus_force()
    ventana_validacion.attributes("-topmost", True)

    ctk.CTkLabel(ventana_validacion, text="Contraseña de Seguridad:").pack(pady=10)
    entrada_contra = ctk.CTkEntry(ventana_validacion, show="*")
    entrada_contra.pack(pady=10)

    def validar_y_abrir():
        if entrada_contra.get() != "MAYORADMIN":
            messagebox.showerror("Error", "Acceso denegado")
            return
        
        ventana_validacion.destroy()
        ventana_lista = ctk.CTkToplevel()
        ventana_lista.title("Lista de Administradores")
        ventana_lista.geometry("500x400")
        ventana_lista.lift()
        ventana_lista.focus_force()

        try:
            db = conectar_db()
            cursor = db.cursor()
            # IMPORTANTE: Traemos el idUsuario para la Blockchain
            cursor.execute("SELECT idUsuario, Nombre, Correo FROM Usuarios WHERE idRol = 1")
            admins = cursor.fetchall()
            db.close()

            for id_u, nombre, correo in admins:
                frame = ctk.CTkFrame(ventana_lista)
                frame.pack(pady=5, padx=10, fill="x")
                ctk.CTkLabel(frame, text=f"{nombre} ({correo})").pack(side="left", padx=10)
                # Pasamos id_u a la función de modificar
                ctk.CTkButton(frame, text="Editar", width=70, 
                             command=lambda i=id_u, n=nombre: modificar_admin(i, n)).pack(side="right", padx=10)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    ctk.CTkButton(ventana_validacion, text="Entrar", command=validar_y_abrir).pack(pady=10)

def modificar_admin(id_usuario, nombre_actual):
    ventana = ctk.CTkToplevel()
    ventana.title("Editar Administrador")
    ventana.geometry("400x300")
    
    # --- MEJORA: Ventana al frente y enfocada ---
    ventana.lift()
    ventana.focus_force()
    ventana.attributes("-topmost", True)

    # --- MEJORA: Mostrar nombre actual ---
    ctk.CTkLabel(ventana, text="Nombre Actual:", font=("Helvetica", 12, "bold")).pack(pady=(20, 0))
    ctk.CTkLabel(ventana, text=nombre_actual, text_color="gray").pack(pady=(0, 10))

    ctk.CTkLabel(ventana, text="Nuevo Nombre:").pack(pady=5)
    entrada_nombre = ctk.CTkEntry(ventana, placeholder_text="Escriba el nuevo nombre...")
    entrada_nombre.pack(pady=10)

    def guardar():
        nuevo_nom = entrada_nombre.get()
        if not nuevo_nom: return
        try:
            db = conectar_db()
            cursor = db.cursor()
            cursor.execute("UPDATE Usuarios SET Nombre=%s WHERE idUsuario=%s", (nuevo_nom, id_usuario))
            
            # Re-sellado para mantener la Blockchain intacta
            resincronizar_cadena_desde(id_usuario, db, cursor)
            
            db.close()
            messagebox.showinfo("Éxito", "Administrador actualizado y Blockchain sincronizada.")
            ventana.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo modificar: {e}")

    ctk.CTkButton(ventana, text="Guardar Cambios", command=guardar, fg_color="#27ae60").pack(pady=20)

def mostrar_pacientes():
    ventana = ctk.CTkToplevel()
    ventana.title("Expediente de Pacientes")
    ventana.geometry("600x500")
    ventana.lift()
    ventana.focus_force()

    try:
        db = conectar_db()
        cursor = db.cursor()
        # Unimos Usuarios y Pacientes para tener el ID de la cadena
        cursor.execute("""
            SELECT u.idUsuario, u.Nombre, p.Telefono, p.Direccion 
            FROM Usuarios u 
            JOIN Pacientes p ON u.Correo = p.Correo 
            WHERE u.idRol = 3
        """)
        pacientes = cursor.fetchall()
        db.close()

        for id_u, nombre, tel, dir_ in pacientes:
            frame = ctk.CTkFrame(ventana)
            frame.pack(pady=5, padx=10, fill="x")
            ctk.CTkLabel(frame, text=f"{nombre} | {tel}").pack(side="left", padx=10)
            ctk.CTkButton(frame, text="Modificar", 
                         command=lambda i=id_u: modificar_individual_paciente(i)).pack(side="right", padx=10)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def modificar_individual_paciente(id_usuario, nombre_actual):
    ventana = ctk.CTkToplevel()
    ventana.title("Editar Expediente de Paciente")
    ventana.geometry("400x450")
    
    ventana.lift()
    ventana.focus_force()
    ventana.attributes("-topmost", True)

    ctk.CTkLabel(ventana, text="Paciente Actual:", font=("Helvetica", 12, "bold")).pack(pady=(20, 0))
    ctk.CTkLabel(ventana, text=nombre_actual, text_color="gray").pack(pady=(0, 10))

    ctk.CTkLabel(ventana, text="Nuevo Nombre:").pack(pady=2)
    ent_nom = ctk.CTkEntry(ventana); ent_nom.pack(pady=5)
    
    ctk.CTkLabel(ventana, text="Nuevo Teléfono:").pack(pady=2)
    ent_tel = ctk.CTkEntry(ventana); ent_tel.pack(pady=5)

    def guardar():
        try:
            db = conectar_db()
            cursor = db.cursor()
            
            # Actualizamos la tabla base de la Blockchain
            cursor.execute("UPDATE Usuarios SET Nombre=%s WHERE idUsuario=%s", (ent_nom.get(), id_usuario))
            
            # Actualizamos la tabla de detalles (Pacientes)
            cursor.execute("UPDATE Pacientes SET Nombre_Paciente=%s, Telefono=%s WHERE idUsuario=%s", 
                           (ent_nom.get(), ent_tel.get(), id_usuario))

            resincronizar_cadena_desde(id_usuario, db, cursor)
            
            db.close()
            messagebox.showinfo("Éxito", "Expediente actualizado y Blockchain re-sellada.")
            ventana.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    ctk.CTkButton(ventana, text="Guardar Cambios", command=guardar).pack(pady=20)
