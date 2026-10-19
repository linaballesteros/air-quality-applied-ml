# Presentación final

Presentación HTML de 19 diapositivas para 15 minutos de exposición y 5 de
preguntas. Bloques: introducción y datos (Lina), metodología y resultados
(Alejandro).

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
revelan su contenido por pasos (diagrama de faltantes, preguntas,
conclusiones). Para un PDF de respaldo: imprimir desde el navegador y
guardar como PDF; sale una diapositiva por página, con todos los pasos
visibles.

## Archivos

- `index.html`: contenido, estilos y gráficos (SVG dibujado en el navegador).
  Las notas de cada diapositiva están en su `<aside class="notas">`.
- `datos.js`: todas las cifras de los gráficos y tablas. Lo genera la
  sección 14.1 de `notebooks/02_modelado.ipynb`; no se edita a mano. Si
  cambian los resultados, se reejecuta el notebook y la presentación se
  actualiza sola.
- `fuentes.css`: Newsreader, Public Sans e IBM Plex Mono (Google Fonts,
  licencia SIL OFL) incrustadas en base64 para presentar sin conexión.

Las cifras escritas en el texto de las diapositivas (por ejemplo, los
intervalos de confianza) vienen del mismo notebook y coinciden con el paper.
