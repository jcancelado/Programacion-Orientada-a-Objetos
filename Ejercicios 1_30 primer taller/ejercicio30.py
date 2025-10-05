#Imprimir primos hasta el 50

for x in range (1,101):
    contador=0
    for i in range (1,x+1):
        if(x%i==0):
            contador = contador+1 
    if contador == 2 :
        print(x)
    else:
        continue
    
