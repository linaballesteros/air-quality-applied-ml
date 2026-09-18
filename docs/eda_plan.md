# Plan del EDA — Entrega 1

Este plan parte del perfil reproducible de los 162 archivos PM2.5. No incluye
modelado ni decisiones de imputación anticipadas.

## Respuestas a la inspección inicial

1. **Columnas.** Todos los archivos contienen `fecha_hora` y un subconjunto
   cambiante de 33 códigos históricos de estación. La lista y cobertura se
   reproducen con `python scripts/profile_pm25.py`.
2. **Observación.** Una fila representa una hora; cada columna de estación es
   su medición de PM2.5 en esa hora.
3. **Granularidad.** Horaria exacta.
4. **Rango.** 2013-01-01 00:00 a 2026-06-30 23:00.
5. **Estaciones.** Aparecen 33; no todas operan simultáneamente.
6. **Target.** La fuente no trae una columna target única. Se transforma a
   formato largo, se agrega por estación-día y se deriva
   `pm25_mean_d_plus_1`: media diaria de la misma estación al día siguiente.
7. **Faltantes.** Hay 1.879.277 mediciones no nulas y 2.024.491 celdas vacías
   sobre la unión de 33 estaciones. El segundo valor mezcla ausencia de una
   estación fuera de su vida útil con fallas durante operación, por lo que no
   debe presentarse como tasa de missingness.
8. **Duplicados.** Cero filas y cero timestamps duplicados.
9. **Códigos inválidos.** No aparecieron textos no numéricos ni valores
   negativos. Hay 5.036 ceros cuyo significado debe validarse; no se tratarán
   automáticamente como inválidos.
10. **Fecha y hora.** `fecha_hora` usa `YYYY-MM-DD HH:MM:SS`; la zona horaria
    no está declarada en los metadatos consultados.
11. **Compatibilidad.** Los meses no comparten un schema idéntico: existen 30
    variantes por cambios de estaciones. El significado estructural sí se
    conserva.
12. **Tamaño consolidado.** 118.296 filas × 35 columnas con `source_file` y la
    unión de estaciones; 1.879.277 observaciones en una eventual tabla larga
    si se retienen solo mediciones presentes.
13. **Todas las estaciones.** No conviene usarlas sin filtro: sus periodos van
    desde 10 observaciones hasta más de 112.000 y algunas ya no operan.
14. **Rango seleccionado.** 2018–2025 comprende ocho años completos y 16
    estaciones con cobertura ≥90%.
15. **Variables de entrada actuales.** Mediciones de PM2.5 disponibles hasta
    el final del día `d`, `station_id` y variables temporales. Otras fuentes
    quedan fuera del alcance actual.

## Secuencia exacta del EDA

### 1. Completar metadatos

- Obtener catálogo oficial de estaciones, coordenadas, municipio, tipo y
  periodo operativo.
- Confirmar zona horaria y tratamiento oficial de ceros. La unidad µg/m³ y
  cinco códigos de estación ya se contrastaron con un informe de SIATA.
- Actualizar `docs/data_dictionary.md` con evidencia, no inferencias.

**Salida:** diccionario completo y tabla de estaciones.

### 2. Construir la tabla analítica de PM2.5

- Cargar los 162 meses con `src/data/load_pm25.py`.
- Transformar de ancho a largo sin imputar: `fecha_hora`, `station_id`,
  `pm25`, `source_file`.
- Diferenciar ausencia estructural de estación y dato faltante durante su
  periodo activo.
- Producir resumen de cobertura por estación, año y mes.

**Salida:** dataset intermedio reproducible y criterio preliminar de selección.

### 3. Evaluar calidad

- Fechas inválidas, duplicados, discontinuidades y frecuencia.
- Nulos por estación y periodo; rachas consecutivas sin medición.
- Ceros, extremos, saltos abruptos y valores físicamente sospechosos.
- Conservar extremos hasta distinguir episodios reales de errores.

**Salida:** tabla de calidad y decisiones justificadas de limpieza.

### 4. Caracterizar PM2.5

- Media, mediana, desviación, percentiles e IQR por estación.
- Histogramas, ECDF y boxplots con escala apropiada.
- Evolución horaria, diaria y mensual sin convertir correlación en causalidad.
- Comparar estaciones únicamente dentro de ventanas temporales comunes.

**Salida:** candidatos a los primeros hallazgos del paper.

### 5. Analizar estructura temporal

- Perfil por hora del día, día de semana, mes y año.
- Heatmaps hora × mes y series agregadas con número de observaciones visible.
- Autocorrelación y persistencia de PM2.5 si forecasting sigue siendo viable.
- No afirmar picos estacionales sin intervalos y cobertura suficiente.

**Salida:** evidencia para justificar variables temporales y rezagos del
pronóstico diario ya definido.

### 6. Construir el target sin fuga temporal

- Ordenar por `station_id` y `fecha_hora`.
- Agregar la media diaria por estación y día calendario, exigiendo al menos 18
  horas válidas.
- Crear `pm25_mean_d_plus_1` con la media diaria del día calendario siguiente
  dentro de cada estación.
- Verificar que entre predictor y target haya exactamente un día calendario.
- Excluir del modelado filas sin media de hoy o sin target, documentando
  cuántas se pierden.
- Reservar el periodo de prueba por origen móvil; no usar partición aleatoria.

**Salida:** definición empírica e inequívoca del problema de regresión.

### 7. Cerrar alcance y hallazgos

- Elegir ventana, estaciones, unidad de observación y target.
- Seleccionar 2–3 hallazgos que respalden la pregunta de investigación.
- Verificar que cada cifra y figura del paper se reproduzca desde el notebook.
- Registrar limitaciones: cambios de red, faltantes, ceros y cobertura de
  predictores.

**Salida:** caracterización y sección de insights lista para Overleaf.
