import tkinter as tk  # Importa Tkinter base para variables (StringVar) y utilidades
from tkinter import ttk  # Importa ttk para widgets modernos con estilos nativos


class InfoPanel(ttk.Frame):  # Un panel reutilizable que muestra un título y un cuerpo de texto
    def __init__(self, parent):  # parent es el contenedor donde se insertará este panel
        super().__init__(parent)  # Inicializa el Frame con estilos ttk

        # Variables de estado que controlan el contenido mostrado
        self.title_var = tk.StringVar(value="Título")  # Variable de texto para el encabezado
        self.body_var = tk.StringVar(value="Contenido del panel...")  # Variable de texto para el cuerpo

        # Widgets que leen automáticamente las variables anteriores
        title_label = ttk.Label(self, textvariable=self.title_var, font=("Segoe UI", 12, "bold"))  # Etiqueta grande para el título
        title_label.pack(anchor="w", pady=(0, 4))  # Alinea a la izquierda y añade espacio inferior

        body_label = ttk.Label(self, textvariable=self.body_var, wraplength=360, justify="left")  # Etiqueta para el cuerpo con ajuste de línea
        body_label.pack(anchor="w")  # Alinea a la izquierda

    def update_data(self, title: str, body: str):  # Método para actualizar el contenido del panel
        self.title_var.set(title)  # Cambia el texto del título
        self.body_var.set(body)  # Cambia el texto del cuerpo


class App(tk.Tk):  # Ventana principal de la aplicación
    def __init__(self):  # Inicializador de la app
        super().__init__()  # Inicializa tk.Tk
        self.title("Panel reutilizable (misma vista, datos diferentes)")  # Título de la ventana
        self.geometry("480x300")  # Tamaño de la ventana

        # Crea una instancia del panel reutilizable y la coloca
        self.panel = InfoPanel(self)  # Panel que se reconfigurará según el botón que el usuario pulse
        self.panel.pack(fill="both", expand=True, padx=12, pady=12)  # Ocupa el espacio disponible con márgenes

        # Fila de botones para cargar distintos datos en el mismo panel
        buttons = ttk.Frame(self)  # Contenedor para los botones de acciones
        buttons.pack(pady=(0, 8))  # Lo coloca debajo del panel con un poco de espacio

        # Botón 1: Carga datos de "Perfil"
        btn_perfil = ttk.Button(
            buttons,  # Padre: frame de botones
            text="Mostrar Perfil",  # Texto del botón
            command=self._mostrar_perfil,  # Acción para actualizar el panel con datos de perfil
        )
        btn_perfil.pack(side="left", padx=6)  # Coloca el botón a la izquierda con separación

        # Botón 2: Carga datos de "Ayuda"
        btn_ayuda = ttk.Button(
            buttons,
            text="Mostrar Ayuda",
            command=self._mostrar_ayuda,  # Acción para actualizar el panel con datos de ayuda
        )
        btn_ayuda.pack(side="left", padx=6)  # Coloca el botón a la izquierda con separación

        # Botón 3: Carga datos de "Acerca de"
        btn_about = ttk.Button(
            buttons,
            text="Mostrar Acerca de",
            command=self._mostrar_about,  # Acción para actualizar el panel con datos de about
        )
        btn_about.pack(side="left", padx=6)  # Coloca el botón a la izquierda con separación

        # Establece un contenido inicial para el panel al arrancar
        self._mostrar_perfil()  # Carga el perfil por defecto para que el panel no esté vacío

    # A partir de aquí, métodos que "inyectan" diferentes datos en el mismo InfoPanel
    def _mostrar_perfil(self):  # Actualiza el panel con información tipo "Perfil"
        titulo = "Perfil"
        cuerpo = (
            "Nombre: Ana López\n"
            "Rol: Estudiante\n"
            "Intereses: Python, diseño de UI"
        )
        self.panel.update_data(titulo, cuerpo)  # Pasa los datos al panel reutilizable

    def _mostrar_ayuda(self):  # Actualiza el panel con información de "Ayuda"
        titulo = "Ayuda"
        cuerpo = (
            "- Usa los botones para cambiar el contenido.\n"
            "- Este panel es el mismo; solo cambian los datos."
        )
        self.panel.update_data(titulo, cuerpo)  # Actualiza el panel con el nuevo contenido

    def _mostrar_about(self):  # Actualiza el panel con información de "Acerca de"
        titulo = "Acerca de"
        cuerpo = (
            "Ejemplo de reutilización de vistas en Tkinter:\n"
            "Un único ttk.Frame (InfoPanel) que se reconfigura por código."
        )
        self.panel.update_data(titulo, cuerpo)  # Actualiza el panel con el contenido de about


if __name__ == "__main__":  # Punto de entrada del script
    App().mainloop()  # Inicia el bucle principal de eventos de Tkinter


