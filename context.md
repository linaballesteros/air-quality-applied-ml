# Contexto vivo — predicción de PM2.5 en el Valle de Aburrá

Este archivo es la fuente de verdad operativa del repositorio. Debe
actualizarse al cerrar cada tarea que cambie datos, decisiones o estado del
proyecto. El planteamiento extenso inicial se conserva en
[`docs/context_legacy.md`](docs/context_legacy.md).

## Proyecto

| Campo | Estado vigente |
| --- | --- |
| Curso | Aprendizaje de Máquina Aplicado — ST1631, Universidad EAFIT |
| Integrantes | Lina Sofía Ballesteros Merchán y Alejandro Ríos Muñoz |
| Entrega | Short-Paper — Entrega 1 |
| Título tentativo | Predicción de concentraciones de PM2.5 en el Valle de Aburrá mediante aprendizaje automático con datos de la red SIATA |
| Problema ML | Aprendizaje supervisado de regresión |
| Pregunta | ¿Es posible predecir, con una hora de anticipación, la concentración de PM2.5 en estaciones seleccionadas del Valle de Aburrá usando mediciones históricas del contaminante y variables temporales mediante modelos supervisados de regresión? |

## Reglas de trabajo

- Distinguir siempre hechos verificados, propuestas y pendientes.
- Toda cifra del paper debe reproducirse en un notebook o script.
- No imputar nulos, eliminar extremos ni interpretar ceros sin evidencia.
- No unir fuentes sin comprobar estación, fecha-hora, frecuencia y zona
  horaria.
- Los cambios metodológicos se registran en [`docs/decisions.md`](docs/decisions.md).
- Los PDFs convertidos para consulta están en [`docs/sources`](docs/sources/);
  las citas finales deben verificarse en los originales.

## Requisitos verificados de Entrega 1

Fuente: [`docs/sources/shortpaper_entrega1_requisitos.md`](docs/sources/shortpaper_entrega1_requisitos.md).

- Paper IEEE de 3–5 páginas, sin contar referencias, con al menos tres fuentes.
- PDF y notebook de EDA o enlace público al repositorio.
- Introducción de 300–500 palabras y trabajos relacionados de 150–250
  palabras con 2–4 referencias.
- Caracterización explícita de fuente, tamaño, granularidad y target.
- Notebook con carga/limpieza, descriptivos, nulos, duplicados, outliers y
  visualizaciones explicadas.
- Paper con solo 2–3 hallazgos respaldados exactamente por el notebook.

## Fuente de datos verificada

| Propiedad | Evidencia |
| --- | --- |
| Dataset | SIATA, *Histórico de Material Particulado - PM2.5*, DOI `10.83041/AUWZWT` |
| Versión | 4.0, publicada el 25 de agosto de 2026 |
| Catálogo | 162 archivos mensuales, aproximadamente 14,6 MB |
| Periodo publicado | Enero de 2013 a junio de 2026 |
| Descarga | `python scripts/download_pm25_dataset.py --all` |
| Almacenamiento | `data/raw/pm25/`, excluido de Git y validado con MD5 oficial |

El archivo original tiene extensión `.tab`, pero la muestra de enero de 2013
usa comas. El loader detecta delimitador y codificación; no los supone.

## Perfil completo verificado

Ejecutar `python scripts/profile_pm25.py` para reproducirlo.

| Pregunta | Resultado |
| --- | --- |
| ¿Qué representa una fila? | Una hora. Cada columna de estación contiene su medición de PM2.5 para esa hora. |
| Granularidad | Horaria, sin huecos en el índice global. |
| Rango | 2013-01-01 00:00 a 2026-06-30 23:00. |
| Filas | 118.296. |
| Estaciones | 33 códigos históricos. |
| Schema | 30 variantes por altas, retiros y cambios de estaciones. |
| Variable objetivo | No hay una única columna target: los datos vienen en formato ancho, una columna por estación. |
| Mediciones no nulas | 1.879.277. |
| Duplicados | 0 filas y 0 timestamps duplicados. |
| Horas globales ausentes | 0. |
| Horas sin ninguna medición | 47. |
| Valores negativos | 0. |
| Valores iguales a cero | 5.036; significado pendiente de validar. |

