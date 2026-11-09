
import mysql.connector
from database import conectar


def mostrar_sanciones():
    conexion = conectar()
    cursor = conexion.cursor()

    try:
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

        if len(sanciones) == 0:
            print("No hay sanciones registradas.")

        for sancion in sanciones:
            id_sancion, nombre, apellido, motivo, fecha, cantidad = sancion

            print(f"\nSanción {id_sancion}")
            print(f"Jugador: {nombre} {apellido}")
            print(f"Motivo: {motivo}")
            print(f"Desde la fecha: {fecha}")
            print(f"Cantidad de fechas: {cantidad}")

    finally:
        cursor.close()
        conexion.close()


def agregar_sancion():
    try:
        torneo = int(input("ID del torneo: "))
        ci = input("Cédula del jugador: ")

        conexion = conectar()
        cursor = conexion.cursor()

        try:
            cursor.execute("""
                SELECT COUNT(*)
                FROM equipo_jugador_torneo
                WHERE ci_jugador = %s
                  AND id_torneo = %s
            """, (ci, torneo))

            if cursor.fetchone()[0] == 0:
                print("El jugador no está inscrito en ese torneo.")
                return

            fecha = int(input("Fecha de inicio de sanción: "))
            cantidad = int(input("Cantidad de fechas: "))

            if cantidad <= 0:
                print("La cantidad de fechas debe ser mayor que cero.")
                return

            cursor.execute("""
                SELECT COUNT(*)
                FROM fecha_torneo
                WHERE id_torneo = %s
                  AND numero_fecha = %s
            """, (torneo, fecha))

            if cursor.fetchone()[0] == 0:
                print("La fecha indicada no existe en ese torneo.")
                return

            cursor.execute("""
                SELECT MAX(numero_fecha)
                FROM fecha_torneo
                WHERE id_torneo = %s
            """, (torneo,))

            ultima_fecha = cursor.fetchone()[0]

            if fecha + cantidad - 1 > ultima_fecha:
                print("La sanción supera las fechas registradas del torneo.")
                return

            cursor.execute("""
                INSERT INTO sancion_jugador
                (ci_jugador, id_torneo, motivo,
                 numero_fecha_inicio, cantidad_fechas)
                VALUES (%s, %s, %s, %s, %s)
            """, (ci, torneo, "disciplinaria", fecha, cantidad))

            conexion.commit()
            print("Sanción disciplinaria agregada correctamente.")

        except mysql.connector.Error as error:
            conexion.rollback()
            print("Error:", error)

        finally:
            cursor.close()
            conexion.close()

    except ValueError:
        print("Debés ingresar números válidos.")


def modificar_sancion():
    try:
        id_sancion = int(input("ID de la sanción: "))

        conexion = conectar()
        cursor = conexion.cursor()

        try:
            cursor.execute("""
                SELECT motivo, id_torneo, numero_fecha_inicio
                FROM sancion_jugador
                WHERE id_sancion = %s
            """, (id_sancion,))

            sancion = cursor.fetchone()

            if sancion is None:
                print("La sanción no existe.")
                return

            motivo, torneo, fecha = sancion

            if motivo != "disciplinaria":
                print("No se pueden modificar sanciones automáticas.")
                return

            cantidad = int(input("Nueva cantidad de fechas: "))

            if cantidad <= 0:
                print("La cantidad debe ser mayor que cero.")
                return

            cursor.execute("""
                SELECT MAX(numero_fecha)
                FROM fecha_torneo
                WHERE id_torneo = %s
            """, (torneo,))

            ultima_fecha = cursor.fetchone()[0]

            if ultima_fecha is None or fecha + cantidad - 1 > ultima_fecha:
                print("La sanción supera las fechas registradas.")
                return

            cursor.execute("""
                UPDATE sancion_jugador
                SET cantidad_fechas = %s
                WHERE id_sancion = %s
            """, (cantidad, id_sancion))

            conexion.commit()
            print("Sanción modificada correctamente.")

        except mysql.connector.Error as error:
            conexion.rollback()
            print("Error:", error)

        finally:
            cursor.close()
            conexion.close()

    except ValueError:
        print("Debés ingresar números válidos.")


def eliminar_sancion():
    id_sancion = input("ID de la sanción a eliminar: ")

    conexion = conectar()
    cursor = conexion.cursor()

    try:
        cursor.execute("""
            SELECT motivo
            FROM sancion_jugador
            WHERE id_sancion = %s
        """, (id_sancion,))

        sancion = cursor.fetchone()

        if sancion is None:
            print("La sanción no existe.")
            return

        if sancion[0] != "disciplinaria":
            print("No se pueden eliminar sanciones automáticas.")
            return

        cursor.execute("""
            DELETE FROM sancion_jugador
            WHERE id_sancion = %s
        """, (id_sancion,))

        conexion.commit()
        print("Sanción eliminada correctamente.")

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
