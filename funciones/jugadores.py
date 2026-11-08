import mysql.connector
from database import conectar

def agregar_jugador():
    ci = input("Cédula: ")
    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    email = input("Email: ")
    fecha = input("Fecha de nacimiento (AAAA-MM-DD): ")
    facultad = int(input("ID de facultad: "))
    tipo = input("Tipo (grado, posgrado, docente, funcionario): ")

    conexion = conectar()
    cursor = conexion.cursor()

    sql = """
    INSERT INTO jugador
    (ci, nombre, apellido, email, fecha_nacimiento, id_facultad, tipo)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    valores = (ci, nombre, apellido, email, fecha, facultad, tipo)

    cursor.execute(sql, valores)
    conexion.commit()

    print("Jugador agregado correctamente.")

    cursor.close()
    conexion.close()


def mostrar_jugadores():
    conexion = conectar()
    cursor = conexion.cursor()

    sql = """
    SELECT
        j.ci,
        j.nombre,
        j.apellido,
        j.email,
        j.fecha_nacimiento,
        f.nombre,
        j.tipo
    FROM jugador j
    JOIN facultad f
        ON j.id_facultad = f.id_facultad
    ORDER BY j.apellido, j.nombre
    """

    cursor.execute(sql)
    jugadores = cursor.fetchall()

    print("\n===== LISTA DE JUGADORES =====")

    for jugador in jugadores:
        ci, nombre, apellido, email, nacimiento, facultad, tipo = jugador

        print(f"\n{nombre} {apellido}")
        print(f"Cédula: {ci}")
        print(f"Email: {email}")
        print(f"Fecha de nacimiento: {nacimiento}")
        print(f"Facultad: {facultad}")
        print(f"Tipo: {tipo}")

    cursor.close()
    conexion.close()




def modificar_jugador():
    ci = input("Cédula del jugador a modificar: ")
    email = input("Nuevo email: ")

    conexion = conectar()
    cursor = conexion.cursor()

    sql = """
    UPDATE jugador
    SET email = %s
    WHERE ci = %s
    """

    cursor.execute(sql, (email, ci))
    conexion.commit()

    if cursor.rowcount > 0:
        print("Jugador modificado correctamente.")
    else:
        print("No se encontró el jugador.")

    cursor.close()
    conexion.close()


def eliminar_jugador():
    ci = input("Cédula del jugador a eliminar: ")

    conexion = conectar()
    cursor = conexion.cursor()

    try:
        sql = "DELETE FROM jugador WHERE ci = %s"
        cursor.execute(sql, (ci,))
        conexion.commit()

        if cursor.rowcount > 0:
            print("Jugador eliminado correctamente.")
        else:
            print("No se encontró el jugador.")

    except mysql.connector.Error:
        conexion.rollback()
        print("No se puede eliminar el jugador porque tiene registros asociados.")

    cursor.close()
    conexion.close()

def menu_jugadores():
    while True:
        print("\n===== GESTIÓN DE JUGADORES =====")
        print("1. Mostrar jugadores")
        print("2. Agregar jugador")
        print("3. Modificar jugador")
        print("4. Eliminar jugador")
        print("0. Volver")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            mostrar_jugadores()
        elif opcion == "2":
            agregar_jugador()
        elif opcion == "3":
            modificar_jugador()
        elif opcion == "4":
            eliminar_jugador()
        elif opcion == "0":
            break
        else:
            print("Opción inválida")
