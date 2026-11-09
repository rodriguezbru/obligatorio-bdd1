
import mysql.connector
from database import conectar


def verificar_inscripcion(cursor, id_torneo):
    cursor.execute(
        "SELECT estado FROM torneo WHERE id_torneo = %s",
        (id_torneo,)
    )
    torneo = cursor.fetchone()

    if torneo is None:
        print("El torneo no existe.")
        return False

    if torneo[0] != "inscripción":
        print("No se pueden modificar equipos ni planteles fuera del período de inscripción.")
        return False

    return True


def mostrar_equipos():
    conexion = conectar()
    cursor = conexion.cursor()

    sql = """
    SELECT
        e.id_equipo,
        e.nombre,
        f.nombre,
        j.nombre,
        j.apellido
    FROM equipo e
    JOIN facultad f ON e.id_facultad = f.id_facultad
    LEFT JOIN jugador j ON e.ci_capitan = j.ci
    ORDER BY e.id_equipo
    """

    cursor.execute(sql)
    equipos = cursor.fetchall()

    print("\n===== EQUIPOS DEL TORNEO =====")

    for equipo in equipos:
        id_equipo, nombre, facultad, nombre_capitan, apellido_capitan = equipo

        print(f"\nEquipo {id_equipo}: {nombre}")
        print(f"Facultad: {facultad}")

        if nombre_capitan is not None:
            print(f"Capitán: {nombre_capitan} {apellido_capitan}")
        else:
            print("Capitán: Sin asignar")

    cursor.close()
    conexion.close()


def agregar_equipo():
    try:
        torneo = int(input("ID del torneo: "))
        conexion = conectar()
        cursor = conexion.cursor()

        try:
            if not verificar_inscripcion(cursor, torneo):
                return

            nombre = input("Nombre del equipo: ")
            facultad = int(input("ID de facultad: "))

            sql = """
            INSERT INTO equipo
            (nombre, id_torneo, id_facultad, ci_capitan)
            VALUES (%s, %s, %s, NULL)
            """

            cursor.execute(sql, (nombre, torneo, facultad))
            conexion.commit()

            print("Equipo agregado correctamente.")

        except mysql.connector.Error as error:
            conexion.rollback()
            print("Error:", error)

        finally:
            cursor.close()
            conexion.close()

    except ValueError:
        print("Debés ingresar un número válido.")


def modificar_equipo():
    try:
        id_equipo = int(input("ID del equipo a modificar: "))

        conexion = conectar()
        cursor = conexion.cursor()

        try:
            cursor.execute(
                "SELECT id_torneo FROM equipo WHERE id_equipo = %s",
                (id_equipo,)
            )
            equipo = cursor.fetchone()

            if equipo is None:
                print("El equipo no existe.")
                return

            if not verificar_inscripcion(cursor, equipo[0]):
                return

            nombre = input("Nuevo nombre del equipo: ")

            sql = """
            UPDATE equipo
            SET nombre = %s
            WHERE id_equipo = %s
            """

            cursor.execute(sql, (nombre, id_equipo))
            conexion.commit()

            if cursor.rowcount > 0:
                print("Equipo modificado correctamente.")
            else:
                print("El equipo ya tenía ese nombre.")

        except mysql.connector.Error as error:
            conexion.rollback()
            print("Error:", error)

        finally:
            cursor.close()
            conexion.close()

    except ValueError:
        print("Debés ingresar un ID válido.")


def eliminar_equipo():
    try:
        id_equipo = int(input("ID del equipo a eliminar: "))

        conexion = conectar()
        cursor = conexion.cursor()

        try:
            cursor.execute(
                "SELECT id_torneo FROM equipo WHERE id_equipo = %s",
                (id_equipo,)
            )
            equipo = cursor.fetchone()

            if equipo is None:
                print("El equipo no existe.")
                return

            if not verificar_inscripcion(cursor, equipo[0]):
                return

            cursor.execute(
                "DELETE FROM equipo WHERE id_equipo = %s",
                (id_equipo,)
            )
            conexion.commit()

            print("Equipo eliminado correctamente.")

        except mysql.connector.Error as error:
            conexion.rollback()
            print("No se pudo eliminar el equipo:", error)

        finally:
            cursor.close()
            conexion.close()

    except ValueError:
        print("Debés ingresar un ID válido.")


