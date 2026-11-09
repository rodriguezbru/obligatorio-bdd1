
import mysql.connector
from datetime import datetime, timedelta
from database import conectar


def validar_plazo_tarjeta(cursor, id_partido):
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

    if estado != "jugado":
        print("Solo se pueden registrar tarjetas en partidos jugados.")
        return False

    if isinstance(hora_fin, timedelta):
        fin = datetime.combine(dia, datetime.min.time()) + hora_fin
    else:
        fin = datetime.combine(dia, hora_fin)

    ahora = datetime.now()

    if ahora < fin:
        print("El partido todavía no terminó.")
        return False

    if ahora > fin + timedelta(hours=48):
        print("Pasaron más de 48 horas. No se pueden registrar tarjetas.")
        return False

    return True


def mostrar_tarjetas():
    id_partido = input("ID del partido: ")

    conexion = conectar()
    cursor = conexion.cursor()

    try:
        cursor.execute("""
            SELECT id_tarjeta, ci_jugador, minuto, color
            FROM tarjeta
            WHERE id_partido = %s
            ORDER BY minuto
        """, (id_partido,))

        tarjetas = cursor.fetchall()

        print("\n===== TARJETAS DEL PARTIDO =====")

        if len(tarjetas) == 0:
            print("No hay tarjetas registradas.")
        else:
            for tarjeta in tarjetas:
                print(tarjeta)

    finally:
        cursor.close()
        conexion.close()


def agregar_tarjeta():
    id_partido = input("ID del partido: ")

    conexion = conectar()
    cursor = conexion.cursor()

    try:
        if not validar_plazo_tarjeta(cursor, id_partido):
            return

        ci = input("Cédula del jugador: ")

        cursor.execute("""
            SELECT COUNT(*)
            FROM planilla_partido
            WHERE id_partido = %s
              AND ci_jugador = %s
        """, (id_partido, ci))

        if cursor.fetchone()[0] == 0:
            print("El jugador no figura en la planilla del partido.")
            return

        try:
            minuto = int(input("Minuto de la tarjeta: "))
        except ValueError:
            print("El minuto debe ser un número.")
            return

        if minuto < 0:
            print("El minuto no puede ser negativo.")
            return

        color = input("Color (amarilla/roja): ").lower()

        if color not in ("amarilla", "roja"):
            print("Color inválido.")
            return

        cursor.execute("""
            INSERT INTO tarjeta
            (id_partido, ci_jugador, minuto, color)
            VALUES (%s, %s, %s, %s)
        """, (id_partido, ci, minuto, color))

        if color == "roja":
            sancionar_por_roja(cursor, id_partido, ci)

        elif color == "amarilla":
            sancionar_por_amarillas(cursor, id_partido, ci)

        conexion.commit()
        print("Tarjeta registrada correctamente.")

    except mysql.connector.Error as error:
        conexion.rollback()
        print("Error:", error)

    finally:
        cursor.close()
        conexion.close()


def sancionar_por_roja(cursor, id_partido, ci):
    cursor.execute("""
        SELECT id_torneo, numero_fecha
        FROM partido
        WHERE id_partido = %s
    """, (id_partido,))

    torneo, fecha = cursor.fetchone()

    cursor.execute("""
        SELECT COUNT(*)
        FROM sancion_jugador
        WHERE ci_jugador = %s
          AND id_torneo = %s
          AND motivo = 'roja'
          AND numero_fecha_inicio = %s
    """, (ci, torneo, fecha + 1))

    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO sancion_jugador
            (ci_jugador, id_torneo, motivo,
             numero_fecha_inicio, cantidad_fechas)
            VALUES (%s, %s, 'roja', %s, 1)
        """, (ci, torneo, fecha + 1))


def sancionar_por_amarillas(cursor, id_partido, ci):
    cursor.execute("""
        SELECT id_torneo, numero_fecha
        FROM partido
        WHERE id_partido = %s
    """, (id_partido,))

    torneo, fecha = cursor.fetchone()

    cursor.execute("""
        SELECT COUNT(*)
        FROM tarjeta t
        JOIN partido p ON t.id_partido = p.id_partido
        WHERE t.ci_jugador = %s
          AND p.id_torneo = %s
          AND p.estado = 'jugado'
          AND t.color = 'amarilla'
    """, (ci, torneo))

    cantidad = cursor.fetchone()[0]

    if cantidad > 0 and cantidad % 3 == 0:
        cursor.execute("""
            SELECT COUNT(*)
            FROM sancion_jugador
            WHERE ci_jugador = %s
              AND id_torneo = %s
              AND motivo = 'acumulación de amarillas'
              AND numero_fecha_inicio = %s
        """, (ci, torneo, fecha + 1))

        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO sancion_jugador
                (ci_jugador, id_torneo, motivo,
                 numero_fecha_inicio, cantidad_fechas)
                VALUES (%s, %s, 'acumulación de amarillas', %s, 1)
            """, (ci, torneo, fecha + 1))


def menu_tarjetas():
    while True:
        print("\n===== TARJETAS =====")
        print("1. Mostrar tarjetas")
        print("2. Agregar tarjeta")
        print("0. Volver")

        opcion = input("Opción: ")

        if opcion == "1":
            mostrar_tarjetas()

        elif opcion == "2":
            agregar_tarjeta()

        elif opcion == "0":
            break

        else:
            print("Opción inválida")
