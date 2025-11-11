import tkinter as tk
from tkinter import *
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hola Mundo")
        self.geometry("300x200")
        tk.Label(self, text="Hola Mundo").pack()
        self.bind('<Control-s>', lambda event: self.guardar())
    def guardar(self):
        print("si señorita directora")
if __name__ == "__main__":
    App().mainloop()