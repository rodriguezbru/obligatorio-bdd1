
import mysql.connector
from database import conectar


def mostrar_partidos():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM partido")
    partidos = cursor.fetchall()

    for partido in partidos:
        print(partido)

    cursor.close()
    conexion.close()


def agregar_partido():
    torneo = int(input("ID del torneo: "))
    fecha = int(input("Número de fecha: "))
    local = int(input("ID del equipo local: "))
    visitante = int(input("ID del equipo visitante: "))
    dia = input("Día (AAAA-MM-DD): ")
    turno = int(input("ID del turno: "))
    cancha = input("Nombre de la cancha: ")
    complejo = int(input("ID del complejo: "))

    conexion = conectar()
    cursor = conexion.cursor()

    try:
        sql = """
        INSERT INTO partido
        (id_torneo, numero_fecha, id_equipo_local,
         id_equipo_visitante, dia, id_turno,
         nombre_cancha, id_complejo, estado)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'programado')
        """

        valores = (torneo, fecha, local, visitante,
                   dia, turno, cancha, complejo)

        cursor.execute(sql, valores)
        conexion.commit()

        print("Partido agregado correctamente.")

    except mysql.connector.Error as error:
        conexion.rollback()
        print("Error al agregar partido:", error)

    finally:
        cursor.close()
        conexion.close()


def cambiar_estado_partido():
    id_partido = int(input("ID del partido: "))
    estado = input(
        "Nuevo estado (programado, jugado, postergado, cancelado): "
    )

    if estado not in ("programado", "jugado", "postergado", "cancelado"):
        print("Estado inválido.")
        return

    conexion = conectar()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            "UPDATE partido SET estado = %s WHERE id_partido = %s",
            (estado, id_partido)
        )
        conexion.commit()

        if cursor.rowcount > 0:
            print("Estado actualizado correctamente.")
        else:
            print("No se encontró el partido o ya tenía ese estado.")

    except mysql.connector.Error as error:
        conexion.rollback()
        print("Error:", error)

    finally:
        cursor.close()
        conexion.close()


def menu_partidos():
    while True:
        print("\n===== GESTIÓN DE PARTIDOS =====")
        print("1. Mostrar partidos")
        print("2. Agregar partido")
        print("3. Cambiar estado de un partido")
        print("0. Volver")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            mostrar_partidos()
        elif opcion == "2":
            agregar_partido()
        elif opcion == "3":
            cambiar_estado_partido()
        elif opcion == "0":
            break
        else:
            print("Opción inválida")
