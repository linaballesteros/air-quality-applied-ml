# Short paper — Entrega 1

- `main.tex`: borrador IEEEtran (antes `paper_hasta_el_momento.md`, movido sin
  cambios de contenido el 2026-09-14).
- `referencias.bib`: diez entradas. `main.tex` cita siete (`grisales2022relacion`,
  `parra2020analitica`, `baena2019red`, `minambiente2017resolucion2254`,
  `kleine2017modeling`, `siata2026pm25`, `siata2026meteo`); quedan sin usar
  `ganan2026spatiotemporal` (cita retirada por no tener fuente primaria
  archivada), `gomez2017contaminacion` y `joharestani2019pm25`.
- `figuras/`: PDF vectoriales exportados de los notebooks ejecutados
  (`distribucion_target` y `extension_eventos` de `01_eda_pm25.ipynb`;
  `importancia_shap` y `replica_baena` de la sección 14 de
  `02_modelado.ipynb`). Se dibujan al ancho real de
  una columna IEEE (3,5 pulgadas) para incluirlos sin reducir, así el texto
  de los ejes se mantiene nítido y legible.
- `figuras/diagramas/`: fuentes TikZ de los diagramas de flujo
  (`flujo_datos`, `flujo_metodologia`, `origen_movil`) y su estilo común.
  Se compilan con pdflatex y el PDF se mueve a `figuras/`:

  ```bash
  cd paper/figuras/diagramas
  for f in flujo_datos flujo_metodologia origen_movil; do
    pdflatex -interaction=nonstopmode $f.tex && mv $f.pdf ..
  done
  rm -f *.aux *.log
  ```

Este directorio es el registro local de lo que hay en Overleaf: cuando se
cambie algo allí, copiarlo aquí en el mismo commit.

## Compilar

```bash
cd paper
latexmk -pdf main.tex
```

Requiere una distribución LaTeX con la clase `IEEEtran`, `babel` en español y
los paquetes de tipografía `ebgaramond-maths` y `newtx` (ambos vienen en TeX
Live completo y en Overleaf). Los artefactos de compilación están excluidos de Git. En Overleaf
basta con subir `main.tex` y `referencias.bib`.

## Qué debe reflejar el texto

La guía de contenido por sección es [`../docs/entrega1_contenido.md`](../docs/entrega1_contenido.md);
la pregunta vigente y las cifras verificadas están en [`../context.md`](../context.md).
Toda cifra del paper debe existir en `notebooks/01_eda_pm25.ipynb` o en
`notebooks/02_modelado.ipynb`.

Borrador de la entrega final (2026-10-18): resumen, dos preguntas de
investigación y secciones VI–IX (metodología, resultados, discusión y
conclusiones). Compila sin errores en 8 páginas con referencias (unas 7,3
de contenido). Para Overleaf hay que subir `main.tex`, `referencias.bib`
(cinco entradas nuevas) y los cinco PDF nuevos de `figuras/`.
