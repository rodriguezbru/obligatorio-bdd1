
import mysql.connector
from datetime import datetime, time, timedelta
from database import conectar


def verificar_partido(cursor, id_partido):
    cursor.execute("""
        SELECT p.estado, p.dia, t.hora_fin
        FROM partido p
        JOIN turno t ON p.id_turno = t.id_turno
        WHERE p.id_partido = %s
    """, (id_partido,))

    partido = cursor.fetchone()

    if partido is None:
        print("El partido no existe.")
        return False

    estado, dia, hora_fin = partido

    if estado in ("cancelado", "postergado"):
        print("No se puede modificar la planilla de un partido cancelado o postergado.")
        return False

    if isinstance(hora_fin, timedelta):
        final_partido = datetime.combine(dia, time.min) + hora_fin
    else:
        final_partido = datetime.combine(dia, hora_fin)

    ahora = datetime.now()

    if estado == "jugado" and ahora > final_partido + timedelta(hours=48):
        print("Pasaron más de 48 horas. No se puede modificar la planilla.")
        return False

    if estado == "programado" and ahora > final_partido:
        print("Ya pasó el horario del partido. No se puede modificar la planilla.")
        return False

    return True


def mostrar_planilla():
    id_partido = input("ID del partido: ")

    conexion = conectar()
    cursor = conexion.cursor()

    try:
        cursor.execute("""
            SELECT j.ci, j.nombre, j.apellido, pp.id_equipo
            FROM planilla_partido pp
            JOIN jugador j ON pp.ci_jugador = j.ci
            WHERE pp.id_partido = %s
        """, (id_partido,))

        jugadores = cursor.fetchall()

        print("\n===== PLANILLA DEL PARTIDO =====")

        if len(jugadores) == 0:
            print("No hay jugadores en la planilla.")
        else:
            for jugador in jugadores:
                print(jugador)

    finally:
        cursor.close()
        conexion.close()


def agregar_jugador_planilla():
    id_partido = input("ID del partido: ")

    conexion = conectar()
    cursor = conexion.cursor()

    try:
        if not verificar_partido(cursor, id_partido):
            return

        cursor.execute("""
            SELECT id_torneo, numero_fecha,
                   id_equipo_local, id_equipo_visitante
            FROM partido
            WHERE id_partido = %s
        """, (id_partido,))

        torneo, fecha, local, visitante = cursor.fetchone()

        id_equipo = input("ID del equipo: ")

        if id_equipo not in (str(local), str(visitante)):
            print("El equipo no participa en este partido.")
            return

        ci = input("Cédula del jugador: ")

        cursor.execute("""
            SELECT ci_jugador
            FROM equipo_jugador_torneo
            WHERE id_equipo = %s
              AND id_torneo = %s
              AND ci_jugador = %s
        """, (id_equipo, torneo, ci))

        if cursor.fetchone() is None:
            print("El jugador no pertenece al plantel.")
            return

        cursor.execute("""
            SELECT COUNT(*)
            FROM sancion_jugador
            WHERE ci_jugador = %s
              AND id_torneo = %s
              AND %s BETWEEN numero_fecha_inicio
                  AND numero_fecha_inicio + cantidad_fechas - 1
        """, (ci, torneo, fecha))

        if cursor.fetchone()[0] > 0:
            print("El jugador está suspendido para esta fecha.")
            return

        cursor.execute("""
            INSERT INTO planilla_partido
            (id_partido, ci_jugador, id_equipo)
            VALUES (%s, %s, %s)
        """, (id_partido, ci, id_equipo))

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

    conexion = conectar()
    cursor = conexion.cursor()

    try:
        if not verificar_partido(cursor, id_partido):
            return

        ci = input("Cédula del jugador a quitar: ")

        cursor.execute("""
            SELECT COUNT(*)
            FROM gol
            WHERE id_partido = %s
              AND ci_jugador = %s
        """, (id_partido, ci))

        if cursor.fetchone()[0] > 0:
            print("No se puede quitar al jugador porque tiene goles registrados.")
            return

        cursor.execute("""
            SELECT COUNT(*)
            FROM tarjeta
            WHERE id_partido = %s
              AND ci_jugador = %s
        """, (id_partido, ci))

        if cursor.fetchone()[0] > 0:
            print("No se puede quitar al jugador porque tiene tarjetas registradas.")
            return

        cursor.execute("""
            DELETE FROM planilla_partido
            WHERE id_partido = %s
              AND ci_jugador = %s
        """, (id_partido, ci))

        conexion.commit()

        if cursor.rowcount > 0:
            print("Jugador eliminado de la planilla.")
        else:
            print("El jugador no pertenece a esa planilla.")

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
