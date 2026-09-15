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
| Pregunta | ¿Es posible predecir, con un día de anticipación, la concentración media diaria de PM2.5 por estación en el Valle de Aburrá, a partir de mediciones históricas del contaminante, variables meteorológicas observadas de SIATA y variables temporales, superando a un pronóstico de persistencia tanto en error como en la anticipación de días en Nivel de Prevención? |
| Aporte | Pronóstico por estación (la norma exige evaluar por punto de monitoreo y el aviso público actual es agregado) y detección del inicio de episodios, que es cuando un aviso sirve para actuar. |

## Reglas de trabajo

- Distinguir siempre hechos verificados, propuestas y pendientes.
- Toda cifra del paper debe reproducirse en un notebook o script.
- No imputar nulos, eliminar extremos ni interpretar ceros sin evidencia.
- No unir fuentes sin comprobar estación, fecha-hora, frecuencia y zona
  horaria.
- Los cambios metodológicos se registran en [`docs/decisions.md`](docs/decisions.md).
- Los PDFs convertidos para consulta están en [`docs/sources`](docs/sources/);
  las citas finales deben verificarse en los originales.
- Los umbrales normativos provienen de la Resolución 2254 de 2017; el
  extracto verificado está en
  [`docs/sources/resolucion_2254_2017_extracto.md`](docs/sources/resolucion_2254_2017_extracto.md).

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

## Fuente de datos verificada — PM2.5

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

## Fuente de datos verificada — meteorología

| Propiedad | Evidencia |
| --- | --- |
| Colección | SIATA, colección *Meteorológica*: 51 estaciones, un dataset por estación |
| Descripción de la red | *Información de la Red Meteorológica*, DOI `10.83041/NXHIKW` (tabla de estaciones con coordenadas y PDF de generalidades) |
| Resolución | Un registro por minuto; archivos mensuales de ~2,8 MB por estación |
| Variables | `t` temperatura, `h` humedad relativa, `pr` presión, `p` precipitación, `vv`/`vv_max` velocidad del viento, `dv`/`dv_max` dirección, bandera `calidad` por variable |
| Estaciones requeridas | 12 códigos (59, 68, 73, 82, 105, 197, 201, 202, 206, 229, 252, 271), asignados a las 16 estaciones PM2.5 en [`docs/station_matching.md`](docs/station_matching.md) |
| Cobertura de archivos 2018–2025 | 10 estaciones con 94–96 de 96 meses; 271 termina en 2024-07 (afecta a BEL-FEVE) |
| Descarga | `python scripts/download_meteo_dataset.py` a `data/raw/meteo/<código>/`, excluido de Git y validado con MD5 |
| Agregación | `python scripts/build_meteo_hourly.py` aplica la bandera `calidad` (gramática verificada contra 64 valores observados), exige 45 minutos válidos por hora y escribe `data/interim/meteo_hourly.csv` (801.839 filas) |
| Cobertura válida 2018–2025 | 88–98 % de las horas en la mayoría de variables y estaciones; huecos estructurales en viento de 206 (33 %), presión de 252 (15 %), lluvia de 229 (74 %) y todo 271 desde 2024-08; detalle y alternativas en [`docs/station_matching.md`](docs/station_matching.md) |

También existen históricos consolidados de PM10, O3, NO2, NO, NOx, CO y SO2
con el mismo formato que PM2.5. No forman parte del alcance actual.

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

- **Unidad de observación analítica:** una estación en un día `d`.
- **Target:** `pm25_mean_d_plus_1`, media de PM2.5 del día calendario
  siguiente en esa estación, calculada con al menos 18 horas válidas;
  variable numérica continua en µg/m³.
- **Predictores disponibles:** PM2.5 observado hasta el final del día `d`
  (media diaria, medias de días previos, medias horarias del día), variables
  meteorológicas observadas hasta el final del día `d` en la estación
  asignada, código de estación y variables temporales derivadas de la fecha.
- **Tipo de problema:** aprendizaje supervisado de regresión con horizonte de
  un día.
- **Evaluación derivada:** se comparan las predicciones con el umbral de
  Nivel de Prevención (≥38 µg/m³, Resolución 2254 de 2017, Tabla 4) para
  medir la anticipación de días en ese nivel, en particular las
  transiciones (día sin evento seguido de día con evento). ICA Naranja
  (≥40,5 µg/m³) se reporta como umbral secundario.
- **Baseline obligatorio:** persistencia (la media de hoy como pronóstico de
  mañana), evaluada en MAE y en precisión/recall de días en prevención.
- **Restricción:** ninguna variable del día `d+1` puede utilizarse como
  predictor y la división de datos debe conservar el orden temporal.

### Hechos verificados sobre eventos (2018–2025, 16 estaciones)

Calculados con la media del día calendario y umbral ≥38 µg/m³; deben
reproducirse en el notebook antes de citarse en el paper.

