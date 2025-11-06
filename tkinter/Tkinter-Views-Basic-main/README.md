Tkinter Views Basic

Ejemplos didácticos para enseñar reutilización de vistas en una misma ventana con Tkinter (Python 3.10+). Incluye:

- stacked_frames.py: patrón de navegación con vistas apiladas (stacked frames)
- reusable_panel.py: un único panel reutilizable al que se le cambian los datos

Requisitos

- Python 3.10 o superior
- Tkinter viene incluido con la mayoría de instalaciones de Python en Windows/macOS. En Linux, instala el paquete de Tk.

Cómo ejecutar

En Windows (PowerShell) desde este directorio:

```
python .\stacked_frames.py
python .\reusable_panel.py
```

Qué enseñar con estos ejemplos

- Uso de `ttk.Frame` como "vista" y navegación con `tkraise()` (stacked frames).
- Separación entre controlador (la `App`) y vistas (`Frame`).
- Reutilización de un mismo `Frame` con diferentes datos (método `update_data`).
- Buenas prácticas básicas: `StringVar`/`BooleanVar`, `ttk` para apariencia nativa, y contenedores para layout.

