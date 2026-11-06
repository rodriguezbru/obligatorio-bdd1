
import mysql.connector
from database import conectar


def mostrar_planilla():
    id_partido = input("ID del partido: ")

    conexion = conectar()
    cursor = conexion.cursor()

    sql = """
    SELECT j.ci, j.nombre, j.apellido,
           pp.id_equipo
    FROM planilla_partido pp
    JOIN jugador j ON pp.ci_jugador = j.ci
    WHERE pp.id_partido = %s
    """

    cursor.execute(sql, (id_partido,))
    jugadores = cursor.fetchall()

    for jugador in jugadores:
        print(jugador)

    cursor.close()
    conexion.close()


def agregar_jugador_planilla():
    id_partido = input("ID del partido: ")
    ci = input("Cédula del jugador: ")
    id_equipo = input("ID del equipo: ")

    conexion = conectar()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            SELECT id_torneo, numero_fecha,
                   id_equipo_local, id_equipo_visitante
            FROM partido
            WHERE id_partido = %s
            """,
            (id_partido,)
        )

        partido = cursor.fetchone()

        if partido is None:
            print("El partido no existe.")
            return

        torneo, fecha, local, visitante = partido

        if int(id_equipo) not in (local, visitante):
            print("El equipo no participa en este partido.")
            return

        cursor.execute(
            """
            SELECT ci_jugador
            FROM equipo_jugador_torneo
            WHERE id_equipo = %s
              AND id_torneo = %s
              AND ci_jugador = %s
            """,
            (id_equipo, torneo, ci)
        )

        if cursor.fetchone() is None:
            print("El jugador no pertenece al plantel.")
            return

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM sancion_jugador
            WHERE ci_jugador = %s
              AND id_torneo = %s
              AND %s BETWEEN numero_fecha_inicio
                  AND numero_fecha_inicio + cantidad_fechas - 1
            """,
            (ci, torneo, fecha)
        )

        if cursor.fetchone()[0] > 0:
            print("El jugador está suspendido para esta fecha.")
            return

        cursor.execute(
            """
            INSERT INTO planilla_partido
            (id_partido, ci_jugador, id_equipo)
            VALUES (%s, %s, %s)
            """,
            (id_partido, ci, id_equipo)
        )

        conexion.commit()
        print("Jugador agregado a la planilla.")

    except mysql.connector.Error as error:
        conexion.rollback()
        print("Error:", error)

    finally:
        cursor.close()
        conexion.close()


def eliminar_jugador_planilla():
    id_partido = input("ID del partido: ")
    ci = input("Cédula del jugador: ")

    conexion = conectar()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            DELETE FROM planilla_partido
            WHERE id_partido = %s
              AND ci_jugador = %s
            """,
            (id_partido, ci)
        )

        conexion.commit()

        if cursor.rowcount > 0:
            print("Jugador eliminado de la planilla.")
        else:
            print("No se encontró al jugador en esa planilla.")

    except mysql.connector.Error as error:
        conexion.rollback()
        print("Error:", error)

    finally:
        cursor.close()
        conexion.close()


def menu_planillas():
    while True:
        print("\n===== PLANILLAS =====")
        print("1. Mostrar planilla")
        print("2. Agregar jugador")
        print("3. Eliminar jugador")
        print("0. Volver")

        opcion = input("Opción: ")

        if opcion == "1":
            mostrar_planilla()
        elif opcion == "2":
            agregar_jugador_planilla()
        elif opcion == "3":
            eliminar_jugador_planilla()
        elif opcion == "0":
            break
        else:
            print("Opción inválida")
