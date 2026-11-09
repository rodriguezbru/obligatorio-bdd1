
import mysql.connector
from getpass import getpass


rol_actual = None
contrasenas_mysql = {}


def conectar():
    if rol_actual == "administrador":
        usuario = "admin_torneo"

    elif rol_actual == "planillero":
        usuario = "planillero_torneo"

    else:
        usuario = "consulta_torneo"

    if usuario not in contrasenas_mysql:
        contrasenas_mysql[usuario] = getpass(
            "Contraseña MySQL de " + usuario + ": "
        )

    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user=usuario,
            password=contrasenas_mysql[usuario],
            database="torneo_ucu"
        )

        return conexion

    except mysql.connector.Error:
        contrasenas_mysql.pop(usuario, None)
        raise


def cambiar_rol(nuevo_rol):
    global rol_actual

    if nuevo_rol not in ("administrador", "planillero"):
        return False

    rol_anterior = rol_actual
    rol_actual = nuevo_rol

    try:
        conexion = conectar()
        conexion.close()
        return True

    except mysql.connector.Error as error:
        print("No se pudo conectar con los permisos del rol:", error)
        rol_actual = rol_anterior
        return False


def cerrar_sesion():
    global rol_actual
    rol_actual = None
