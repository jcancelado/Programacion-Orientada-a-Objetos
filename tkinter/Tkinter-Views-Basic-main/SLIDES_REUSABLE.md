## Tkinter: Panel reutilizable (misma vista, datos distintos)

### Objetivos (paso a paso)
- Comprender qué es un `Frame` y por qué lo usamos como “vista”.
- Ver cómo `StringVar` permite cambiar texto en pantalla sin recrear widgets.
- Distinguir responsabilidades: `App` controla; `InfoPanel` solo muestra.

### Idea clave (en simple)
Reutilizamos la misma “cajita” (`InfoPanel`) y solo cambiamos el texto que muestra. No creamos ventanas nuevas, no recreamos controles.

### Estructura (explicada línea por línea)
```python
class InfoPanel(ttk.Frame):          # Creamos un panel (vista) que hereda de ttk.Frame
    def __init__(self, parent):     # parent: quién contiene este panel (la App)
        super().__init__(parent)    # Inicializa el Frame de ttk
        self.title_var = tk.StringVar()  # Variable de texto: cambia y la etiqueta se actualiza sola
        self.body_var = tk.StringVar()   # Otra variable para el contenido principal
        ttk.Label(self, textvariable=self.title_var).pack()  # Muestra el título leyendo title_var
        ttk.Label(self, textvariable=self.body_var).pack()   # Muestra el cuerpo leyendo body_var

    def update_data(self, title, body): # Método “público” para cambiar lo que se ve
        self.title_var.set(title)        # Actualiza el título (la etiqueta cambia automáticamente)
        self.body_var.set(body)          # Actualiza el cuerpo
```

### Cómo lo usa la App
- La `App` crea UNA instancia de `InfoPanel` y la `pack()`ea.
- Cada botón llama a un método que ejecuta `panel.update_data(...)` con textos distintos.

### Demo (correr)
```
python .\reusable_panel.py
```

### Actividad (muy guiada)
- Crear botón “Noticias” que llame a un método `_mostrar_noticias()`.
- En ese método, llamar `self.panel.update_data("Noticias", "- Titular 1\n- Titular 2")`.
- Probar que la misma vista ahora muestra otra información.

### Bonus: estilos claros con `ttk.Style`
- Crear un estilo `Title.TLabel` con fuente más grande.
- Aplicarlo al label del título para diferenciarlo visualmente.

### Buenas prácticas (recordatorio)
- La vista NO decide qué mostrar: solo sabe cómo mostrarlo.
- El controlador (App) decide CUÁNDO y QUÉ contenido cargar.


