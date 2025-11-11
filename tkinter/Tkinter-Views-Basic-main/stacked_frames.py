import tkinter as tk  # Importa el módulo base de Tkinter para widgets clásicos
from tkinter import ttk  # Importa ttk para widgets con estilo nativo (mejor apariencia)


class App(tk.Tk):  # Define la aplicación principal heredando de tk.Tk (la ventana raíz)
    def __init__(self):  # Método de inicialización de la ventana
        super().__init__()  # Inicializa la clase base tk.Tk
        self.title("Demo: Vistas reutilizables con stacked frames")  # Título de la ventana
        self.geometry("420x260")  # Tamaño inicial de la ventana (ancho x alto)

        container = ttk.Frame(self)  # Crea un contenedor (panel) que guardará las vistas apiladas
        container.pack(fill="both", expand=True)  # Lo hace crecer para ocupar todo el espacio disponible

        # Diccionario para almacenar las vistas por nombre, útil para navegar entre ellas
        self.frames = {}

        # Lista de clases de vistas que queremos crear y apilar
        for ViewClass in (HomeView, SettingsView, AboutView, FormView):  # Itera sobre cada clase de vista
            view_instance = ViewClass(container, self)  # Instancia la vista; parent=container, controller=self
            name = ViewClass.__name__  # Obtiene el nombre de la clase (clave del diccionario)
            self.frames[name] = view_instance  # Guarda la instancia en el diccionario de vistas
            # Coloca cada vista en la misma celda (0,0) para poder alternarlas con tkraise()
            view_instance.grid(row=0, column=0, sticky="nsew")  # sticky="nsew" hace que se expanda en todas las direcciones

        self.show_frame("HomeView")  # Muestra la vista inicial al arrancar la app

    def show_frame(self, name: str):  # Método para cambiar de vista según su nombre
        frame = self.frames[name]  # Recupera la instancia de la vista del diccionario
        frame.tkraise()  # Eleva esa vista al frente (la hace visible sobre las demás)


class HomeView(ttk.Frame):  # Define la vista "Home" como un Frame estilizado (ttk.Frame)
    def __init__(self, parent, controller):  # parent=container, controller=instancia de App
        super().__init__(parent)  # Inicializa ttk.Frame con el contenedor como padre

        # Título de la vista Home
        title = ttk.Label(self, text="Home", font=("Segoe UI", 14, "bold"))  # Crea una etiqueta como título
        title.pack(pady=(16, 8))  # Empaqueta la etiqueta con separación vertical (arriba=16, abajo=8)

        # Texto de ejemplo en Home
        body = ttk.Label(self, text="Bienvenid@. Usa los botones para navegar entre vistas.")  # Mensaje informativo
        body.pack(pady=(0, 16))  # Empaqueta con separación inferior

        # Contenedor para los botones de navegación
        nav = ttk.Frame(self)  # Crea un frame para alinear los botones en una fila
        nav.pack(pady=4)  # Empaqueta el contenedor de botones

        # Botón: ir a Settings
        btn_settings = ttk.Button(
            nav,  # Padre: el contenedor de navegación
            text="Ir a Settings",  # Texto del botón
            command=lambda: controller.show_frame("SettingsView"),  # Acción: mostrar la vista Settings
        )
        btn_settings.pack(side="left", padx=6)  # Empaqueta el botón a la izquierda con espacio horizontal

        # Botón: ir a About
        btn_about = ttk.Button(
            nav,
            text="Ir a About",
            command=lambda: controller.show_frame("AboutView"),  # Acción: mostrar la vista About
        )
        btn_about.pack(side="left", padx=6)  # Empaqueta el botón a la izquierda con separación

        # Botón: ir a form
        btn_form = ttk.Button(
            nav,
            text="Ir a Form",
            command=lambda: controller.show_frame("FormView"),  # Acción: mostrar la vista About
        )
        btn_form.pack(side="left", padx=6)  # Empaqueta el botón a la izquierda con separación


