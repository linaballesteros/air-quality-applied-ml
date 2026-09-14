# Contenido que debe ir en la Entrega 1

Esta guía traduce los requisitos oficiales al proyecto. No reemplaza el paper;
indica qué debe demostrarse y de dónde sale cada elemento.

## 1. Título tentativo

**Predicción de concentraciones de PM2.5 en el Valle de Aburrá mediante
aprendizaje automático con datos de la red SIATA**

Tiene 19 palabras, identifica contaminante, región, método y fuente; cumple el
máximo de 20 palabras indicado por la guía.

## 2. Introducción — 300 a 500 palabras

Organizar como embudo:

1. PM2.5 como problema ambiental y de salud.
2. Condiciones y evidencia del Valle de Aburrá.
3. Necesidad de anticipar su concentración.
4. Disponibilidad del histórico SIATA y posibilidad de aplicar regresión.

Debe apoyarse en 1–2 fuentes y evitar detalles de implementación.

## 3. Planteamiento del problema

Explicar que el monitoreo describe el valor observado, mientras una predicción
a una hora podría aportar información previa para análisis preventivo. Los
beneficiarios potenciales son autoridades ambientales, investigadores y
población susceptible. No afirmar que se construirá un sistema oficial de
alertas.

## 4. Trabajos relacionados — 150 a 250 palabras

Usar 2–4 trabajos y cubrir para cada uno: problema, datos, método, resultado y
oportunidad restante. La selección inicial más coherente es:

- Baena-Salazar et al. (2019): pronóstico local de PM2.5 con red neuronal.
- Kleine Deters et al. (2017): ML con PM2.5 y variables meteorológicas.
- Parra-Sánchez et al. (2020): datos SIATA, calidad del aire y salud pública.

La oportunidad del proyecto es evaluar un horizonte horario con el histórico
público actualizado y una metodología temporal reproducible de alcance de
curso.

## 5. Pregunta de investigación

> ¿Es posible predecir, con una hora de anticipación, la concentración de
> PM2.5 en estaciones seleccionadas del Valle de Aburrá usando mediciones
> históricas del contaminante y variables temporales mediante modelos
> supervisados de regresión?

Es aprendizaje supervisado de regresión porque el target
`pm25_t_plus_1` es una concentración numérica continua en µg/m³.

## 6. Caracterización de los datos

Incluir únicamente cifras verificadas por el notebook:

- fuente y DOI de SIATA;
- versión 4.0 y 162 archivos mensuales;
- 118.296 observaciones horarias entre 2013-01-01 y 2026-06-30;
- formato original ancho con `fecha_hora` y columnas de estaciones;
- 33 estaciones históricas y 30 variantes de schema;
- transformación a estación-hora;
- target derivado `pm25_t_plus_1`;
- resumen correcto de faltantes y duplicados.

No reportar 2.024.491 celdas vacías como tasa general de fallas: muchas
corresponden a estaciones que aún no existían o ya habían salido de operación.

### Texto base para caracterización

El repositorio de SIATA contiene 162 archivos mensuales de PM2.5, con 118.296
registros horarios entre enero de 2013 y junio de 2026. Los archivos están en
formato ancho: `fecha_hora` identifica el instante y cada una de las demás
columnas corresponde a una estación. En el histórico aparecen 33 estaciones y
30 variantes de schema debido a cambios en la red. Para el EDA se tomó la
ventana 2018–2025 y se seleccionaron 16 estaciones con cobertura mínima de
90%. Tras transformar los datos a una observación por estación-hora, se
obtuvieron 1.122.048 registros; 1.050.341 contienen tanto la medición actual
como el target de la hora siguiente. La variable objetivo
`pm25_t_plus_1`, expresada en µg/m³, es numérica continua.

## 7. Insights preliminares del EDA

El notebook conserva el análisis completo. Los tres hallazgos seleccionados
para el paper son:

1. **Cobertura suficiente:** las 16 estaciones seleccionadas tienen entre
   92,67% y 97,41% de cobertura durante 2018–2025 y generan 1.050.341 pares
   horarios utilizables.
2. **Estructura temporal:** el promedio horario máximo aparece a las 08:00
   (25,79 µg/m³) y el mínimo a las 15:00 (13,48 µg/m³); marzo alcanza el mayor
   promedio mensual (28,05 µg/m³).
3. **Persistencia a corto plazo:** la correlación entre `pm25(t)` y
   `pm25(t+1)` es 0,804. Un baseline que repite la última medición obtiene MAE
   de 4,98 µg/m³, referencia que los modelos futuros deberán superar sobre un
   periodo de prueba posterior.

Estos resultados respaldan la viabilidad del problema, pero no constituyen
todavía una evaluación de modelos ni prueban relaciones causales.

## 8. Referencias y trazabilidad

- Mínimo tres fuentes académicas u oficiales.
- Toda cifra del paper debe aparecer calculada en el notebook.
- Usar los PDFs originales para la referencia bibliográfica y los Markdown de
  `docs/sources/` únicamente como ayuda de consulta.
