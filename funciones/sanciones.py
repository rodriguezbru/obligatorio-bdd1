
import mysql.connector
from database import conectar


def mostrar_sanciones():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT s.id_sancion, j.nombre, j.apellido,
               s.motivo, s.numero_fecha_inicio,
               s.cantidad_fechas
        FROM sancion_jugador s
        JOIN jugador j ON s.ci_jugador = j.ci
        ORDER BY s.id_sancion
    """)

    sanciones = cursor.fetchall()

    print("\n===== SANCIONES =====")

    for sancion in sanciones:
        id_sancion, nombre, apellido, motivo, fecha, cantidad = sancion

        print(f"\nSanción {id_sancion}")
        print(f"Jugador: {nombre} {apellido}")
        print(f"Motivo: {motivo}")
        print(f"Desde la fecha: {fecha}")
        print(f"Cantidad de fechas: {cantidad}")

    cursor.close()
    conexion.close()


def agregar_sancion():
    ci = input("Cédula del jugador: ")
    torneo = int(input("ID del torneo: "))
    motivo = input("Motivo (roja/acumulación de amarillas/disciplinaria): ")
    fecha = int(input("Fecha de inicio de sanción: "))
    cantidad = int(input("Cantidad de fechas: "))

    conexion = conectar()
    cursor = conexion.cursor()

    try:
        cursor.execute("""
            INSERT INTO sancion_jugador
            (ci_jugador, id_torneo, motivo,
             numero_fecha_inicio, cantidad_fechas)
            VALUES (%s, %s, %s, %s, %s)
        """, (ci, torneo, motivo, fecha, cantidad))

        conexion.commit()
        print("Sanción agregada correctamente.")

    except mysql.connector.Error as error:
        conexion.rollback()
        print("Error:", error)

    finally:
        cursor.close()
        conexion.close()


def modificar_sancion():
    id_sancion = input("ID de la sanción: ")
    cantidad = int(input("Nueva cantidad de fechas: "))

    conexion = conectar()
    cursor = conexion.cursor()

    try:
        cursor.execute("""
            UPDATE sancion_jugador
            SET cantidad_fechas = %s
            WHERE id_sancion = %s
        """, (cantidad, id_sancion))

        conexion.commit()

        if cursor.rowcount > 0:
            print("Sanción modificada correctamente.")
        else:
            print("No se encontró la sanción o no hubo cambios.")

    except mysql.connector.Error as error:
        conexion.rollback()
        print("Error:", error)

    finally:
        cursor.close()
        conexion.close()


def eliminar_sancion():
    id_sancion = input("ID de la sanción a eliminar: ")

    conexion = conectar()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            "DELETE FROM sancion_jugador WHERE id_sancion = %s",
            (id_sancion,)
        )

        conexion.commit()

        if cursor.rowcount > 0:
            print("Sanción eliminada correctamente.")
        else:
            print("No se encontró la sanción.")

    except mysql.connector.Error as error:
        conexion.rollback()
        print("Error:", error)

    finally:
        cursor.close()
        conexion.close()


def menu_sanciones():
    while True:
        print("\n===== GESTIÓN DE SANCIONES =====")
        print("1. Mostrar sanciones")
        print("2. Agregar sanción")
        print("3. Modificar sanción")
        print("4. Eliminar sanción")
        print("0. Volver")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            mostrar_sanciones()
        elif opcion == "2":
            agregar_sancion()
        elif opcion == "3":
            modificar_sancion()
        elif opcion == "4":
            eliminar_sancion()
        elif opcion == "0":
            break
        else:
            print("Opción inválida")
