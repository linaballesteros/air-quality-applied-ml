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

Explicar que la red mide y comunica lo observado, mientras las decisiones
preventivas requieren anticipación. El aviso público actual es agregado para
el valle y se decide por constatación; la Resolución 2254 de 2017 exige
evaluar por punto de monitoreo y admite declarar niveles por pronóstico
(ver `sources/resolucion_2254_2017_extracto.md`). El proyecto propone un
pronóstico diario por estación con un día de anticipación. Los beneficiarios
potenciales son autoridades ambientales, investigadores y población
susceptible. No afirmar que se construirá un sistema oficial de alertas.

Si se cita el comunicado del AMVA de marzo de 2025 o el trabajo sobre la
eficacia de las medidas del PIGECA, verificar antes las fuentes originales;
no usar la cifra de "20 estaciones de representatividad poblacional" hasta
encontrarla en una fuente oficial.

## 4. Trabajos relacionados — 150 a 250 palabras

Usar 2–4 trabajos y cubrir para cada uno: problema, datos, método, resultado y
oportunidad restante. La selección inicial más coherente es:

- Baena-Salazar et al. (2019): pronóstico local de PM2.5 con red neuronal.
- Kleine Deters et al. (2017): ML con PM2.5 y variables meteorológicas.
- Parra-Sánchez et al. (2020): datos SIATA, calidad del aire y salud pública.

La oportunidad del proyecto es un pronóstico por estación, con un día de
anticipación, evaluado explícitamente contra la persistencia y en su
capacidad de anticipar el inicio de episodios, usando el histórico público
actualizado y una metodología temporal reproducible de alcance de curso.

## 5. Pregunta de investigación

> ¿Es posible predecir, con un día de anticipación, la concentración media
> diaria de PM2.5 por estación en el Valle de Aburrá, a partir de mediciones
> históricas del contaminante, variables meteorológicas observadas de SIATA y
> variables temporales, superando a un pronóstico de persistencia tanto en
> error como en la anticipación de días en Nivel de Prevención?

Es aprendizaje supervisado de regresión porque el target
`pm25_mean_d_plus_1` es una concentración numérica continua en µg/m³. La
comparación con el umbral de prevención (≥38 µg/m³) es una evaluación derivada
de la predicción numérica, no un segundo problema de clasificación.

## 6. Caracterización de los datos

Incluir únicamente cifras verificadas por el notebook:

- fuente y DOI de SIATA;
- versión 4.0 y 162 archivos mensuales;
- 118.296 observaciones horarias entre 2013-01-01 y 2026-06-30;
- formato original ancho con `fecha_hora` y columnas de estaciones;
- 33 estaciones históricas y 30 variantes de schema;
- transformación a estación-hora y agregación a estación-día;
- target derivado `pm25_mean_d_plus_1`;
- resumen correcto de faltantes y duplicados;
- meteorología SIATA: 12 estaciones asignadas, resolución minutal agregada a
  hora, variables disponibles y cobertura válida tras la bandera `calidad`.

No reportar 2.024.491 celdas vacías como tasa general de fallas: muchas
corresponden a estaciones que aún no existían o ya habían salido de operación.

### Texto base para caracterización

El repositorio de SIATA contiene 162 archivos mensuales de PM2.5, con 118.296
registros horarios entre enero de 2013 y junio de 2026. Los archivos están en
formato ancho: `fecha_hora` identifica el instante y cada una de las demás
columnas corresponde a una estación. En el histórico aparecen 33 estaciones y
30 variantes de schema debido a cambios en la red. Para el EDA se tomó la
ventana 2018–2025 y se seleccionaron 16 estaciones con cobertura mínima de
90%. Tras transformar los datos a una observación por estación-hora
(1.122.048 registros) y agregarlos por día calendario con al menos 18 horas
válidas, se obtuvieron 44.399 registros estación-día con target disponible.
La variable objetivo `pm25_mean_d_plus_1`, media de PM2.5 del día siguiente
en la misma estación expresada en µg/m³, es numérica continua. Como
predictores meteorológicos se asignó a cada estación PM2.5 la estación
meteorológica de SIATA más cercana (14 de 16 a menos de 3 km), con registros
minutales de temperatura, humedad, presión, precipitación y viento agregados
a resolución horaria tras descartar los minutos marcados como dudosos por la
bandera de calidad de SIATA; la cobertura válida es de 88–98% de las horas
en la mayoría de variables y estaciones, con huecos estructurales en el
viento de una estación, la presión de otra y la precipitación de una tercera
(ver `station_matching.md`; reproducir en el notebook antes de citar).

## 7. Insights preliminares del EDA

El notebook conserva el análisis completo. Los tres hallazgos seleccionados
para el paper son:

1. **Cobertura suficiente:** las 16 estaciones seleccionadas tienen entre
   92,67% y 97,41% de cobertura durante 2018–2025 y generan 44.399 registros
   estación-día con target disponible.
2. **Estructura temporal:** el promedio horario máximo aparece a las 08:00
   (25,79 µg/m³) y el mínimo a las 15:00 (13,48 µg/m³); marzo alcanza el mayor
   promedio mensual (28,05 µg/m³), y 179 de los 246 días con alguna estación
   en Nivel de Prevención ocurren en febrero–marzo.
3. **Los episodios son mayoritariamente locales y la persistencia es un
   rival exigente:** en 156 de los 246 días con alguna estación en
   prevención (63%), tres estaciones o menos están afectadas, lo que
   justifica un pronóstico por estación. De los 1.090 días-estación en
   prevención, 438 (40%) son inicios de episodio; un pronóstico de
   persistencia obtiene precisión y recall de 0,60 y, por construcción, nunca
   anticipa un inicio.

Las cifras del hallazgo 3 fueron calculadas con umbral ≥38 µg/m³ y media del
día calendario; deben reproducirse en el notebook antes de incluirse en el
paper. Estos resultados respaldan la viabilidad del problema, pero no
constituyen todavía una evaluación de modelos ni prueban relaciones causales.

## 8. Referencias y trazabilidad

- Mínimo tres fuentes académicas u oficiales.
- Toda cifra del paper debe aparecer calculada en el notebook.
- Usar los PDFs originales para la referencia bibliográfica y los Markdown de
  `docs/sources/` únicamente como ayuda de consulta.
