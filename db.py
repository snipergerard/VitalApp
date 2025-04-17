import mysql.connector
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