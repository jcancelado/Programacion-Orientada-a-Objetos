numero = int(input("Ingrese un numero entero para ver sus numeros impares menores que el"))
if(numero%2==0):
    for x in range(0,numero):
        restasacaimp = numero - x
        if(restasacaimp%2==0):
          continue
        else:
                print(restasacaimp)
else:
    for x in range(0,numero):
        restasacaimp = numero - x
        if(restasacaimp%2==0):
          continue

        else:
                print(restasacaimp)



