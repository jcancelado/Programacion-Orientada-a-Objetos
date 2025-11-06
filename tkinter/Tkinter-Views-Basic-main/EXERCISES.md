## Ejercicios: Tkinter vistas reutilizables (estudiantes)

Duración sugerida: 45-60 min

Requisitos previos: haber ejecutado `stacked_frames.py` y `reusable_panel.py`.

---

### Ejercicio 1: Nueva vista en stacked frames
- Objetivo: añadir una vista `FormView` a `stacked_frames.py`.
- Contenido: dos `Entry` (Nombre, Email) y un botón "Enviar" que imprime en consola.
- Pistas:
  - Crea `class FormView(ttk.Frame)`.
  - Añádela al bucle que apila vistas en `App`.
  - Desde `HomeView`, añade un botón "Ir a Form".

### Ejercicio 2: Validación mínima
- Objetivo: en `FormView`, deshabilitar "Enviar" si nombre o email están vacíos.
- Pistas:
  - Usa `StringVar` y `trace_add('write', callback)` para actualizar estado.
  - Habilita/deshabilita con `button.state(['disabled'])` / `button.state(['!disabled'])`.

### Ejercicio 3: Panel reutilizable con una tercera sección
- Objetivo: en `reusable_panel.py`, agrega un botón "Noticias" que muestre 2-3 titulares.
- Pistas:
  - Crea método `_mostrar_noticias()` y llama a `self.panel.update_data()`.
  - Añade el botón al frame `buttons`.

### Ejercicio 4: Estilos con ttk.Style
- Objetivo: aplicar un estilo al título del `InfoPanel`.
- Pistas:
  - Crea `style = ttk.Style(self)` en `App`.
  - Define `style.configure('Title.TLabel', font=("Segoe UI", 13, 'bold'))`.
  - Aplica el estilo al label del título (`style='Title.TLabel'`).

### Ejercicio 5: Navegación de retorno
- Objetivo: en `stacked_frames.py`, desde `FormView` añade un botón "Volver" que regrese a `HomeView`.
- Pistas:
  - Recibir `controller` en el constructor y llamar `controller.show_frame("HomeView")`.

---

### Retos (opcional)
- Agrega un menú superior (menubar) con opciones para navegar entre vistas.
- Persiste las preferencias de `SettingsView` en un archivo JSON simple.
- Agrega atajos de teclado (p. ej., Ctrl+1 Home, Ctrl+2 Settings).

---

Cuando termines, ejecuta:
```
python .\stacked_frames.py
python .\reusable_panel.py
```


