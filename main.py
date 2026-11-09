
from funciones.equipos import menu_equipos
from funciones.jugadores import menu_jugadores
from funciones.partidos import menu_partidos, mostrar_partidos
from funciones.planillas import menu_planillas
from funciones.goles import menu_goles, mostrar_resultado
from funciones.tarjetas import menu_tarjetas
from funciones.usuarios import iniciar_sesion
from funciones.complejos import menu_complejos
from funciones.sanciones import menu_sanciones
from funciones.reportes import menu_reportes
from database import cambiar_rol, cerrar_sesion


def mostrar_menu():
    print("\n===== TORNEO INTERFACULTADES =====")
    print("1. Gestionar jugadores")
    print("2. Gestionar equipos")
    print("3. Gestionar partidos")
    print("4. Gestionar complejos y canchas")
    print("5. Gestionar sanciones")
    print("6. Ver reportes")
    print("7. Gestionar planillas")
    print("8. Gestionar goles")
    print("9. Gestionar tarjetas")
    print("0. Cerrar sesión")


def menu_planillero():
    while True:
        print("\n===== MENÚ PLANILLERO =====")
        print("1. Gestionar planillas")
        print("2. Gestionar goles")
        print("3. Gestionar tarjetas")
        print("0. Cerrar sesión")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            menu_planillas()

        elif opcion == "2":
            menu_goles()

        elif opcion == "3":
            menu_tarjetas()

        elif opcion == "0":
            print("Cerrando sesión...")
            break

        else:
            print("Opción inválida")


def main():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            menu_jugadores()

        elif opcion == "2":
            menu_equipos()

        elif opcion == "3":
            menu_partidos()

        elif opcion == "4":
            menu_complejos()

        elif opcion == "5":
            menu_sanciones()

        elif opcion == "6":
            menu_reportes()

        elif opcion == "7":
            menu_planillas()

        elif opcion == "8":
            menu_goles()

        elif opcion == "9":
            menu_tarjetas()

        elif opcion == "0":
            print("Cerrando sesión...")
            break

        else:
            print("Opción inválida")


def menu_publico():
    while True:
        print("\n===== CONSULTAR TORNEO =====")
        print("1. Ver partidos y fechas")
        print("2. Ver resultado de un partido")
        print("0. Volver")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            mostrar_partidos()

        elif opcion == "2":
            mostrar_resultado()

        elif opcion == "0":
            break

        else:
            print("Opción inválida")


if __name__ == "__main__":
    while True:
        print("\n===== TORNEO INTERFACULTADES =====")
        print("1. Iniciar sesión")
        print("2. Consultar torneo")
        print("0. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            rol = iniciar_sesion()

            if rol in ("administrador", "planillero"):
                if cambiar_rol(rol):
                    try:
                        if rol == "administrador":
                            main()

                        elif rol == "planillero":
                            menu_planillero()

                    finally:
                        cerrar_sesion()

        elif opcion == "2":
            menu_publico()

        elif opcion == "0":
            print("Saliendo del sistema...")
            break

        else:
            print("Opción inválida")


from funciones.equipos import menu_equipos
from funciones.jugadores import menu_jugadores
from funciones.partidos import menu_partidos, mostrar_partidos
from funciones.planillas import menu_planillas
from funciones.goles import menu_goles, mostrar_resultado
from funciones.tarjetas import menu_tarjetas
from funciones.usuarios import iniciar_sesion
from funciones.complejos import menu_complejos
from funciones.sanciones import menu_sanciones
from funciones.reportes import menu_reportes
from database import cambiar_rol, cerrar_sesion


def mostrar_menu():
    print("\n===== TORNEO INTERFACULTADES =====")
    print("1. Gestionar jugadores")
    print("2. Gestionar equipos")
    print("3. Gestionar partidos")
    print("4. Gestionar complejos y canchas")
    print("5. Gestionar sanciones")
    print("6. Ver reportes")
    print("7. Gestionar planillas")
    print("8. Gestionar goles")
    print("9. Gestionar tarjetas")
    print("0. Cerrar sesión")


def menu_planillero():
    while True:
        print("\n===== MENÚ PLANILLERO =====")
        print("1. Gestionar planillas")
        print("2. Gestionar goles")
        print("3. Gestionar tarjetas")
        print("0. Cerrar sesión")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            menu_planillas()

        elif opcion == "2":
            menu_goles()

        elif opcion == "3":
            menu_tarjetas()

        elif opcion == "0":
            print("Cerrando sesión...")
            break

        else:
            print("Opción inválida")


def main():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            menu_jugadores()

        elif opcion == "2":
            menu_equipos()

        elif opcion == "3":
            menu_partidos()

        elif opcion == "4":
            menu_complejos()

        elif opcion == "5":
            menu_sanciones()

        elif opcion == "6":
            menu_reportes()

        elif opcion == "7":
            menu_planillas()

        elif opcion == "8":
            menu_goles()

        elif opcion == "9":
            menu_tarjetas()

        elif opcion == "0":
            print("Cerrando sesión...")
            break

        else:
            print("Opción inválida")


def menu_publico():
    while True:
        print("\n===== CONSULTAR TORNEO =====")
        print("1. Ver partidos y fechas")
        print("2. Ver resultado de un partido")
        print("0. Volver")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            mostrar_partidos()

        elif opcion == "2":
            mostrar_resultado()

        elif opcion == "0":
            break

        else:
            print("Opción inválida")


if __name__ == "__main__":
    while True:
        print("\n===== TORNEO INTERFACULTADES =====")
        print("1. Iniciar sesión")
        print("2. Consultar torneo")
        print("0. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            rol = iniciar_sesion()

            if rol in ("administrador", "planillero"):
                if cambiar_rol(rol):
                    try:
                        if rol == "administrador":
                            main()

                        elif rol == "planillero":
                            menu_planillero()

                    finally:
                        cerrar_sesion()

        elif opcion == "2":
            menu_publico()

        elif opcion == "0":
            print("Saliendo del sistema...")
            break

        else:
            print("Opción inválida")

