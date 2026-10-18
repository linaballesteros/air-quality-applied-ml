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
| Pregunta | ¿Es posible predecir, con un día de anticipación, la concentración media diaria de PM2.5 por estación en el Valle de Aburrá a partir del historial del contaminante y variables temporales, y en qué medida las variables meteorológicas observadas de SIATA mejoran esa predicción frente a un pronóstico de persistencia, en error y en anticipación de días en Nivel de Prevención? |
| Aporte | Pronóstico por estación (la norma exige evaluar por punto de monitoreo y el aviso público actual es agregado), evaluación rigurosa contra la persistencia con igual número de avisos, y cuantificación del valor incremental de la meteorología observada; un aporte pequeño también es un resultado útil (señalaría la necesidad de pronóstico meteorológico). |

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
  mañana), evaluada en MAE y en precisión/recall de días en prevención. En
  los inicios de episodio la comparación se hace con el mismo número de
  avisos: una persistencia con umbral de aviso más bajo también captura
  inicios, porque el PM2.5 sube gradualmente.
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
1.122.048 combinaciones estación-hora; agregada por día deja 46.752
combinaciones estación-día, 45.152 con media diaria válida y 44.399 con media
de hoy y target de mañana disponibles.

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
- Notebook de modelado: [`notebooks/02_modelado.ipynb`](notebooks/02_modelado.ipynb).
- Predictores y evaluación: [`src/features/`](src/features/) y [`src/models/`](src/models/).

## Estado de la parte de código — Entrega 1

Completada y alineada con la formulación diaria. El notebook
[`notebooks/01_eda_pm25.ipynb`](notebooks/01_eda_pm25.ipynb) está ejecutado
sin errores (51 celdas, ejecutado con `.venv`) y cubre: fuente, estructura,
cobertura, ventana, target diario `pm25_mean_d_plus_1`, limpieza,
distribución, patrones temporales, diferencias entre estaciones, persistencia
diaria y días en Nivel de Prevención (por año, inicios de episodio, extensión
espacial), meteorología asignada (cruce, cobertura válida por variable,
descriptivos, correlaciones diarias y un episodio de ejemplo), hallazgos,
limitaciones e implicaciones. Todas las cifras de la tabla de hechos
verificados de este archivo se reproducen en el notebook. La sección 16
regenera las figuras del paper en `paper/figuras/`.

Pendiente antes de modelar: resolver los huecos meteorológicos documentados
en [`docs/station_matching.md`](docs/station_matching.md) y validar las
presiones de 0 hPa que la bandera de calidad no marcó (resuelto el
2026-10-17: se tratan como faltantes en `src/features`).

## Estado y cómo retomar — entrega final

Última actualización: 2026-10-17. Esta sección es el punto de partida para
cualquiera de los dos; el detalle del feedback y la lista completa de tareas
están en [`feedback-delivery-01/README.md`](feedback-delivery-01/README.md).

**Requisitos.** Paper final: metodología, resultados, discusión (comparar
con los trabajos relacionados) y conclusiones. Presentación: introducción
con el problema, EDA con insights, metodología con diagramas de flujo y
resultados. Pendiente preguntar al profesor si se exige abstract.

**Hecho.**

- Tabla de predictores con ventanas de tiempo:
  [`src/features/build_features.py`](src/features/build_features.py).
- Origen móvil, métricas y regla de aviso:
  [`src/models/evaluation.py`](src/models/evaluation.py).
- [`notebooks/02_modelado.ipynb`](notebooks/02_modelado.ipynb) ejecutado
  (secciones 1–13): persistencia, Gradient Boosting sin y con meteorología,
  bootstrap, avisos a igual presupuesto, error en días críticos, SHAP
  (sección 11, con la comparación de pesos de Baena-Salazar en 11.1) y
  réplica del periodo de validación de Baena-Salazar (sección 12).

**Cifras vigentes (2022–2025, fuera de muestra).**

