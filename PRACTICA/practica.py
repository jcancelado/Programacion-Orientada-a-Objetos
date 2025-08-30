opcion = int(input("Ingrese un número (1-3): "))

match opcion:
    case 1:
        print("Elegiste la opción 1")
    case 2:
        print("Elegiste la opción 2")
    case 3:
        print("Elegiste la opción 3")
    case _:
        print("Opción no válida")
