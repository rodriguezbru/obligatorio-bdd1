
import mysql.connector
from database import conectar
from datetime import datetime, date



def mostrar_partidos():
    conexion = conectar()
    cursor = conexion.cursor()

    sql = """
    SELECT
        p.numero_fecha,
        p.dia,
        t.hora_inicio,
        el.nombre,
        ev.nombre,
        p.nombre_cancha,
        c.nombre,
        p.estado
    FROM partido p
    JOIN equipo el
        ON p.id_equipo_local = el.id_equipo
    JOIN equipo ev
        ON p.id_equipo_visitante = ev.id_equipo
    JOIN turno t
        ON p.id_turno = t.id_turno
    JOIN complejo c
        ON p.id_complejo = c.id_complejo
    ORDER BY p.numero_fecha, t.hora_inicio
    """

    cursor.execute(sql)
    partidos = cursor.fetchall()

    print("\n===== PARTIDOS DEL TORNEO =====")

    for partido in partidos:
        fecha, dia, hora, local, visitante, cancha, complejo, estado = partido

        print(f"\nFecha {fecha} - {dia}")
        print(f"Hora: {hora}")
        print(f"{local} vs {visitante}")
        print(f"Lugar: {complejo} - {cancha}")
        print(f"Estado: {estado}")

    cursor.close()
    conexion.close()



def validar_ubicacion(cursor, torneo, dia, turno, cancha, complejo, local, visitante, excluir=None):
    try:
        dia_fecha = date.fromisoformat(dia)
    except ValueError:
        print("La fecha debe tener el formato AAAA-MM-DD.")
        return False

    cursor.execute("""
        SELECT fecha_inicio, fecha_fin
        FROM torneo WHERE id_torneo = %s
    """, (torneo,))
    fechas = cursor.fetchone()
    if fechas is None or not (fechas[0] <= dia_fecha <= fechas[1]):
        print("El día debe estar dentro de las fechas del torneo.")
        return False

    cursor.execute("SELECT id_turno FROM turno WHERE id_turno = %s", (turno,))
    if cursor.fetchone() is None:
        print("El turno no existe.")
        return False

    cursor.execute("""
        SELECT nombre_cancha FROM cancha
        WHERE nombre_cancha = %s AND id_complejo = %s
    """, (cancha, complejo))
    if cursor.fetchone() is None:
        print("La cancha no pertenece al complejo indicado.")
        return False

    cursor.execute("""
        SELECT COUNT(*) FROM partido
        WHERE dia = %s AND id_turno = %s
          AND nombre_cancha = %s AND id_complejo = %s
          AND estado IN ('programado', 'jugado')
          AND (%s IS NULL OR id_partido <> %s)
    """, (dia, turno, cancha, complejo, excluir, excluir))
    if cursor.fetchone()[0] > 0:
        print("La cancha ya está ocupada en ese horario.")
        return False

    cursor.execute("""
        SELECT COUNT(*) FROM partido
        WHERE dia = %s AND id_turno = %s
          AND estado IN ('programado', 'jugado')
          AND (id_equipo_local IN (%s, %s)
               OR id_equipo_visitante IN (%s, %s))
          AND (%s IS NULL OR id_partido <> %s)
    """, (dia, turno, local, visitante, local, visitante, excluir, excluir))
    if cursor.fetchone()[0] > 0:
        print("Uno de los equipos ya tiene otro partido a esa hora.")
        return False

    return True


