# Presentación final

Presentación HTML de 16 diapositivas para 15 minutos de exposición y 5 de
preguntas. Cada diapositiva es una afirmación (el título) y su evidencia (un
gráfico, un diagrama o una cifra), con el mínimo texto posible, como pidió el
profesor, y en lenguaje sencillo. Lo que se explica en voz alta está en el
guion de estudio, [`guion/guion.pdf`](guion/guion.pdf).

## Presentar

Abrir `index.html` en Chrome, Edge o Firefox; funciona sin internet.

| Tecla | Acción |
| --- | --- |
| → · espacio · clic a la derecha | Siguiente paso o diapositiva |
| ← · clic a la izquierda | Anterior |
| F | Pantalla completa |
| N | Notas del presentador, con cronómetro desde el primer avance |
| Inicio · Fin | Primera y última diapositiva |

`index.html#7` abre directamente la diapositiva 7. Algunas diapositivas
revelan su contenido por pasos (preguntas, diagrama de faltantes, cifras de
resultados y conclusiones). `presentacion.pdf` es la versión de respaldo, con todos los pasos visibles. Para
regenerarla: imprimir desde el navegador y guardar como PDF (una diapositiva
por página), o desde la raíz del repositorio:

```bash
google-chrome --headless=new --no-pdf-header-footer --virtual-time-budget=5000 \
  --print-to-pdf=presentacion/presentacion.pdf "file://$PWD/presentacion/index.html"
```

## Archivos

- `index.html`: contenido, estilos y gráficos (SVG dibujado en el navegador).
  Las notas cortas de cada diapositiva están en su `<aside class="notas">`.
- `guion/guion.tex` y `guion/guion.pdf`: guion de estudio. Trae la historia en
  un minuto, las cifras clave y un glosario sin tecnicismos. Para cada
  diapositiva incluye su miniatura, el tiempo, qué decir, la idea clave y
  cómo responder preguntas. Recoge los textos y notas que Lina redactó el
  2026-10-20. Las miniaturas salen de `presentacion.pdf`; si cambian las
  diapositivas, se regenera ese PDF y se compila con
  `cd presentacion/guion && latexmk -pdf guion.tex`.
- `presentacion.pdf`: respaldo en PDF de las diapositivas.
- `datos.js`: todas las cifras de los gráficos y tablas. Lo genera la
  sección 14.1 de `notebooks/02_modelado.ipynb`; no se edita a mano. Si
  cambian los resultados, se reejecuta el notebook y la presentación se
  actualiza sola.
- `fuentes.css`: Newsreader, Public Sans e IBM Plex Mono (Google Fonts,
  licencia SIL OFL) incrustadas en base64 para presentar sin conexión.

Las cifras escritas en el texto de las diapositivas (por ejemplo, los
intervalos de confianza) vienen del mismo notebook y coinciden con el paper.
