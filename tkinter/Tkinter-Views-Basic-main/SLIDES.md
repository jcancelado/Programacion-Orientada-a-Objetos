## Clase: Reutilizar vistas en Tkinter (primer curso)

### 1. Objetivos
- Entender `Frame` como "vista" reutilizable.
- Navegar entre vistas sin abrir nuevas ventanas (stacked frames).
- Reutilizar un mismo panel con datos distintos.

### 2. ¿Por qué `ttk`?
- Apariencia nativa del sistema.
- Misma API básica que Tk, pero con estilos.

### 3. Estructura base
```python
import tkinter as tk
from tkinter import ttk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mi App")
```

### 4. Patrón: Stacked Frames (una ventana, múltiples vistas)
Idea: todas las vistas (frames) ocupan la misma celda del grid; mostramos una con `tkraise()`.

Pasos:
- Crear `container = ttk.Frame(self)` y usar `grid` o `pack` para expandir.
- Crear un diccionario `self.frames` para registrar vistas.
- Para cada clase de vista: instanciar, `grid(row=0, column=0, sticky="nsew")`.
- Cambiar de vista con `frame.tkraise()`.

Ver archivo `stacked_frames.py` (líneas comentadas).

### 5. Patrón: Un panel reutilizable (misma vista, datos distintos)
Idea: un `ttk.Frame` con `StringVar` que cambiamos por código.

Pasos:
- Crear clase `InfoPanel(ttk.Frame)` con `title_var` y `body_var`.
- Método `update_data(title, body)` para setear el contenido.
- Botones que llaman a métodos que cambian el contenido del panel.

Ver archivo `reusable_panel.py` (líneas comentadas).

### 6. Buenas prácticas didácticas
- Separar "controlador" (la `App`) de las vistas.
- Usar variables de Tk (`StringVar`, `BooleanVar`) para enlazar estado.
- Mantener funciones pequeñas y con nombres claros.

### 7. Ejecución (Windows PowerShell)
```
python .\stacked_frames.py
python .\reusable_panel.py
```

### 8. Actividad guiada (rápida)
- Añade una vista nueva a `stacked_frames.py` con un formulario simple (nombre/email).
- Añade un tercer contenido al `InfoPanel` llamado "Noticias" con 2-3 líneas.

### 9. Evaluación
- ¿Cuándo conviene stacked frames vs. panel reutilizable?
- ¿Cómo separar responsabilidades entre vistas y la `App`?


