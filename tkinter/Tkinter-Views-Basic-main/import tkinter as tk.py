import tkinter as tk
from tkinter import ttk, messagebox
import firebase_admin
from firebase_admin import credentials, db

# --- Configurar Firebase ---
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://TU_PROYECTO.firebaseio.com/"
})
ref = db.reference("/usuarios")


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Usuarios Firebase")
        self.geometry("400x300")

        ttk.Label(self, text="Nombre:").pack(pady=5)
        self.nombre = tk.StringVar()
        ttk.Entry(self, textvariable=self.nombre).pack()

        ttk.Label(self, text="Edad:").pack(pady=5)
        self.edad = tk.StringVar()
        ttk.Entry(self, textvariable=self.edad).pack()

        ttk.Button(self, text="Guardar", command=self.guardar).pack(pady=10)
        ttk.Button(self, text="Mostrar todos", command=self.mostrar).pack()

    def guardar(self):
        nombre = self.nombre.get()
        edad = self.edad.get()
        if nombre and edad:
            ref.push({"nombre": nombre, "edad": edad})
            messagebox.showinfo("Éxito", "Usuario guardado")
        else:
            messagebox.showwarning("Atención", "Completa todos los campos")

    def mostrar(self):
        usuarios = ref.get()
        print("Usuarios en Firebase:")
        for k, v in usuarios.items():
            print(f"- {v['nombre']} ({v['edad']} años)")


if __name__ == "__main__":
    App().mainloop()
