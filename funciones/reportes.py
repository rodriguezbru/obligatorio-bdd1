
from database import conectar
from pathlib import Path


def ejecutar_reporte(titulo, consulta):
    conexion = conectar()
    cursor = conexion.cursor()

    try:
        cursor.execute(consulta)
        resultados = cursor.fetchall()
        columnas = [columna[0] for columna in cursor.description]

        print("\n===== " + titulo.upper() + " =====")
        print(" | ".join(columnas))
        print("-" * 70)

        if len(resultados) == 0:
            print("No se encontraron resultados")
        else:
            for fila in resultados:
                print(" | ".join(str(dato) for dato in fila))

    except Exception as error:
        print("Error al ejecutar el reporte:", error)

    finally:
        cursor.close()
        conexion.close()


def cargar_consultas():
    ruta = Path(__file__).resolve().parent.parent / "04_reportes.sql"

    with open(ruta, "r", encoding="utf-8-sig") as archivo:
        contenido = archivo.read()

    consultas = []

    for parte in contenido.split(";"):
        consulta = parte.strip()

        if consulta and not consulta.upper().startswith("USE "):
            consultas.append(consulta)

    return consultas


def menu_reportes():
    reportes = {
        "1": ("Top 10 goleadores", 0),
        "2": ("Tabla de posiciones", 2),
        "3": ("Fair Play", 3),
        "4": ("Promedio de goles por fecha", 4),
        "5": ("Promedio de goles por edición", 5),
        "6": ("Canchas más utilizadas", 6),
        "7": ("Turnos más utilizados", 7),
        "8": ("Jugadores por facultad y tipo", 8),
        "9": ("Jugadores que nunca participaron", 9),
        "10": ("Sanciones por equipo y motivo", 10),
        "11": ("Porcentaje de partidos por estado", 11),
        "12": ("Resultados de partidos", 12),
        "13": ("Equipos invictos", 13),
        "14": ("Partidos jugados por equipo", 14),
        "15": ("Jugadores con más tarjetas", 15)
    }

    try:
        consultas = cargar_consultas()
    except Exception as error:
        print("No se pudo leer 04_reportes.sql:", error)
        return

    if len(consultas) != 16:
        print("Error: se esperaban 16 consultas en 04_reportes.sql.")
        print("Se encontraron:", len(consultas))
        return

    while True:
        print("\n===== REPORTES DEL TORNEO =====")

        for numero, datos in reportes.items():
            print(numero + ". " + datos[0])

        print("0. Volver")

        opcion = input("Seleccione una opción: ")

        if opcion == "0":
            break

        elif opcion in reportes:
            titulo, indice = reportes[opcion]
            ejecutar_reporte(titulo, consultas[indice])

        else:
            print("Opción inválida")
