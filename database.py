
import mysql.connector
import os
from getpass import getpass


def conectar():
    if "MYSQL_PASSWORD" not in os.environ:
        os.environ["MYSQL_PASSWORD"] = getpass("Contraseña de MySQL: ")

    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.environ["MYSQL_PASSWORD"],
        database="torneo_ucu"
    )

    return conexion
