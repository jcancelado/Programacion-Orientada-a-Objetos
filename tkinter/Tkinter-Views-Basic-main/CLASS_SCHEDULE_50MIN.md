## Clase de 50 minutos: Tkinter y vistas reutilizables

Duración total: 50 min

1) Apertura y objetivos (5 min)
- Presentar qué es Tkinter y por qué usar `ttk`.
- Meta: una ventana, varias vistas; panel reutilizable.

2) Stacked Frames (15 min)
- Explicar el patrón (una celda del grid; `tkraise()`).
- Demo rápida con `stacked_frames.py` (Home → Settings → About).
- Preguntas guiadas: ¿ventajas de no abrir nuevas ventanas?

3) Panel reutilizable (10 min)
- Explicar `StringVar` y método `update_data(...)`.
- Demo con `reusable_panel.py` (Perfil/Ayuda/Acerca de).

4) Ejercicio en vivo (10 min)
- Añadir una vista simple de formulario en `stacked_frames.py` O
- Añadir "Noticias" al `InfoPanel`.
- Validación mínima opcional (deshabilitar botón si hay campos vacíos).

5) Cierre y próximos pasos (10 min)
- Buenas prácticas: separación App/Vistas, uso de variables de Tk, estilos con `ttk.Style`.
- Asignar `EXERCISES.md` como práctica y mencionar soluciones para docentes.

Material de apoyo:
- `SLIDES.md` para la explicación.
- `EXERCISES.md` (alumnos) y `EXERCISES_SOLUTIONS.md` (docente).