| Resultado | Persistencia | GB sin meteo | GB con meteo |
| --- | --- | --- | --- |
| MAE (µg/m³) | 3,37 | 2,77 | 2,74 |
| R² | 0,56 | 0,71 | 0,71 |
| MAE en días en prevención | 5,88 | 6,90 | 6,56 |
| Inicios avisados a igual presupuesto (de 123) | 0 | 29 | 30 |

SHAP (modelo con meteorología): PM2.5 del día `d` 49,5 % de la
importancia, rezagos y ventanas 19,9 %, calendario 18,2 %, meteorología
8,6 %, estación 3,9 %. Con entradas tipo Baena-Salazar el PM2.5 de hoy
concentra el 65,7 % (ellos: 34,2 %).

Réplica de Baena-Salazar (ene–mar 2016, ITA-CONC / MED-UNNV, r² como
correlación al cuadrado): ellos 0,806 / 0,864; persistencia 0,796 / 0,811;
GB con meteorología que predice el nivel 0,726 / 0,517 (22 días superan el
máximo de entrenamiento y los árboles no extrapolan); la variante que
predice el cambio 0,802 / 0,822, con MAPE de 14,2 % / 11,5 % (ellos:
18,5 % / 12,4 %).

**Para retomar.** Con los datos ya descargados (ver README), activar
`.venv`, ejecutar `python -m unittest discover -q` (20 pruebas) y abrir
`notebooks/02_modelado.ipynb`; se ejecuta completo en unos tres minutos. La
sección 12 necesita además la meteorología 2013–2016 de las estaciones 203 y
206 (comando en el README).

**Siguientes pasos, en orden.**

1. ~~SHAP~~: hecho el 2026-10-18 (sección 11).
2. ~~Réplica de Baena-Salazar~~: hecha el 2026-10-18 (sección 12).
3. **Sensibilidad** (nueva sección 13, opcional si falta tiempo): excluir
   BEL-FEVE y MED-SCRI, y probar la estación 397 para el viento de ITA-CONC.
4. ~~Diagramas de flujo~~: hechos el 2026-10-18 en TikZ
   (`paper/figuras/diagramas/`, PDF en `paper/figuras/`): `flujo_datos`,
   `flujo_metodologia` y `origen_movil`, al ancho de una columna IEEE.
5. **Paper** (`paper/main.tex`): dividir la pregunta en dos (borrador en
   `respuestas.md` §5), aplicar los textos de §2 y §4, y escribir
   metodología, resultados, discusión y conclusiones. Las figuras deben
   salir del notebook, como en la Entrega 1.
6. **Presentación**: cuatro bloques, reutilizando las figuras del paper;
   en el EDA, explicar la composición de estaciones (`respuestas.md` §1).

**Decisiones abiertas.**

- ~~Nivel o cambio~~: resuelto el 2026-10-18, se mantiene el nivel
  (justificación y cifras en `docs/decisions.md`). Lo de 2016 va a la
  discusión como limitación.
- Si se usa el semestre 2026 como prueba final adicional (exige descargar
  meteorología 2026).
- Cómo cubrir los huecos meteorológicos de `docs/station_matching.md`.

## Siguientes pasos por persona

El borrador del paper está en [`paper/main.tex`](paper/main.tex) (movido
desde `paper_hasta_el_momento.md` sin cambios de contenido). La guía sección
por sección es [`docs/entrega1_contenido.md`](docs/entrega1_contenido.md).

**Lina — título, introducción y planteamiento del problema: completado.** El
título se mantuvo porque cumple el límite de 20 palabras. La introducción y el
planteamiento quedaron alineados con el pronóstico de la media diaria por
estación a un día, la comparación con persistencia, la cuantificación del
aporte meteorológico y el alcance exclusivo de PM2.5. Se incorporó el sustento
de la Resolución 2254 de 2017 y se retiró del texto la cita a
`ganan2026spatiotemporal`, cuya fuente primaria no está archivada.

