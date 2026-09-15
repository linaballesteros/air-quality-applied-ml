# Notas metodológicas

## Perfil reproducible del histórico PM2.5

Ejecutar:

```bash
python scripts/profile_pm25.py
```

Resultados verificados el 14 de septiembre de 2026 con la versión 4.0:

- 162 archivos mensuales y 118.296 observaciones horarias;
- periodo 2013-01-01 00:00 a 2026-06-30 23:00;
- 33 estaciones históricas y 30 variantes de schema;
- 1.879.277 mediciones no nulas;
- 0 filas duplicadas, 0 timestamps duplicados y 0 horas ausentes del índice;
- 47 horas sin medición en ninguna estación;
- 0 mediciones negativas y 5.036 mediciones iguales a cero.

El número `2.024.491` de celdas vacías sobre la unión de las 33 estaciones no
debe reportarse como tasa de falla: incluye años anteriores a la instalación
o posteriores al retiro de estaciones. La cobertura relevante debe calcularse
por estación y dentro de su periodo activo o de una ventana común definida.

## Tabla analítica propuesta

Para la ventana definida 2018–2025 se seleccionaron 16 estaciones con
cobertura mínima de 90%. La transformación produce:

- tabla ancha: 70.128 horas × 16 estaciones, además de `fecha_hora`;
- tabla larga: 1.122.048 combinaciones estación-hora;
- 1.069.236 mediciones de PM2.5 observadas;
- 1.050.341 pares consecutivos con `pm25` y target `pm25_t_plus_1`
  disponibles para el análisis supervisado;
- 37.083 mediciones fuera de los límites IQR globales (-8,49; 41,98 µg/m³).

El límite inferior negativo es un resultado matemático del criterio IQR, no un
valor observado. Estos 37.083 casos son **posibles valores extremos**, no
errores confirmados, y no se eliminan en el EDA.

## Cálculos exploratorios del 2026-09-14 (fuera del notebook)

Realizados con el loader del repositorio sobre la ventana 2018–2025 y las 16
estaciones, para decidir la formulación. No citar en el paper hasta
reproducirlos en el notebook.

- Horizonte horario: la correlación entre `pm25(t)` y `pm25(t+h)` cae de 0,80
  (h=1) a 0,61 (h=3) y 0,43 (h=6); un modelo lineal con rezagos mejora la
  persistencia solo de 4,97 a 4,59 µg/m³ de MAE en h=1 (test 2025).
- Horizonte diario: persistencia de la media diaria 2,95 µg/m³ vs. 2,73 con un
  modelo lineal de rezagos diarios y estacionalidad (test 2025), sin
  meteorología.
- Eventos de Nivel de Prevención (≥38 µg/m³, media del día calendario con ≥18
  horas): 1.090 días-estación, 438 transiciones, persistencia con precisión y
  recall de 0,60; distribución por año y por número de estaciones afectadas
  en `context.md`.
- Con el máximo de la media móvil de 24 h como target, los eventos suben a
  1.702 y la persistencia a 0,69; se evaluará como sensibilidad.
- Aporte de la meteorología (lineal, origen móvil 2022–2025, 34.908 filas con
  meteorología completa): MAE persistencia 3,42; solo historial PM2.5 3,15;
  historial + meteorología 3,11. AUC para ordenar inicios entre días con hoy
  <38: 0,958 / 0,961 / 0,964. El día previo a un inicio la mediana de PM2.5 es
  32,7 µg/m³ (16,0 en días sin inicio), la lluvia 0,06 mm (1,09) y la humedad
  mínima 44,5 % (50,5 %).
