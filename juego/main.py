import tkinter as tk
import random

root = tk.Tk()
root.title("Game")
root.geometry("900x700")


# ============================================================
#   Cargar imágenes (RUTAS COMPLETAS)
# ============================================================
lux = tk.PhotoImage(file=r"C:/Users/Estudiante/Documents/Programacion Orientada a Objetos/juego/img/lux-emote.gif")
yasuo = tk.PhotoImage(file=r"C:/Users/Estudiante/Documents/Programacion Orientada a Objetos/juego/img/yasuo.png")
ezreal = tk.PhotoImage(file=r"C:/Users/Estudiante/Documents/Programacion Orientada a Objetos/juego/img/Ezreal.png")
jinx = tk.PhotoImage(file=r"C:/Users/Estudiante/Documents/Programacion Orientada a Objetos/juego/img/jinx.png")
poppy = tk.PhotoImage(file=r"C:/Users/Estudiante/Documents/Programacion Orientada a Objetos/juego/img/poppy.png")
cait = tk.PhotoImage(file=r"C:/Users/Estudiante/Documents/Programacion Orientada a Objetos/juego/img/caytlin.png")


personajes = [
    {"nombre": "Lux", "imagen": lux},
    {"nombre": "Yasuo", "imagen": yasuo},
    {"nombre": "Ezreal", "imagen": ezreal},
    {"nombre": "Jinx", "imagen": jinx},
    {"nombre": "Poppy", "imagen": poppy},
    {"nombre": "Caitlyn", "imagen": cait},
]


# ============================================================
#   ÁREA DE SELECCIÓN
# ============================================================

frame_select = tk.Frame(root)
frame_select.pack(pady=20)

tk.Label(frame_select, text="Selecciona Jugador 1").grid(row=0, column=0)
tk.Label(frame_select, text="Selecciona Jugador 2").grid(row=0, column=1)

jugador1 = None
jugador2 = None


def seleccionar(jugador, personaje):
    global jugador1, jugador2

    if jugador == 1:
        jugador1 = personaje
    else:
        jugador2 = personaje

    actualizar_info()


def actualizar_info():
    if jugador1 and jugador2:
        info.config(text=f"{jugador1['nombre']}   VS   {jugador2['nombre']}")
    elif jugador1:
        info.config(text=f"Jugador 1: {jugador1['nombre']}")
    elif jugador2:
        info.config(text=f"Jugador 2: {jugador2['nombre']}")


# ============================================================
#   Crear botones de selección en 2 columnas
# ============================================================
for i, pj in enumerate(personajes):
    # columna izquierda = jugador 1
    tk.Button(
        frame_select,
        image=pj["imagen"],
        command=lambda p=pj: seleccionar(1, p),
        width=150,
        height=150
    ).grid(row=i + 1, column=0, padx=10, pady=5)

    # columna derecha = jugador 2
    tk.Button(
        frame_select,
        image=pj["imagen"],
        command=lambda p=pj: seleccionar(2, p),
        width=150,
        height=150
    ).grid(row=i + 1, column=1, padx=10, pady=5)


# ============================================================
#   Info visual
# ============================================================
info = tk.Label(root, text="Selecciona Personajes", font=("Arial", 20))
info.pack(pady=20)


root.mainloop()
