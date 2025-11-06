## Exportar SLIDES.md a PDF (Windows)

Opción A) Con Pandoc (recomendado)
1. Instalar Pandoc y un motor LaTeX (TinyTeX):
   - Descarga Pandoc: `https://github.com/jgm/pandoc/releases`
   - (Opcional) TinyTeX: abre PowerShell como admin y ejecuta:
     ```powershell
     iwr -useb https://yihui.org/tinytex/install-windows.ps1 | iex
     ```
2. Desde la carpeta del proyecto, ejecutar:
   ```powershell
   pandoc .\SLIDES.md -o .\SLIDES.pdf --pdf-engine=xelatex
   ```

Opción B) A HTML e imprimir a PDF
```powershell
pandoc .\SLIDES.md -o .\SLIDES.html
start .\SLIDES.html
```
Luego usa "Imprimir" → "Microsoft Print to PDF".

Notas
- Si no tienes un motor LaTeX, Pandoc puede advertir; usa la Opción B.
- Para mejores fuentes, instala `Segoe UI` (Windows) o ajusta el CSS/tema.