class SettingsView(ttk.Frame):  # Define la vista "Settings"
    def __init__(self, parent, controller):  # parent=container, controller=App
        super().__init__(parent)  # Inicializa ttk.Frame

        title = ttk.Label(self, text="Settings", font=("Segoe UI", 14, "bold"))  # Título
        title.pack(pady=(16, 8))  # Empaqueta con espacio vertical

        # Un par de controles de ejemplo: una casilla y un combo
        self.dark_mode = tk.BooleanVar(value=False)  # Variable booleana para el estado de un checkbutton
        chk = ttk.Checkbutton(self, text="Modo oscuro (simulado)", variable=self.dark_mode)  # Checkbutton enlazado a la variable
        chk.pack(anchor="w", padx=16, pady=4)  # Alinea a la izquierda con relleno

        ttk.Label(self, text="Tamaño de fuente:").pack(anchor="w", padx=16, pady=(12, 4))  # Etiqueta para el combo

        self.font_size = tk.StringVar(value="Mediana")  # Variable de texto para el combobox
        cmb = ttk.Combobox(self, textvariable=self.font_size, values=["Pequeña", "Mediana", "Grande"], state="readonly")  # Combo de solo lectura
        cmb.pack(anchor="w", padx=16, pady=(0, 12))  # Alinea a la izquierda

        # Botones de navegación al final
        nav = ttk.Frame(self)  # Contenedor de botones
        nav.pack(pady=6)  # Empaqueta el contenedor

        ttk.Button(nav, text="Guardar", command=self._guardar).pack(side="left", padx=6)  # Botón que invoca un método de la vista
        ttk.Button(nav, text="Volver a Home", command=lambda: controller.show_frame("HomeView")).pack(side="left", padx=6)  # Regresa a Home

    def _guardar(self):  # Método "privado" para simular guardado de ajustes
        # Aquí iría la lógica real de guardado; por ahora mostramos por consola
        print("[Settings] Guardado:", {
            "modo_oscuro": self.dark_mode.get(),  # Lee la variable booleana del checkbutton
            "tamanio_fuente": self.font_size.get(),  # Lee el valor seleccionado del combobox
        })


class AboutView(ttk.Frame):  # Define la vista "About"
    def __init__(self, parent, controller):  # parent=container, controller=App
        super().__init__(parent)  # Inicializa ttk.Frame

        title = ttk.Label(self, text="About", font=("Segoe UI", 14, "bold"))  # Título de la vista
        title.pack(pady=(16, 8))  # Empaqueta con separación

        # Texto informativo
        info = (
            "Este ejemplo usa el patrón 'stacked frames':\n"
            "- Todas las vistas son ttk.Frame.\n"
            "- Se colocan en la misma celda del grid.\n"
            "- Cambiamos la vista activa con tkraise()."
        )
        ttk.Label(self, text=info, justify="left").pack(padx=16, pady=8)  # Etiqueta multilínea alineada a la izquierda

        # Botón para volver a Home
        ttk.Button(self, text="Volver a Home", command=lambda: controller.show_frame("HomeView")).pack(pady=6)  # Regresa a Home


class FormView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        ttk.Label(self, text="Formulario", font=("arial", 14, "bold")).grid(row=0, column=0, columnspan=5, pady=(16, 8))

        # Variables de entrada
        self.var_nom = tk.StringVar()
        self.var_correo = tk.StringVar()

        # Cada vez que cambie el contenido, se llama a self._verificar_campos
        self.var_nom.trace_add("write", self._verificar_campos)
        self.var_correo.trace_add("write", self._verificar_campos)

        # Etiquetas y entradas
        ttk.Label(self, text="Nombre", font=("arial", 10, "bold")).grid(row=1, column=1)
        ttk.Entry(self, textvariable=self.var_nom).grid(row=2, column=1)

        ttk.Label(self, text="Correo", font=("arial", 10, "bold")).grid(row=1, column=2)
        ttk.Entry(self, textvariable=self.var_correo).grid(row=2, column=2)

        # Botones
        self.boton_enviar = ttk.Button(self, text="Enviar", command=self._enviar, state="disabled")  # <- deshabilitado al inicio
        self.boton_enviar.grid(row=3, column=1, pady=16)

        ttk.Button(self, text="Volver a Home",
                   command=lambda: controller.show_frame("HomeView")).grid(row=3, column=2, pady=16)

    def _verificar_campos(self, *args):
        """Habilita el botón si ambos campos tienen texto."""
        if self.var_nom.get().strip() and self.var_correo.get().strip():
            self.boton_enviar.state(["!disabled"])  # habilita
        else:
            self.boton_enviar.state(["disabled"])  # deshabilita

    def _enviar(self):
        print("Formulario enviado, nombre:", self.var_nom.get(), "correo:", self.var_correo.get())



if __name__ == "__main__":  # Punto de entrada del script
    app= App()
    app.mainloop()  # Crea la app y entra en el bucle principal de eventos de Tkinter


