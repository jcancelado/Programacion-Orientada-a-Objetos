## Tkinter: Stacked Frames (navegación sin nuevas ventanas)

### Objetivos (paso a paso)
- Cambiar de pantalla sin crear ventanas nuevas.
- Tratar cada pantalla como un `ttk.Frame` (vista).
- Usar `tkraise()` para mostrar la vista activa.

### Idea clave (imagen mental)
Tenemos varias “hojas” superpuestas en el mismo lugar. Levantamos la que queremos ver con `tkraise()`.

### Estructura (línea por línea)
```python
class App(tk.Tk):                       # Ventana principal que controla la navegación
    def __init__(self):
        super().__init__()
        container = ttk.Frame(self)     # Contenedor donde apilamos todas las vistas
        container.pack(fill="both", expand=True)
        self.frames = {}                # Diccionario: nombre_de_vista -> instancia
        for View in (HomeView, SettingsView):  # Lista de vistas de la app
            f = View(container, self)   # Creamos la vista pasando parent y controller
            self.frames[View.__name__] = f  # Guardamos para acceder luego
            f.grid(row=0, column=0, sticky="nsew")  # Todas en la misma celda

    def show_frame(self, name):         # Cambia la vista visible
        self.frames[name].tkraise()     # Sube esa “hoja” al frente
```

### ¿Qué es el "controller"? (App como orquestador)
- La `App` decide QUÉ vista mostrar y CUÁNDO.
- Las vistas NO cambian por sí solas: le piden a `controller` (la App) que cambie.
- Patrón útil: pasar `controller=self` al crear cada vista.

```python
f = View(container, self)   # self es la App → la vista puede llamar controller.show_frame("...")
```

### Interfaz mínima del controller (lo que ofrece la App)
- `show_frame(name: str)`: muestra la vista cuyo nombre se pasa.
- Opcionalmente podría ofrecer otros métodos (ej. guardar estado, cambiar tema, etc.).

```python
def show_frame(self, name: str):
    self.frames[name].tkraise()
```

### Detalle del bucle for (registrar vistas)
- Recorremos una TUPLA de clases de vistas.
- Instanciamos cada clase con `parent=container` y `controller=self`.
- Guardamos en `self.frames` usando como clave el nombre de la clase.

```python
for View in (HomeView, SettingsView, AboutView):
    instance = View(container, self)          # Crea la vista
    key = View.__name__                        # "HomeView", "SettingsView", ...
    self.frames[key] = instance                # Registra la instancia
    instance.grid(row=0, column=0, sticky="nsew")  # Misma celda para todas
```

### ¿Por qué usar `View.__name__` como clave?
- Es legible: coincide con el nombre de tu clase.
- Evita errores de strings sueltos; renombrar la clase mantiene la clave coherente.
- Alternativa: usar constantes o Enum si prefieres.

### ¿Cómo navega una vista? (desde dentro de un Frame)
```python
class HomeView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        ttk.Button(self, text="Ir a Settings",
                   command=lambda: controller.show_frame("SettingsView")).pack()
```

### Flujo de control (roles claros)
- La `App` decide qué vista se ve (controlador).
- Cada vista recibe `controller` para solicitar cambios de vista.

### Demo (correr)
```
python .\stacked_frames.py
```

### Actividad (guiada)
- Crear `FormView` con `Entry` de Nombre y Email y botón "Enviar".
- Desde `HomeView`, agregar botón "Ir a Form".
- En `FormView`, botón "Volver" que llame a `controller.show_frame("HomeView")`.

### Buenas prácticas (recordatorio)
- Evitar abrir nuevas ventanas por cada sección.
- Centralizar la navegación en `App` para mantener orden y pruebas más fáciles.


