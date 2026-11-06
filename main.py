from funciones.equipos import menu_equipos
from funciones.jugadores import menu_jugadores
from funciones.partidos import menu_partidos

def mostrar_menu():
    print("\n===== TORNEO INTERFACULTADES =====")
    print("1. Gestionar jugadores")
    print("2. Gestionar equipos")
    print("3. Gestionar partidos")
    print("4. Gestionar complejos y canchas")
    print("5. Gestionar sanciones")
    print("6. Ver reportes")
    print("0. Salir")


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
            print("Gestión de complejos y canchas")

        elif opcion == "5":
            print("Gestión de sanciones")

        elif opcion == "6":
            print("Reportes")

        elif opcion == "0":
            print("Saliendo del sistema...")
            break

        else:
            print("Opción inválida")


if __name__ == "__main__":
    main()