def mostrar_plantel():
    id_equipo = input("ID del equipo: ")

    conexion = conectar()
    cursor = conexion.cursor()

    sql = """
    SELECT
        j.ci,
        j.nombre,
        j.apellido,
        ejt.numero_camiseta
    FROM equipo_jugador_torneo ejt
    JOIN jugador j ON ejt.ci_jugador = j.ci
    WHERE ejt.id_equipo = %s
    ORDER BY ejt.numero_camiseta
    """

    cursor.execute(sql, (id_equipo,))
    jugadores = cursor.fetchall()

    print("\n===== PLANTEL DEL EQUIPO =====")

    if len(jugadores) == 0:
        print("No hay jugadores registrados.")
    else:
        for jugador in jugadores:
            print(jugador)

    cursor.close()
    conexion.close()


def agregar_jugador_equipo():
    try:
        id_equipo = int(input("ID del equipo: "))

        conexion = conectar()
        cursor = conexion.cursor()

        try:
            cursor.execute(
                "SELECT id_torneo, id_facultad FROM equipo WHERE id_equipo = %s",
                (id_equipo,)
            )
            equipo = cursor.fetchone()

            if equipo is None:
                print("El equipo no existe.")
                return

            id_torneo, id_facultad = equipo

            if not verificar_inscripcion(cursor, id_torneo):
                return

            ci = input("Cédula del jugador: ")
            numero = int(input("Número de camiseta: "))

            cursor.execute(
                "SELECT id_facultad, tipo FROM jugador WHERE ci = %s",
                (ci,)
            )
            jugador = cursor.fetchone()

            if jugador is None:
                print("El jugador no existe.")
                return

            if jugador[0] != id_facultad:
                print("El jugador no pertenece a la facultad del equipo.")
                return

            cursor.execute("""
                SELECT COUNT(*)
                FROM equipo_jugador_torneo
                WHERE ci_jugador = %s
                AND id_torneo = %s
            """, (ci, id_torneo))

            if cursor.fetchone()[0] > 0:
                print("El jugador ya está inscrito en un equipo de este torneo.")
                return

            cursor.execute("""
                SELECT COUNT(*)
                FROM equipo_jugador_torneo
                WHERE id_equipo = %s
            """, (id_equipo,))

            cantidad = cursor.fetchone()[0]

            if cantidad >= 10:
                print("El equipo ya tiene 10 jugadores.")
                return

            if jugador[1] in ("docente", "funcionario"):
                cursor.execute("""
                    SELECT COUNT(*)
                    FROM equipo_jugador_torneo ejt
                    JOIN jugador j ON ejt.ci_jugador = j.ci
                    WHERE ejt.id_equipo = %s
                    AND j.tipo IN ('docente', 'funcionario')
                """, (id_equipo,))

                if cursor.fetchone()[0] >= 2:
                    print("El equipo ya tiene 2 docentes o funcionarios.")
                    return

            cursor.execute("""
                SELECT COUNT(*)
                FROM equipo_jugador_torneo
                WHERE id_equipo = %s
                AND numero_camiseta = %s
            """, (id_equipo, numero))

            if cursor.fetchone()[0] > 0:
                print("Ese número de camiseta ya está ocupado.")
                return

            sql = """
            INSERT INTO equipo_jugador_torneo
            (id_equipo, ci_jugador, id_torneo, numero_camiseta)
            VALUES (%s, %s, %s, %s)
            """

            cursor.execute(sql, (id_equipo, ci, id_torneo, numero))
            conexion.commit()

            print("Jugador inscrito correctamente.")

        except mysql.connector.Error as error:
            conexion.rollback()
            print("Error:", error)

        finally:
            cursor.close()
            conexion.close()

    except ValueError:
        print("Debés ingresar un número válido.")


