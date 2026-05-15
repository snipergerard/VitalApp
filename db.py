import mysql.connector
import hashlib
from mysql.connector import Error

def conectar_db():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",        
            password="", 
            database="vitalapp"
        )
        if conexion.is_connected():
            return conexion
    except Error as e:
        print("Error al conectar a la base de datos:", e)
        return None
    
def calcular_hash_usuario(id_usuario, nombre, correo, id_rol, prev_hash):
    #hash_actual = HCID || nombre || correo || id_rol || prev_hash)
    bloque_data = f"{id_usuario}{nombre}{correo}{id_rol}{prev_hash}"
    return hashlib.sha256(bloque_data.encode()).hexdigest()


def sellar_respaldo_seguro():
    """Esta funcion lo que hace, es respaldar el estado actual integro de los usuarios"""
    db = conectar_db()
    cursor =db.cursor()
    try:
        cursor.execute("DELETE FROM respaldo_usuarios")
        cursor.execute("""
            INSERT INTO respaldo_usuarios (idUsuario, Nombre, Correo, idRol, Contraseña, prev_hash, hash_actual)
            SELECT idUsuario, Nombre, Correo, idRol, Contraseña, prev_hash, hash_actual FROM Usuarios
        """)      
        db.commit()
    except Exception as e:
        print(f"Error al sellar respaldo: {e}")
    finally:
        db.close()
