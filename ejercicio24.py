print("Este programa le permitira validar ingresar 3 coeficientes y determinar si su funcion cuadratica tiene soluciones o no")
numero1 = float(input("Ingrese el primer cociente(a) de su función cuadratica"))
numero2 = float(input("Ingrese el segundo cociente(b) de su función cuadratica"))
numero3 = float(input("Ingrese el tercer cociente(c) de su función cuadratica"))


if(numero1>numero2):
    print("El número ",numero1," es mayor que ",numero2)
elif(numero2 == numero1):
    print("El número ",numero1," es igual que ",numero2)
else: 
    print("El número ",numero2," es mayor que ",numero1)