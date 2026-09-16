# Short paper — Entrega 1

- `main.tex`: borrador IEEEtran (antes `paper_hasta_el_momento.md`, movido sin
  cambios de contenido el 2026-09-14).
- `referencias.bib`: diez entradas. `main.tex` cita siete (`grisales2022relacion`,
  `parra2020analitica`, `baena2019red`, `minambiente2017resolucion2254`,
  `kleine2017modeling`, `siata2026pm25`, `siata2026meteo`); quedan sin usar
  `ganan2026spatiotemporal` (cita retirada por no tener fuente primaria
  archivada), `gomez2017contaminacion` y `joharestani2019pm25`.
- `figuras/`: PNG exportados del notebook ejecutado (`distribucion_target`,
  `extension_eventos`).

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