def validar_partido(cursor, torneo, fecha, local, visitante,
                    dia, turno, cancha, complejo):
    if local == visitante:
        print("Un equipo no puede jugar contra sí mismo.")
        return False

    cursor.execute("""
        SELECT COUNT(*) FROM equipo
        WHERE id_equipo IN (%s, %s) AND id_torneo = %s
    """, (local, visitante, torneo))
    if cursor.fetchone()[0] != 2:
        print("Los dos equipos deben pertenecer al torneo.")
        return False

    cursor.execute("""
        SELECT COUNT(*) FROM fecha_torneo
        WHERE id_torneo = %s AND numero_fecha = %s
    """, (torneo, fecha))
    if cursor.fetchone()[0] == 0:
        print("El número de fecha no existe en el torneo.")
        return False

    cursor.execute("""
        SELECT COUNT(*) FROM partido
        WHERE id_torneo = %s AND numero_fecha = %s
          AND estado != 'cancelado'
          AND (id_equipo_local IN (%s, %s)
               OR id_equipo_visitante IN (%s, %s))
    """, (torneo, fecha, local, visitante, local, visitante))
    if cursor.fetchone()[0] > 0:
        print("Uno de los equipos ya juega en esta fecha.")
        return False

    cursor.execute("""
        SELECT COUNT(*) FROM partido
        WHERE id_torneo = %s AND estado != 'cancelado'
          AND ((id_equipo_local = %s AND id_equipo_visitante = %s)
               OR (id_equipo_local = %s AND id_equipo_visitante = %s))
    """, (torneo, local, visitante, visitante, local))
    if cursor.fetchone()[0] > 0:
        print("Estos equipos ya se enfrentaron.")
        return False

    for equipo in (local, visitante):
        cursor.execute("""
            SELECT COUNT(*) FROM equipo_jugador_torneo
            WHERE id_equipo = %s AND id_torneo = %s
        """, (equipo, torneo))
        if cursor.fetchone()[0] < 5:
            print("Uno de los equipos tiene menos de 5 jugadores.")
            return False

    return validar_ubicacion(cursor, torneo, dia, turno, cancha,
                             complejo, local, visitante)


def agregar_partido():
    try:
        torneo = int(input("ID del torneo: "))
        fecha = int(input("Número de fecha: "))
        local = int(input("ID del equipo local: "))
        visitante = int(input("ID del equipo visitante: "))
        dia = input("Día (AAAA-MM-DD): ").strip()
        turno = int(input("ID del turno: "))
        cancha = input("Nombre de la cancha: ").strip()
        complejo = int(input("ID del complejo: "))
    except ValueError:
        print("Los identificadores deben ser números.")
        return

    conexion = conectar()
    cursor = conexion.cursor()

    try:
        
        if not validar_partido(
            cursor, torneo, fecha, local, visitante,
            dia, turno, cancha, complejo
        ):
            return

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


