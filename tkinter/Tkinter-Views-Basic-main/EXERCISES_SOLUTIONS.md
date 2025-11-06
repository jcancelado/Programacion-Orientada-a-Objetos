## Soluciones (instructor): Tkinter vistas reutilizables

Nota: Son referencias. Los estudiantes pueden implementar variantes válidas.

---

### Solución 1: Nueva vista en stacked frames (FormView)
Puntos clave:
- Crear clase `FormView(ttk.Frame)`.
- Añadirla al bucle de vistas en `App`.
- Agregar botón en `HomeView` para navegar.

Esqueleto sugerido:
```python
class FormView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.name_var = tk.StringVar()
        self.email_var = tk.StringVar()

        ttk.Label(self, text="Formulario", font=("Segoe UI", 14, "bold")).pack(pady=(16, 8))

        row = ttk.Frame(self); row.pack(padx=12, pady=4, fill='x')
        ttk.Label(row, text="Nombre:", width=10).pack(side='left')
        ttk.Entry(row, textvariable=self.name_var, width=30).pack(side='left')

        row2 = ttk.Frame(self); row2.pack(padx=12, pady=4, fill='x')
        ttk.Label(row2, text="Email:", width=10).pack(side='left')
        ttk.Entry(row2, textvariable=self.email_var, width=30).pack(side='left')

        actions = ttk.Frame(self); actions.pack(pady=8)
        ttk.Button(actions, text="Enviar", command=self._send).pack(side='left', padx=6)
        ttk.Button(actions, text="Volver", command=lambda: controller.show_frame("HomeView")).pack(side='left', padx=6)

    def _send(self):
        print("[Form]", {"name": self.name_var.get(), "email": self.email_var.get()})
```

En `App.__init__`:
```python
for ViewClass in (HomeView, SettingsView, AboutView, FormView):
    ...
```

En `HomeView` (botón extra):
```python
ttk.Button(nav, text="Ir a Form", command=lambda: controller.show_frame("FormView")).pack(side="left", padx=6)
```

---

### Solución 2: Validación mínima
Usar `trace_add` para actualizar el estado del botón:
```python
self.send_btn = ttk.Button(actions, text="Enviar", command=self._send)
self.send_btn.pack(side='left', padx=6)

def _update_state(*_):
    empty = self.name_var.get().strip() == "" or self.email_var.get().strip() == ""
    if empty:
        self.send_btn.state(["disabled"]) 
    else:
        self.send_btn.state(["!disabled"]) 

self.name_var.trace_add('write', _update_state)
self.email_var.trace_add('write', _update_state)
_update_state()
```

---

### Solución 3: Panel con "Noticias"
En `App.__init__` de `reusable_panel.py`, añadir botón y método:
```python
btn_news = ttk.Button(buttons, text="Mostrar Noticias", command=self._mostrar_noticias)
btn_news.pack(side="left", padx=6)

def _mostrar_noticias(self):
    self.panel.update_data("Noticias", "- Python 3.x lanzado\n- Tkinter tips\n- UI patterns")
```

---

### Solución 4: Estilos con ttk.Style
En `App.__init__`:
```python
style = ttk.Style(self)
style.configure('Title.TLabel', font=("Segoe UI", 13, 'bold'))
```
En `InfoPanel.__init__`:
```python
title_label = ttk.Label(self, textvariable=self.title_var, style='Title.TLabel')
```

---

### Solución 5: Botón Volver en FormView
Ya incluido en la Solución 1: botón con `command=lambda: controller.show_frame("HomeView")`.


