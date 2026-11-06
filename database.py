import mysql.connector
import os

def conectar():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.environ["MYSQL_PASSWORD"],
        database="torneo_ucu"
    )
    return conexion