**Alejandro — resto del paper.** Hecho el 2026-09-15: secciones II
(trabajos relacionados, 257 palabras), III (pregunta), IV (caracterización
con Tabla I y Fig. 1) y V (tres insights con Tabla II y Fig. 2) en
`paper/main.tex`; figuras exportadas del notebook a `paper/figuras/`. Se
añadieron al `.bib` las entradas `siata2026pm25` y `siata2026meteo`; la
Resolución 2254 se cita con la entrada `minambiente2017resolucion2254` que
añadió Lina. Gañán 2026 no se resumió en trabajos relacionados por no tener
PDF verificable y Lina retiró su cita de la introducción; la entrada sigue
en el `.bib` sin usarse.

**Integración (2026-09-16).** Se fusionaron ambas partes: el borrador
completo compila con IEEEtran en 4 páginas con referencias y todas las
citas resuelven. La sección III se recortó para no repetir lo que el
planteamiento ya establece (target, tipo de problema, persistencia, igual
número de avisos). Overleaf ya está actualizado y la sección V enlaza el
repositorio en un pie de página. El repositorio se hará público el día
anterior a la entrega (19 de septiembre); hasta entonces el enlace del paper
no abre para terceros.

**Feedback de la Entrega 1 (recibido 2026-10-01).** El profesor recomienda
Gradient Boosting, ventanas de tiempo, SHAP y comparar con Baena-Salazar et
al., sugiere dividir la pregunta en dos y pide explicar la composición de
estaciones, la ventana 2018–2025, los faltantes (con diagrama de flujo) y la
Tabla II. Plan de trabajo y respuestas con cifras verificadas en
[`feedback-delivery-01/`](feedback-delivery-01/README.md) (carpeta interna,
no se lleva a `main`).

