#José Luis Cancelado Castro
#Primera versión

#1. Estructura de control
#if, for, while, swicht, dowhile,
#Prueba
# calificacion 4.5 5 meritorio

nota = float(input("Escriba su calificación en formato numerico entre 0 y 5: "))

if(nota>=4.5 and nota<=5 ):
    print("Esta nota es meritoria")
elif(nota>5):
    print("Esta nota es mayor a la permitida, intentenlo nuevamente")
elif(nota<0):
    print("Esta nota es mayor a la permitida, intentenlo nuevamente")
else:
    print("Esta nota no es meritoria")

