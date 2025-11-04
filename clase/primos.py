#Autor: Gabriel Cely
#Ejercicio
#Mostrar los primeros 30 números primos 

for i in range(0,108):
    if (i%2!=0 and i%3!=0 and i%5!=0 and i%7!=0) or i==2 or i==3 or i==5 or i==7:
        print(i)