**Antes de la Entrega 2 (cualquiera de los dos).** Resolver los huecos
meteorológicos de [`docs/station_matching.md`](docs/station_matching.md).
La regla de aviso quedó fijada el 2026-10-17 (ver `docs/decisions.md`).

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
| 2026-09-14 | Prueba exploratoria (lineal, origen móvil 2022–2025): la meteorología observada mejora el MAE ~1 % sobre el historial de PM2.5 y poco el ordenamiento de inicios; la pregunta pasa a cuantificar ese aporte y la comparación con persistencia se fija a igual número de avisos. |
| 2026-09-14 | Se movió el borrador a `paper/main.tex` con `referencias.bib`, se documentó la puesta en marcha completa y se repartieron los siguientes pasos. |
| 2026-09-14 | Se copiaron a `paper/referencias.bib` las siete referencias que están en Overleaf; `paper/` queda como registro local del artículo. |
| 2026-09-14 | Se completó la parte de Lina: introducción y planteamiento alineados con el pronóstico diario por estación; se añadió la Resolución 2254 de 2017 a la bibliografía y se retiró una cita sin fuente primaria trazable. |
| 2026-09-15 | Se añadió al notebook la distribución y los atípicos del target diario; se redactaron las secciones II–V del paper con cifras del notebook y se verificó la compilación. |
| 2026-09-16 | Se integraron los cambios de Lina (introducción y planteamiento) con las secciones II–V; se recortó la sección III, se unificó la cita de la Resolución 2254 y se verificó la compilación completa. |
| 2026-09-16 | Revisión externa del borrador: se suavizaron afirmaciones categóricas del EDA, se explicó el manejo de faltantes meteorológicos, se eliminó redundancia entre introducción, planteamiento y pregunta, y se corrigió la tipografía (decimal en modo matemático, "Tabla"/"Fig." en captions). La pregunta de investigación no cambió. |
| 2026-09-17 | Revisión previa a la entrega: el notebook exporta las figuras del paper de forma reproducible (sección 16, PNG idénticos a los versionados), el paper explica los 753 registros con media sin target, se corrigieron cifras desactualizadas en `context.md`, `eda_plan.md`, `methodology_notes.md` y `docs/README.md`, el README reporta 11 pruebas y `requirements.txt` incluye `numpy`. |
| 2026-09-20 | Revisión externa de formato: las figuras del paper pasan a PDF vectorial dibujado al ancho de columna IEEE (antes PNG reducidos), la Fig. 2 apila sus dos paneles y se coloca junto a su primera mención, las citas de la sección II aparecen junto al nombre de los autores y el documento usa EB Garamond (`ebgaramond-maths` + `newtxmath`) en vez de la Times de IEEEtran. Compila en 4 páginas con referencias y sin citas sin resolver. |
| 2026-10-01 | Se registró el feedback de la Entrega 1 en `feedback-delivery-01/`: plan para la entrega final (XGBoost con ventanas de tiempo, SHAP, comparación con Baena-Salazar, dos preguntas) y respuestas a las dudas. Verificado: la red tenía 5–9 estaciones hasta 2016 (solo 3 con ≥90 % en 2013–2025) y, en el periodo de validación de Baena-Salazar, la persistencia alcanza r² 0,796 (ITA-CONC) y 0,811 (MED-UNNV) frente a 0,806 y 0,864 de su red neuronal. |
| 2026-10-17 | Tabla de predictores con ventanas de tiempo en `src/features/build_features.py` (5 pruebas nuevas, 16 en total) y notebook `02_modelado.ipynb` ejecutado: reproduce los 44.399 registros del EDA; persistencia por año de prueba con MAE de 2,95 a 3,61 µg/m³ y R² de 0,44 a 0,65; las presiones de 0 hPa se tratan como faltantes. |
| 2026-10-17 | Modelado con origen móvil en `02_modelado.ipynb` y `src/models/evaluation.py` (20 pruebas). En 2022–2025 el MAE baja de 3,37 (persistencia) a 2,76 (Gradient Boosting sin meteorología) y 2,73 µg/m³ (con meteorología); ambas mejoras con IC 95 % por bootstrap de bloques que excluye el cero, la de la meteorología en las 16 estaciones. A igual presupuesto de avisos, Gradient Boosting anticipa 28–30 de 123 inicios de episodio y la persistencia ninguno. La meteorología reduce el error en días en prevención de 6,85 a 6,53 µg/m³. |
| 2026-10-18 | SHAP en `02_modelado.ipynb` (sección 11): el PM2.5 del día `d` es la entrada dominante (49,5 %; 65,7 % con entradas tipo Baena-Salazar, que reportó 34,2 %), seguido de la media de siete días, el día de la semana y el mes; la meteorología suma 8,6 %. La estación pasó a one-hot porque SHAP no reproduce las divisiones categóricas nativas; las cifras del modelado cambiaron en centésimas (MAE con meteorología 2,74 µg/m³; mejora por meteorología en 14 de 16 estaciones). |
| 2026-10-18 | Réplica del periodo de validación de Baena-Salazar et al. (sección 12 de `02_modelado.ipynb`) con ITA-CONC/206 y MED-UNNV/203 (se añadió la 203 a `src/data/stations.py` y se descargó su meteorología 2013-01 a 2016-03 y la de la 206). El modelo de nivel pierde frente a la persistencia porque 22 de 175 días superan el máximo de entrenamiento; predecir el cambio lo corrige (r² 0,80/0,82, MAPE 14,2/11,5 %). Queda abierta la elección entre nivel y cambio. |
| 2026-10-18 | Diagramas de flujo en TikZ para paper y presentación (`paper/figuras/flujo_datos.pdf`, `flujo_metodologia.pdf` y `origen_movil.pdf`; fuentes en `paper/figuras/diagramas/`). El de datos corrige los registros con meteorología completa a 32.455 (73,1 %), la cifra del notebook de modelado. |
