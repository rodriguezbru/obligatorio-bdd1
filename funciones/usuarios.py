
import hashlib
import mysql.connector
from getpass import getpass
from database import conectar


def iniciar_sesion():
    print("\n===== INICIAR SESIÓN =====")

    correo = input("Correo: ")
    contrasena = getpass("Contraseña: ")

    contrasena_hash = hashlib.sha256(
        contrasena.encode("utf-8")
    ).hexdigest()

    conexion = None
    cursor = None

    try:
        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT rol
            FROM login
            WHERE correo = %s
              AND contrasena = %s
        """, (correo, contrasena_hash))

        usuario = cursor.fetchone()

        if usuario is None:
            print("Correo o contraseña incorrectos.")
            return None

        print("Inicio de sesión correcto.")
        return usuario[0]

    except mysql.connector.Error as error:
        print("Error de conexión con MySQL:", error)
        return None

    finally:
        if cursor is not None:
            cursor.close()

        if conexion is not None:
            conexion.close()
