# Presentación final

Presentación HTML de 19 diapositivas para 15 minutos de exposición y 5 de
preguntas: introducción y problema, datos, metodología y resultados.

## Presentar

Abrir `index.html` en Chrome, Edge o Firefox; funciona sin internet.

| Tecla | Acción |
| --- | --- |
| → · espacio · clic a la derecha | Siguiente paso o diapositiva |
| ← · clic a la izquierda | Anterior |
| F | Pantalla completa |
| Inicio · Fin | Primera y última diapositiva |

`index.html#7` abre directamente la diapositiva 7. Algunas diapositivas
revelan su contenido por pasos. `presentacion.pdf` es la versión en PDF, con
todos los pasos visibles. Para regenerarla: imprimir desde el navegador y
guardar como PDF (una diapositiva por página), o desde la raíz del
repositorio:

```bash
google-chrome --headless=new --no-pdf-header-footer --virtual-time-budget=5000 \
  --print-to-pdf=presentacion/presentacion.pdf "file://$PWD/presentacion/index.html"
```

## Archivos

- `index.html`: contenido, estilos y gráficos (SVG dibujado en el navegador).
- `datos.js`: todas las cifras de los gráficos y tablas. Lo genera la
  sección 13.1 de `notebooks/02_modelado.ipynb`; no se edita a mano.
- `fuentes.css`: Newsreader, Public Sans e IBM Plex Mono (Google Fonts,
  licencia SIL OFL) incrustadas en base64 para presentar sin conexión.
- `presentacion.pdf`: las diapositivas en PDF.

Las cifras escritas en el texto de las diapositivas vienen del mismo notebook
y coinciden con el paper.
