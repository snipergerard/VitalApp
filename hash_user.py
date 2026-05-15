import hashlib
import sys
import os

# Asegurar que encuentre db.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from db import conectar_db

def actualizar_contrasenas_existentes():
    try:
        db = conectar_db()
        cursor = db.cursor()
        
        # Obtenemos ID y la contraseña actual (texto plano)
        cursor.execute("SELECT idUsuario, Contraseña FROM Usuarios")
        usuarios = cursor.fetchall()
        
        for id_u, contra_plana in usuarios:
            # Si la contra ya parece un hash (64 caracteres), la saltamos para no re-hashear
            if len(contra_plana) == 64:
                continue
                
            # Crear el hash
            hash_contra = hashlib.sha256(contra_plana.encode()).hexdigest()
            
            # Actualizar
            cursor.execute("UPDATE Usuarios SET Contraseña = %s WHERE idUsuario = %s", (hash_contra, id_u))
            print(f"Contraseña de Usuario ID {id_u} protegida.")
            
        db.commit()
        db.close()
        print("\n✅ Todas las contraseñas existentes han sido cifradas.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    actualizar_contrasenas_existentes()