| Pregunta | Resultado |
| --- | --- |
| Días-estación con target disponible | 44.399 |
| Días-estación en Nivel de Prevención | 1.090 (2,5 %) |
| Transiciones (ayer sin evento, hoy con evento) | 438 (40 % de los eventos) |
| Persistencia como clasificador de "mañana en prevención" | precisión 0,60 y recall 0,60 |
| Eventos por año | 2018: 140 · 2019: 255 · 2020: 412 · 2021: 26 · 2022: 59 · 2023: 36 · 2024: 158 · 2025: 4 |
| Días con al menos una estación en prevención | 246; en 110 de ellos solo una estación y en 156 (63 %) tres o menos; en 40 más de diez |
| Estacionalidad | 179 de 246 días con evento ocurren en febrero–marzo |

Implicaciones: 2025 no puede ser el único periodo de prueba; la evaluación
debe usar origen móvil (probar por separado 2022, 2023, 2024 y 2025). El
carácter local de la mayoría de eventos respalda el pronóstico por estación.

### Ventana y estaciones

Para la Entrega 1 se usa 2018–2025: contiene ocho años completos y 16
estaciones con cobertura entre 92,67% y 97,41%. La tabla larga contiene
1.122.048 combinaciones estación-hora y 1.050.341 pares con medición actual y
target disponibles.

### Alcance de datos

La Entrega 1 caracteriza el histórico de PM2.5 (target y predictores
autorregresivos) y la meteorología de SIATA asignada a cada estación
(cobertura, calidad y descriptivos). Otros contaminantes quedan fuera del
alcance.

## Entregables locales actuales

- Loader: [`src/data/load_pm25.py`](src/data/load_pm25.py).
- Notebook de datos y EDA: [`notebooks/01_eda_pm25.ipynb`](notebooks/01_eda_pm25.ipynb).
- Diccionario: [`docs/data_dictionary.md`](docs/data_dictionary.md).
- Perfil: [`docs/methodology_notes.md`](docs/methodology_notes.md).
- Decisiones: [`docs/decisions.md`](docs/decisions.md).
- Cruce de estaciones: [`docs/station_matching.md`](docs/station_matching.md)
  y [`src/data/stations.py`](src/data/stations.py).
- Descarga meteorológica: [`scripts/download_meteo_dataset.py`](scripts/download_meteo_dataset.py).
- Loader meteorológico: [`src/data/load_meteo.py`](src/data/load_meteo.py) y
  [`scripts/build_meteo_hourly.py`](scripts/build_meteo_hourly.py).
- Respuestas y plan de EDA: [`docs/eda_plan.md`](docs/eda_plan.md).

## Estado de la parte de código — Entrega 1

Completada y alineada con la formulación diaria. El notebook
[`notebooks/01_eda_pm25.ipynb`](notebooks/01_eda_pm25.ipynb) está ejecutado
sin errores (47 celdas, ejecutado con `.venv`) y cubre: fuente, estructura,
cobertura, ventana, target diario `pm25_mean_d_plus_1`, limpieza,
distribución, patrones temporales, diferencias entre estaciones, persistencia
diaria y días en Nivel de Prevención (por año, inicios de episodio, extensión
espacial), meteorología asignada (cruce, cobertura válida por variable,
descriptivos, correlaciones diarias y un episodio de ejemplo), hallazgos,
limitaciones e implicaciones. Todas las cifras de la tabla de hechos
verificados de este archivo se reproducen en el notebook.

Pendiente antes de modelar: resolver los huecos meteorológicos documentados
en [`docs/station_matching.md`](docs/station_matching.md) y validar las
presiones de 0 hPa que la bandera de calidad no marcó.

El siguiente trabajo es incorporar la caracterización y los tres hallazgos en
Overleaf según [`docs/entrega1_contenido.md`](docs/entrega1_contenido.md). La
Introducción actual del borrador ya describe meteorología como predictor; la
sección de pregunta de investigación debe reemplazar la plantilla por la
pregunta vigente.

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
| 2026-09-14 | Se replanteó la pregunta: pronóstico diario por estación con un día de anticipación, meteorología SIATA como predictor y persistencia como baseline; el horizonte horario t+1 se descartó por no aportar valor operativo. |
| 2026-09-14 | Se verificaron los umbrales de la Resolución 2254 de 2017 (norma 37, Prevención 38–55, ICA Naranja 40,5–65,4) y se cuantificaron los eventos por año y su carácter local. |
| 2026-09-14 | Se exploró el Dataverse meteorológico, se cruzaron las 16 estaciones PM2.5 con 12 estaciones meteorológicas y se creó el script de descarga. |
| 2026-09-14 | Se descargaron 1.131 archivos meteorológicos (3,0 GB), se implementó el loader con decodificación de `calidad` y agregación horaria, y se cuantificó la cobertura válida por variable. |
| 2026-09-14 | Se reescribió y ejecutó el notebook con el target diario, el análisis de eventos de prevención y la sección de meteorología; hallazgos, limitaciones e implicaciones actualizados. |