La cantidad de celdas vacías sobre la unión de las 33 estaciones no representa
una tasa directa de falla, porque incluye periodos anteriores a la instalación
o posteriores al retiro de estaciones. La cobertura debe calcularse dentro
del periodo activo o de una ventana común.

## Formulación definida para la Entrega 1

- **Unidad de observación analítica:** una estación en una hora `t`.
- **Target:** `pm25_t_plus_1`, concentración de PM2.5 de esa estación en la
  hora siguiente; variable numérica continua en µg/m³.
- **Predictores disponibles:** PM2.5 observado hasta `t`, código de estación y
  variables temporales derivadas de `fecha_hora`.
- **Tipo de problema:** aprendizaje supervisado de regresión con horizonte de
  una hora.
- **Restricción:** ninguna variable de `t+1` puede utilizarse como predictor y
  la división de datos debe conservar el orden temporal.

### Ventana y estaciones

Para la Entrega 1 se usa 2018–2025: contiene ocho años completos y 16
estaciones con cobertura entre 92,67% y 97,41%. La tabla larga contiene
1.122.048 combinaciones estación-hora y 1.050.341 pares con medición actual y
target disponibles.

### Alcance de datos

La Entrega 1 trabaja únicamente con el histórico de PM2.5 y variables
temporales derivadas. Meteorología y otros contaminantes quedan como posibles
extensiones; no se crean carpetas ni procesos para fuentes que aún no forman
parte del alcance.

## Entregables locales actuales

- Loader: [`src/data/load_pm25.py`](src/data/load_pm25.py).
- Notebook de datos y EDA: [`notebooks/01_eda_pm25.ipynb`](notebooks/01_eda_pm25.ipynb).
- Diccionario: [`docs/data_dictionary.md`](docs/data_dictionary.md).
- Perfil: [`docs/methodology_notes.md`](docs/methodology_notes.md).
- Decisiones: [`docs/decisions.md`](docs/decisions.md).
- Respuestas y plan de EDA: [`docs/eda_plan.md`](docs/eda_plan.md).

## Estado de la parte de código — Entrega 1

Completada. El notebook está ejecutado, contiene outputs guardados y cubre
carga, estructura, calidad, faltantes, duplicados, valores extremos,
distribución, análisis temporal, diferencias entre estaciones, construcción
del target, relación con el target, hallazgos, limitaciones e implicaciones.

El siguiente trabajo es incorporar la caracterización y los tres hallazgos en
Overleaf, verificando que la redacción coincida con
[`docs/entrega1_contenido.md`](docs/entrega1_contenido.md).

## Registro de actualizaciones

| Fecha | Actualización |
| --- | --- |
| 2026-09-14 | Se creó la estructura versionable mínima del repositorio. |
| 2026-09-14 | Se consultó SIATA versión 4.0 y se descargaron/validaron los 162 archivos originales. |
| 2026-09-14 | Se implementó el loader, el perfil completo, el diccionario inicial y el primer notebook. |
| 2026-09-14 | El contexto original se archivó como referencia histórica y este archivo pasó a ser el tablero operativo. |
| 2026-09-14 | Se simplificó el alcance a PM2.5, se retiraron carpetas de fuentes hipotéticas y se definió `pm25_t_plus_1` como target. |
| 2026-09-14 | Se alineó el notebook con los ejemplos de `Machine_Learning_Applied` y con la guía oficial de la Entrega 1. |
| 2026-09-14 | Se completó y ejecutó el EDA; 14 celdas de código tienen outputs guardados y no presentan errores. |
| 2026-09-14 | Se dejó únicamente la estructura de datos PM2.5 y se retiraron las carpetas vacías que no pertenecen al alcance de la Entrega 1. |