def modificar_partido():
    try:
        id_partido = int(input("ID del partido a modificar: "))
    except ValueError:
        print("El ID debe ser un número.")
        return

    conexion = conectar()
    cursor = conexion.cursor()

    try:
        cursor.execute("""
            SELECT id_torneo, estado, dia, id_turno,
                   nombre_cancha, id_complejo,
                   id_equipo_local, id_equipo_visitante
            FROM partido WHERE id_partido = %s
        """, (id_partido,))
        partido = cursor.fetchone()

        if partido is None:
            print("El partido no existe.")
            return

        (torneo, estado, dia_actual, turno_actual, cancha_actual,
         complejo_actual, local, visitante) = partido

        if estado in ("jugado", "cancelado"):
            print("No se puede modificar un partido jugado o cancelado.")
            return

        print(f"Día actual: {dia_actual}")
        print(f"Turno actual: {turno_actual}")
        print(f"Cancha actual: {cancha_actual}")
        print(f"Complejo actual: {complejo_actual}")

        dia = input("Nuevo día (AAAA-MM-DD): ").strip()
        turno = int(input("Nuevo ID del turno: "))
        cancha = input("Nueva cancha: ").strip()
        complejo = int(input("Nuevo ID del complejo: "))
        motivo = input("Motivo de la reprogramación: ").strip()

        if not motivo:
            print("Es necesario indicar un motivo.")
            return

        if not validar_ubicacion(cursor, torneo, dia, turno, cancha,
                                 complejo, local, visitante, id_partido):
            return

        if (dia == str(dia_actual) and turno == turno_actual
                and cancha == cancha_actual and complejo == complejo_actual):
            print("No hay cambios para guardar.")
            return

        cursor.execute("""
            UPDATE partido
            SET dia = %s, id_turno = %s,
                nombre_cancha = %s, id_complejo = %s,
                estado = 'programado'
            WHERE id_partido = %s
        """, (dia, turno, cancha, complejo, id_partido))

        cursor.execute("""
            INSERT INTO historial_partido (
                id_partido, dia_anterior, id_turno_anterior,
                nombre_cancha_anterior, id_complejo_anterior,
                dia_nuevo, id_turno_nuevo, nombre_cancha_nueva,
                id_complejo_nuevo, motivo
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (id_partido, dia_actual, turno_actual, cancha_actual,
              complejo_actual, dia, turno, cancha, complejo, motivo))

        conexion.commit()
        print("Partido reprogramado y registrado en el historial.")

    except (mysql.connector.Error, ValueError) as error:
        conexion.rollback()
        print("Error al modificar partido:", error)
    finally:
        cursor.close()
        conexion.close()


def cambiar_estado_partido():
    try:
        id_partido = int(input("ID del partido: "))
    except ValueError:
        print("El ID debe ser un número.")
        return

    nuevo_estado = input(
        "Nuevo estado (programado, jugado, postergado, cancelado): "
    ).strip().lower()
    if nuevo_estado not in ("programado", "jugado", "postergado", "cancelado"):
        print("Estado inválido.")
        return

    conexion = conectar()
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            SELECT p.estado, p.dia, t.hora_fin
            FROM partido p JOIN turno t ON p.id_turno = t.id_turno
            WHERE p.id_partido = %s
        """, (id_partido,))
        datos = cursor.fetchone()
        if datos is None:
            print("El partido no existe.")
            return

        estado_actual, dia, hora_fin = datos
        if estado_actual == nuevo_estado:
            print("El partido ya tenía ese estado.")
            return

        if estado_actual in ("jugado", "cancelado"):
            print("No se puede cambiar el estado de un partido jugado o cancelado.")
            return

        if estado_actual == "postergado" and nuevo_estado == "programado":
            print("Para reprogramarlo usá la opción 5 y registrá el motivo.")
            return

        if estado_actual == "postergado" and nuevo_estado == "jugado":
            print("Primero tenés que reprogramar el partido.")
            return

        if nuevo_estado == "jugado":
            fin = datetime.combine(dia, (datetime.min + hora_fin).time())
            if fin > datetime.now():
                print("No se puede marcar como jugado un partido que no terminó.")
                return

        cursor.execute("""
            UPDATE partido SET estado = %s WHERE id_partido = %s
        """, (nuevo_estado, id_partido))
        conexion.commit()
        print("Estado actualizado correctamente.")

    except mysql.connector.Error as error:
        conexion.rollback()
        print("Error al cambiar estado:", error)
    finally:
        cursor.close()
        conexion.close()


def eliminar_partido():
    id_partido = input("ID del partido a eliminar: ")

    conexion = conectar()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            "SELECT estado FROM partido WHERE id_partido = %s",
            (id_partido,)
        )

        partido = cursor.fetchone()

        if partido is None:
            print("El partido no existe.")
            return

        if partido[0] == "jugado":
            print("No se puede eliminar un partido jugado.")
            return

        cursor.execute("""
            SELECT COUNT(*) FROM historial_partido WHERE id_partido = %s
        """, (id_partido,))
        if cursor.fetchone()[0] > 0:
            print("No se puede eliminar un partido con historial de cambios.")
            return

        cursor.execute(
            "DELETE FROM partido WHERE id_partido = %s",
            (id_partido,)
        )

        conexion.commit()
        print("Partido eliminado correctamente.")

    except mysql.connector.Error as error:
        conexion.rollback()
        print("No se pudo eliminar el partido:", error)

    finally:
        cursor.close()
        conexion.close()

def menu_partidos():
    while True:
        print("\n===== GESTIÓN DE PARTIDOS =====")
        print("1. Mostrar partidos")
        print("2. Agregar partido")
        print("3. Cambiar estado de un partido")
        print("4. Eliminar partido")
        print("5. Modificar partido")
        print("0. Volver")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            mostrar_partidos()
        elif opcion == "2":
            agregar_partido()
        elif opcion == "3":
            cambiar_estado_partido()

        elif opcion == "4":
            eliminar_partido()

        elif opcion == "5":
            modificar_partido()
        elif opcion == "0":
            break
        else:
            print("Opción inválida")