def eliminar_jugador_equipo():
    id_equipo = input("ID del equipo: ")

    conexion = conectar()
    cursor = conexion.cursor()

    try:
        cursor.execute("""
            SELECT e.id_torneo, e.ci_capitan, t.estado
            FROM equipo e
            JOIN torneo t ON e.id_torneo = t.id_torneo
            WHERE e.id_equipo = %s
        """, (id_equipo,))

        equipo = cursor.fetchone()

        if equipo is None:
            print("El equipo no existe.")
            return

        torneo, capitan, estado = equipo

        if estado != "inscripción":
            print("No se puede modificar el plantel fuera de inscripción.")
            return

        ci = input("Cédula del jugador a quitar: ")

        if ci == capitan:
            print("Primero tenés que asignar otro capitán.")
            return

        cursor.execute("""
            SELECT COUNT(*)
            FROM equipo_jugador_torneo
            WHERE id_equipo = %s
        """, (id_equipo,))

        cantidad = cursor.fetchone()[0]

        if cantidad <= 5:
            print("No se puede quitar un jugador porque el plantel debe tener al menos 5 jugadores.")
            return

        cursor.execute("""
            DELETE FROM equipo_jugador_torneo
            WHERE id_equipo = %s
            AND id_torneo = %s
            AND ci_jugador = %s
        """, (id_equipo, torneo, ci))

        conexion.commit()

        if cursor.rowcount > 0:
            print("Jugador eliminado del plantel.")
        else:
            print("El jugador no pertenece a ese plantel.")

    except mysql.connector.Error as error:
        conexion.rollback()
        print("Error:", error)

    finally:
        cursor.close()
        conexion.close()


def asignar_capitan():
    id_equipo = input("ID del equipo: ")

    conexion = conectar()
    cursor = conexion.cursor()

    try:
        cursor.execute("""
            SELECT e.id_torneo, t.estado
            FROM equipo e
            JOIN torneo t ON e.id_torneo = t.id_torneo
            WHERE e.id_equipo = %s
        """, (id_equipo,))

        equipo = cursor.fetchone()

        if equipo is None:
            print("El equipo no existe.")
            return

        if equipo[1] != "inscripción":
            print("No se puede cambiar el capitán fuera del período de inscripción.")
            return

        ci = input("Cédula del nuevo capitán: ")

        cursor.execute("""
            SELECT *
            FROM equipo_jugador_torneo
            WHERE id_equipo = %s
            AND id_torneo = %s
            AND ci_jugador = %s
        """, (id_equipo, equipo[0], ci))

        jugador = cursor.fetchone()

        if jugador is None:
            print("El jugador no pertenece al equipo.")
            return

        cursor.execute("""
            UPDATE equipo
            SET ci_capitan = %s
            WHERE id_equipo = %s
        """, (ci, id_equipo))

        conexion.commit()
        print("Capitán asignado correctamente.")

    except mysql.connector.Error as error:
        conexion.rollback()
        print("Error:", error)

    finally:
        cursor.close()
        conexion.close()


def menu_equipos():
    while True:
        print("\n===== GESTIÓN DE EQUIPOS =====")
        print("1. Mostrar equipos")
        print("2. Agregar equipo")
        print("3. Modificar equipo")
        print("4. Eliminar equipo")
        print("5. Mostrar plantel")
        print("6. Agregar jugador al equipo")
        print("7. Asignar capitán")
        print("8. Quitar jugador del equipo")
        print("0. Volver")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            mostrar_equipos()

        elif opcion == "2":
            agregar_equipo()

        elif opcion == "3":
            modificar_equipo()

        elif opcion == "4":
            eliminar_equipo()

        elif opcion == "5":
            mostrar_plantel()

        elif opcion == "6":
            agregar_jugador_equipo()

        elif opcion == "7":
            asignar_capitan()

        elif opcion == "8":
            eliminar_jugador_equipo()

        elif opcion == "0":
            break

        else:
            print("Opción inválida")
