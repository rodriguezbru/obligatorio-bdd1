from funciones.equipos import menu_equipos
from funciones.jugadores import menu_jugadores
from funciones.partidos import menu_partidos
from funciones.planillas import menu_planillas
from funciones.goles import menu_goles
from funciones.tarjetas import menu_tarjetas
from funciones.usuarios import iniciar_sesion

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

        elif opcion == "7":
            menu_planillas()

        elif opcion == "8":
            menu_goles()

        elif opcion == "9":
            menu_tarjetas()

        elif opcion == "0":
            print("Saliendo del sistema...")
            break

        else:
            print("Opción inválida")

if __name__ == "__main__":
    rol = iniciar_sesion()

    if rol == "administrador":
        main()

    elif rol == "planillero":
        print("Bienvenido, planillero.")
        print("Próximamente: menú de planillas, goles y tarjetas.")