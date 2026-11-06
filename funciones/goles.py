
import mysql.connector
from database import conectar


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
    ci = input("Cédula del jugador: ")
    minuto = int(input("Minuto del gol: "))
    autogol = input("¿Fue autogol? (s/n): ").lower()

    if autogol not in ("s", "n"):
        print("Opción inválida.")
        return

    conexion = conectar()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO gol
            (id_partido, ci_jugador, minuto, autogol)
            VALUES (%s, %s, %s, %s)
            """,
            (id_partido, ci, minuto, autogol == "s")
        )

        conexion.commit()
        print("Gol registrado correctamente.")

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
        print("0. Volver")

        opcion = input("Opción: ")

        if opcion == "1":
            mostrar_goles()
        elif opcion == "2":
            agregar_gol()
        elif opcion == "3":
            mostrar_resultado()
        elif opcion == "0":
            break
        else:
            print("Opción inválida")
