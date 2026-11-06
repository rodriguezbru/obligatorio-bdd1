import mysql.connector
from database import conectar


def mostrar_equipos():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM equipo")

    equipos = cursor.fetchall()

    for equipo in equipos:
        print(equipo)

    cursor.close()
    conexion.close()


def agregar_equipo():
    nombre = input("Nombre del equipo: ")
    torneo = int(input("ID del torneo: "))
    facultad = int(input("ID de facultad: "))

    conexion = conectar()
    cursor = conexion.cursor()

    sql = """
    INSERT INTO equipo
    (nombre, id_torneo, id_facultad, ci_capitan)
    VALUES (%s, %s, %s, NULL)
    """

    valores = (nombre, torneo, facultad)

    cursor.execute(sql, valores)
    conexion.commit()

    print("Equipo agregado correctamente.")

    cursor.close()
    conexion.close()

def modificar_equipo():
    id_equipo = input("ID del equipo a modificar: ")
    nombre = input("Nuevo nombre del equipo: ")

    conexion = conectar()
    cursor = conexion.cursor()

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
        print("No se encontró el equipo o ya tenía ese nombre.")

    cursor.close()
    conexion.close()



def eliminar_equipo():
    id_equipo = input("ID del equipo a eliminar: ")

    conexion = conectar()
    cursor = conexion.cursor()

    try:
        sql = "DELETE FROM equipo WHERE id_equipo = %s"
        cursor.execute(sql, (id_equipo,))
        conexion.commit()

        if cursor.rowcount > 0:
            print("Equipo eliminado correctamente.")
        else:
            print("No se encontró el equipo.")

    except mysql.connector.Error as error:
        conexion.rollback()
        print("No se pudo eliminar el equipo:", error)

    cursor.close()
    conexion.close()


def mostrar_plantel():
    id_equipo = input("ID del equipo: ")

    conexion = conectar()
    cursor = conexion.cursor()

    sql = """
    SELECT j.ci, j.nombre, j.apellido,
           ejt.numero_camiseta
    FROM equipo_jugador_torneo ejt
    JOIN jugador j
        ON ejt.ci_jugador = j.ci
    WHERE ejt.id_equipo = %s
    ORDER BY ejt.numero_camiseta
    """

    cursor.execute(sql, (id_equipo,))
    jugadores = cursor.fetchall()

    for jugador in jugadores:
        print(jugador)

    cursor.close()
    conexion.close()



def agregar_jugador_equipo():
    id_equipo = int(input("ID del equipo: "))
    ci = input("Cédula del jugador: ")
    numero = int(input("Número de camiseta: "))

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

        cursor.execute(
            "SELECT estado FROM torneo WHERE id_torneo = %s",
            (id_torneo,)
        )
        estado = cursor.fetchone()[0]

        if estado != "inscripción":
            print("No se pueden modificar planteles fuera del período de inscripción.")
            return

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

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM equipo_jugador_torneo
            WHERE id_equipo = %s
            """,
            (id_equipo,)
        )
        cantidad = cursor.fetchone()[0]

        if cantidad >= 10:
            print("El equipo ya tiene 10 jugadores.")
            return

        if jugador[1] in ("docente", "funcionario"):
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM equipo_jugador_torneo ejt
                JOIN jugador j ON ejt.ci_jugador = j.ci
                WHERE ejt.id_equipo = %s
                AND j.tipo IN ('docente', 'funcionario')
                """,
                (id_equipo,)
            )

            cantidad = cursor.fetchone()[0]

            if cantidad >= 2:
                print("El equipo ya tiene 2 docentes o funcionarios.")
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


def asignar_capitan():
    id_equipo = input("ID del equipo: ")
    ci = input("Cédula del nuevo capitán: ")

    conexion = conectar()
    cursor = conexion.cursor()

    try:
        sql = """
        SELECT *
        FROM equipo_jugador_torneo
        WHERE id_equipo = %s AND ci_jugador = %s
        """

        cursor.execute(sql, (id_equipo, ci))
        jugador = cursor.fetchone()

        if jugador is None:
            print("El jugador no pertenece al equipo.")
            return

        sql = """
        UPDATE equipo
        SET ci_capitan = %s
        WHERE id_equipo = %s
        """

        cursor.execute(sql, (ci, id_equipo))
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

        elif opcion == "0":
            break

        else:
            print("Opción inválida")
