# Short paper — Entrega 1

- `main.tex`: borrador IEEEtran (antes `paper_hasta_el_momento.md`, movido sin
  cambios de contenido el 2026-09-14).
- `referencias.bib`: siete entradas bibliográficas (añadidas el 2026-09-14),
  copia de las que están en Overleaf. `main.tex` cita hoy cinco de ellas
  (`baena2019red`, `parra2020analitica`, `grisales2022relacion`,
  `kleine2017modeling`, `ganan2026spatiotemporal`); `gomez2017contaminacion`
  y `joharestani2019pm25` están disponibles para trabajos relacionados.

Este directorio es el registro local de lo que hay en Overleaf: cuando se
cambie algo allí, copiarlo aquí en el mismo commit.

## Compilar

```bash
cd paper
latexmk -pdf main.tex
```

Requiere una distribución LaTeX con la clase `IEEEtran` y `babel` en
español. Los artefactos de compilación están excluidos de Git. En Overleaf
basta con subir `main.tex` y `referencias.bib`.

## Qué debe reflejar el texto

La guía de contenido por sección es [`../docs/entrega1_contenido.md`](../docs/entrega1_contenido.md);
la pregunta vigente y las cifras verificadas están en [`../context.md`](../context.md).
Toda cifra del paper debe existir en `notebooks/01_eda_pm25.ipynb`.
