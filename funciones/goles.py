
import mysql.connector
from database import conectar
from datetime import datetime, timedelta


def validar_plazo_gol(id_partido):
    conexion = conectar()
    cursor = conexion.cursor()

    try:
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

        # MySQL puede devolver las horas como timedelta
        if isinstance(hora_fin, timedelta):
            fin = datetime.combine(dia, datetime.min.time()) + hora_fin
        else:
            fin = datetime.combine(dia, hora_fin)

        ahora = datetime.now()

        if ahora < fin:
            print("El partido todavía no terminó.")
            return False

        if estado == "cancelado":
            print("No se pueden registrar goles en un partido cancelado.")
            return False

        if estado == "jugado" and ahora > fin + timedelta(hours=48):
            print("Pasaron más de 48 horas. No se puede corregir el resultado.")
            return False

        return True

    finally:
        cursor.close()
        conexion.close()

def mostrar_goles():
    id_partido = input("ID del partido: ")

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT id_gol, ci_jugador, minuto, autogol
        FROM gol
        WHERE id_partido = %s
        ORDER BY minuto
        """,
        (id_partido,)
    )

    goles = cursor.fetchall()

    for gol in goles:
        print(gol)

    cursor.close()
    conexion.close()



def agregar_gol():
    id_partido = input("ID del partido: ")

    if not validar_plazo_gol(id_partido):
        return

    ci = input("Cédula del jugador: ")

    try:
        minuto = int(input("Minuto del gol: "))
    except ValueError:
        print("El minuto debe ser un número.")
        return

    if minuto < 0:
        print("El minuto no puede ser negativo.")
        return

    autogol = input("¿Fue autogol? (s/n): ").lower()

    if autogol not in ("s", "n"):
        print("Opción inválida.")
        return

    conexion = conectar()
    cursor = conexion.cursor()

    try:
        cursor.execute("""
            SELECT COUNT(*)
            FROM planilla_partido
            WHERE id_partido = %s
            AND ci_jugador = %s
        """, (id_partido, ci))

        if cursor.fetchone()[0] == 0:
            print("El jugador no figura en la planilla del partido.")
            return

        cursor.execute("""
            INSERT INTO gol
            (id_partido, ci_jugador, minuto, autogol)
            VALUES (%s, %s, %s, %s)
        """, (id_partido, ci, minuto, autogol == "s"))

        conexion.commit()
        print("Gol registrado correctamente.")

    except mysql.connector.Error as error:
        conexion.rollback()
        print("Error:", error)

    finally:
        cursor.close()
        conexion.close()

def modificar_gol():
    id_gol = input("ID del gol a modificar: ")

    conexion = conectar()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            "SELECT id_partido FROM gol WHERE id_gol = %s",
            (id_gol,)
        )

        gol = cursor.fetchone()

        if gol is None:
            print("El gol no existe.")
            return

        if not validar_plazo_gol(gol[0]):
            return

        minuto = int(input("Nuevo minuto: "))
        autogol = input("¿Fue autogol? (s/n): ").lower()

        if minuto < 0 or autogol not in ("s", "n"):
            print("Datos inválidos.")
            return

        cursor.execute("""
            UPDATE gol
            SET minuto = %s, autogol = %s
            WHERE id_gol = %s
        """, (minuto, autogol == "s", id_gol))

        conexion.commit()
        print("Gol modificado correctamente.")

    except (mysql.connector.Error, ValueError) as error:
        conexion.rollback()
        print("Error:", error)

    finally:
        cursor.close()
        conexion.close()


def eliminar_gol():
    id_gol = input("ID del gol a eliminar: ")

    conexion = conectar()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            "SELECT id_partido FROM gol WHERE id_gol = %s",
            (id_gol,)
        )

        gol = cursor.fetchone()

        if gol is None:
            print("El gol no existe.")
            return

        if not validar_plazo_gol(gol[0]):
            return

        cursor.execute(
            "DELETE FROM gol WHERE id_gol = %s",
            (id_gol,)
        )

        conexion.commit()
        print("Gol eliminado correctamente.")

    except mysql.connector.Error as error:
        conexion.rollback()
        print("Error:", error)

    finally:
        cursor.close()
        conexion.close()

def mostrar_resultado():
    id_partido = input("ID del partido: ")

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT id_equipo_local, id_equipo_visitante
        FROM partido
        WHERE id_partido = %s
        """,
        (id_partido,)
    )

    partido = cursor.fetchone()

    if partido is None:
        print("El partido no existe.")
        cursor.close()
        conexion.close()
        return

    local, visitante = partido
    
    cursor.execute(
        "SELECT nombre FROM equipo WHERE id_equipo = %s",
        (local,)
    )
    nombre_local = cursor.fetchone()[0]

    cursor.execute(
        "SELECT nombre FROM equipo WHERE id_equipo = %s",
        (visitante,)
    )
    nombre_visitante = cursor.fetchone()[0]

    goles_local = 0
    goles_visitante = 0

    cursor.execute(
        """
        SELECT pp.id_equipo, g.autogol
        FROM gol g
        JOIN planilla_partido pp
          ON g.id_partido = pp.id_partido
         AND g.ci_jugador = pp.ci_jugador
        WHERE g.id_partido = %s
        """,
        (id_partido,)
    )

    for equipo, autogol in cursor.fetchall():
        if equipo == local:
            if autogol:
                goles_visitante += 1
            else:
                goles_local += 1
        else:
            if autogol:
                goles_local += 1
            else:
                goles_visitante += 1

    print(f"Resultado: {nombre_local} {goles_local} - {goles_visitante} {nombre_visitante}")

    cursor.close()
    conexion.close()


def menu_goles():
    while True:
        print("\n===== GOLES =====")
        print("1. Mostrar goles")
        print("2. Agregar gol")
        print("3. Ver resultado")
        print("4. Modificar gol")
        print("5. Eliminar gol")
        print("0. Volver")

        opcion = input("Opción: ")

        if opcion == "1":
            mostrar_goles()
        elif opcion == "2":
            agregar_gol()
        elif opcion == "3":
            mostrar_resultado()
        elif opcion == "4":
            modificar_gol()
        elif opcion == "5":
            eliminar_gol()

        
        elif opcion == "0":
            break
        else:
            print("Opción inválida")
