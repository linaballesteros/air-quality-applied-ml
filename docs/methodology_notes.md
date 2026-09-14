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
