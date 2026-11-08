
import mysql.connector
from database import conectar


def mostrar_complejos():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id_complejo, nombre, direccion, departamento
        FROM complejo
        ORDER BY id_complejo
    """)

    complejos = cursor.fetchall()

    print("\n===== COMPLEJOS DEPORTIVOS =====")

    for complejo in complejos:
        id_complejo, nombre, direccion, departamento = complejo

        print(f"\nComplejo {id_complejo}: {nombre}")
        print(f"Dirección: {direccion}")
        print(f"Departamento: {departamento}")

    cursor.close()
    conexion.close()


def agregar_complejo():
    nombre = input("Nombre del complejo: ")
    direccion = input("Dirección: ")
    departamento = input("Departamento: ")

    conexion = conectar()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO complejo (nombre, direccion, departamento)
            VALUES (%s, %s, %s)
            """,
            (nombre, direccion, departamento)
        )

        conexion.commit()
        print("Complejo agregado correctamente.")

    except mysql.connector.Error as error:
        conexion.rollback()
        print("Error:", error)

    finally:
        cursor.close()
        conexion.close()


def modificar_complejo():
    id_complejo = input("ID del complejo: ")
    direccion = input("Nueva dirección: ")

    conexion = conectar()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            UPDATE complejo
            SET direccion = %s
            WHERE id_complejo = %s
            """,
            (direccion, id_complejo)
        )

        conexion.commit()

        if cursor.rowcount > 0:
            print("Complejo modificado correctamente.")
        else:
            print("No se encontró el complejo o no hubo cambios.")

    except mysql.connector.Error as error:
        conexion.rollback()
        print("Error:", error)

    finally:
        cursor.close()
        conexion.close()


def eliminar_complejo():
    id_complejo = input("ID del complejo a eliminar: ")

    conexion = conectar()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            "DELETE FROM complejo WHERE id_complejo = %s",
            (id_complejo,)
        )

        conexion.commit()

        if cursor.rowcount > 0:
            print("Complejo eliminado correctamente.")
        else:
            print("No se encontró el complejo.")

    except mysql.connector.Error as error:
        conexion.rollback()
        print("No se pudo eliminar el complejo:", error)

    finally:
        cursor.close()
        conexion.close()


def mostrar_canchas():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT c.nombre_cancha, co.nombre,
               c.superficie, c.techada, c.id_complejo
        FROM cancha c
        JOIN complejo co
            ON c.id_complejo = co.id_complejo
        ORDER BY c.id_complejo, c.nombre_cancha
    """)

    canchas = cursor.fetchall()

    print("\n===== CANCHAS DISPONIBLES =====")

    for cancha in canchas:
        nombre, complejo, superficie, techada, id_complejo = cancha

        print(f"\nCancha: {nombre}")
        print(f"Complejo: {complejo} (ID: {id_complejo})")
        print(f"Superficie: {superficie}")

        if techada:
            print("Techada: Sí")
        else:
            print("Techada: No")

    cursor.close()
    conexion.close()


def agregar_cancha():
    nombre = input("Nombre de la cancha: ")
    id_complejo = int(input("ID del complejo: "))
    superficie = input("Superficie (sintético/parquet): ").lower()
    techada = input("¿Es techada? (s/n): ").lower()

    if superficie not in ("sintético", "parquet"):
        print("Superficie inválida.")
        return

    if techada not in ("s", "n"):
        print("Respuesta inválida.")
        return

    conexion = conectar()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO cancha
            (nombre_cancha, id_complejo, superficie, techada)
            VALUES (%s, %s, %s, %s)
            """,
            (nombre, id_complejo, superficie, techada == "s")
        )

        conexion.commit()
        print("Cancha agregada correctamente.")

    except mysql.connector.Error as error:
        conexion.rollback()
        print("Error:", error)

    finally:
        cursor.close()
        conexion.close()


def modificar_cancha():
    nombre = input("Nombre de la cancha: ")
    id_complejo = input("ID del complejo: ")
    superficie = input("Nueva superficie (sintético/parquet): ")

    if superficie not in ("sintético", "parquet"):
        print("Superficie inválida.")
        return

    conexion = conectar()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            UPDATE cancha
            SET superficie = %s
            WHERE nombre_cancha = %s
            AND id_complejo = %s
            """,
            (superficie, nombre, id_complejo)
        )

        conexion.commit()

        if cursor.rowcount > 0:
            print("Cancha modificada correctamente.")
        else:
            print("No se encontró la cancha o no hubo cambios.")

    except mysql.connector.Error as error:
        conexion.rollback()
        print("Error:", error)

    finally:
        cursor.close()
        conexion.close()

def eliminar_cancha():
    nombre = input("Nombre de la cancha: ")
    id_complejo = input("ID del complejo: ")

    conexion = conectar()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            DELETE FROM cancha
            WHERE nombre_cancha = %s
            AND id_complejo = %s
            """,
            (nombre, id_complejo)
        )

        conexion.commit()

        if cursor.rowcount > 0:
            print("Cancha eliminada correctamente.")
        else:
            print("No se encontró la cancha.")

    except mysql.connector.Error as error:
        conexion.rollback()
        print("No se pudo eliminar la cancha:", error)

    finally:
        cursor.close()
        conexion.close()


def menu_complejos():
    while True:
        print("\n===== GESTION DE COMPLEJOS =====")
        print("1. Mostrar complejos")
        print("2. Agregar complejo")
        print("3. Modificar complejo")
        print("4. Eliminar complejo")
        print("5. Mostrar canchas")
        print("6. Agregar cancha")
        print("7. Modificar cancha")
        print("8. Eliminar cancha")
        print("0. Volver")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            mostrar_complejos()

        elif opcion == "2":
            agregar_complejo()

        elif opcion == "3":
            modificar_complejo()

        elif opcion == "4":
            eliminar_complejo()

        elif opcion == "5":
            mostrar_canchas()

        elif opcion == "6":
            agregar_cancha()

        elif opcion == "7":
            modificar_cancha()

        elif opcion == "8":
            eliminar_cancha()

        elif opcion == "0":
            break

        else:
            print("Opción inválida")
