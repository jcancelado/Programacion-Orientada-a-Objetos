print("Este programa le permitira validar ingresar 3 coeficientes y determinar si su funcion cuadratica tiene soluciones o no")
numero1 = float(input("Ingrese el primer cociente(a) de su función cuadratica"))
numero2 = float(input("Ingrese el segundo cociente(b) de su función cuadratica"))
numero3 = float(input("Ingrese el tercer cociente(c) de su función cuadratica"))
discri =  0.5*(numero2**2+2*numero1*numero3)

def  discrimante (discri):
    if(discri>0):
        print("2 soluciones")
    elif(discri==0):
        print("1")
    else:
        print("no")
        return discri
print (discrimante(discri))
    