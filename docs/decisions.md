# Registro de decisiones

## Decisiones vigentes

| Fecha | Decisión | Justificación |
| --- | --- | --- |
| 2026-09-14 | Descargar los archivos originales mediante `?format=original`. | El endpoint por defecto de Dataverse entrega una representación tabulada generada; el original conserva el archivo publicado y coincide con el MD5 oficial. |
| 2026-09-14 | Detectar codificación y delimitador en el loader. | La extensión `.tab` no garantiza tabuladores: la muestra original de 2013-01 usa comas. |
| 2026-09-14 | Permitir cambios de estaciones entre meses y conservar `source_file`. | Se observaron 30 variantes de schema y 33 estaciones históricas. Exigir igualdad descartaría cambios reales de la red. |
| 2026-09-14 | Mantener datos crudos, intermedios y procesados fuera de Git. | Los archivos pueden reproducirse desde la API y no deben inflar el repositorio. |
| 2026-09-14 | Definir el problema como pronóstico de la media diaria de PM2.5 por estación con un día de anticipación (`pm25_mean_d_plus_1`). Reemplaza la decisión previa de horizonte horario t+1. | Un horizonte de una hora no deja tiempo para actuar y un modelo apenas mejora la persistencia (MAE 4,59 vs 4,97 µg/m³ en pruebas exploratorias). Un día sí permite decisiones preventivas; la Resolución 2254 de 2017 evalúa por punto de monitoreo y admite declarar niveles por pronóstico. |
| 2026-09-14 | Incorporar meteorología observada de SIATA como predictor, asignando a cada estación PM2.5 la meteorológica más cercana. | El pasado reciente de PM2.5 pierde poder predictivo más allá de unas horas; la literatura local usa meteorología para anticipar episodios. El cruce verificado da 15 de 16 estaciones a ≤3 km; 14 de ellas con archivos mensuales casi completos. |
| 2026-09-14 | Usar el Nivel de Prevención (≥38 µg/m³, Tabla 4) como umbral principal de evaluación e ICA Naranja (≥40,5 µg/m³, Tabla 6) como secundario. | El nivel de prevención es el que activa medidas y es declarable por pronóstico. El valor 37 de la norma no es un umbral de alerta. |
| 2026-09-14 | Definir la media diaria como media del día calendario con al menos 18 horas válidas. | Es una media de 24 horas, coincide con la unidad diaria de comunicación de alertas y produce un target por estación-día sin ventanas solapadas. La norma usa medias móviles de 24 h para constatación; el máximo de la media móvil del día se evaluará como sensibilidad. |
| 2026-09-14 | Evaluar con origen móvil: probar por separado en 2022, 2023, 2024 y 2025 entrenando con los años anteriores. | Los eventos son muy desiguales entre años (412 en 2020, 4 en 2025); un único test futuro no permite medir la anticipación de episodios. |
| 2026-09-14 | Exigir a todo modelo superar a la persistencia en MAE y en precisión/recall de días en prevención, reportando aparte los inicios de episodio. | La persistencia acierta el 60 % de los días en prevención; el aporte de un modelo debe demostrarse sobre todo en los inicios de episodio. |
| 2026-09-14 | Comparar modelos y persistencia en los inicios de episodio con el mismo número de avisos (igual presupuesto de alertas o igual precisión), no con el umbral fijo de 38 µg/m³. | Con umbral 38 la persistencia no anticipa inicios por definición, pero como el PM2.5 sube gradualmente (mediana de 32,7 µg/m³ el día previo a un inicio), una persistencia con umbral de aviso 30 captura el 74 % de los inicios; una regresión que minimiza el error medio se encoge hacia la media y con umbral 38 avisa menos eventos que la persistencia. La regla de aviso de la Entrega 2 será un umbral calibrado o una probabilidad de exceder 38. |
| 2026-09-14 | Formular la pregunta como cuantificación del aporte de la meteorología observada, no como supuesto de que aporta. | En una prueba lineal con origen móvil 2022–2025 la meteorología redujo el MAE de 3,15 a 3,11 µg/m³ y elevó el AUC de inicios de 0,961 a 0,964; un aporte pequeño es un resultado válido que señalaría la necesidad de pronóstico meteorológico. |
| 2026-09-14 | Conservar BEL-FEVE (meteorológica 271 sin archivos desde 2024-08) y MED-SCRI (meteorológica 201 a 5,8 km) y reportarlos como limitación. | Excluirlas reduce la cobertura espacial; su efecto se medirá con un análisis de sensibilidad. |
| 2026-09-14 | Trabajar inicialmente con 2018–2025 y 16 estaciones con cobertura ≥90%. | Conserva ocho años completos y entre 92,67% y 97,41% de cobertura por estación. |
| 2026-09-14 | No imputar faltantes en el EDA; excluir solo pares sin medición actual o target de la tabla supervisada. | Mantiene transparentes los datos observados y deja 1.050.341 pares utilizables. |
| 2026-09-14 | Conservar ceros y valores fuera de límites IQR. | SIATA reporta mínimos horarios de 0,0 y los extremos pueden ser episodios reales; no existe evidencia para eliminarlos. |
| 2026-10-17 | Tratar como faltantes las 7 horas con presión de 0 hPa antes de la media diaria. | No son físicas (la presión en el valle ronda 840 hPa) y la bandera de calidad no las marca. |
| 2026-10-17 | Predictores con ventanas de tiempo: media de hoy y de 1 a 6 días antes, medias móviles de 3 y 7 días, desviación de 7 días, cambio respecto a ayer, máximo horario y media de 18–23 h del día `d`; meteorología diaria con lluvia de 3 días; mes y día de la semana del día pronosticado. | Recomendación del profesor (ventanas de tiempo) y entradas de Baena-Salazar et al. (PM2.5 de 1–3 días antes, lluvia acumulada de 3 días). Todo se observa hasta el final de `d`; una prueba unitaria lo verifica. |
| 2026-10-17 | Usar `HistGradientBoostingRegressor` de scikit-learn y conservar los registros con predictores faltantes. | El curso usa Gradient Boosting de scikit-learn; esta variante admite faltantes sin imputar, y exigir meteorología completa descartaría el 27 % de la tabla supervisada. |
| 2026-10-17 | Origen móvil anual: cada año de 2019 a 2025 se predice con un modelo entrenado solo con los años anteriores; 2022–2025 son años de prueba y 2019–2021 solo validación. | Resuelve el corte de entrenamiento/validación pendiente. Las predicciones fuera de muestra de años previos sirven para elegir hiperparámetros y calibrar avisos sin tocar el año de prueba. |
| 2026-10-17 | Hiperparámetros elegidos con el MAE de 2019–2021 y comunes a los dos modelos: `learning_rate=0.03`, `max_iter=300`, `max_leaf_nodes=7`, `min_samples_leaf=50`. | Las configuraciones probadas (tasa 0,03–0,1; 100–500 iteraciones; 7–31 hojas; 50–200 muestras por hoja) difieren en centésimas de µg/m³; usar la misma en ambos modelos aísla el efecto de la meteorología. |
| 2026-10-17 | Regla de aviso: el umbral de cada método se fija para que, en los años anteriores al de prueba, emita tantos avisos como eventos hubo, y se congela antes del año de prueba. | Implementa la comparación a igual número de avisos sin fuga de información (revisión externa del 2026-09-16). Para la persistencia el umbral resulta ≈38 µg/m³; para Gradient Boosting ≈35 µg/m³. |
| 2026-10-17 | Estimar la incertidumbre de las diferencias de MAE con bootstrap por bloques de 14 días. | Los errores de días cercanos y estaciones vecinas están correlacionados; remuestrear días sueltos subestimaría la incertidumbre. |

## Decisiones reemplazadas

| Fecha | Decisión original | Reemplazada por |
| --- | --- | --- |
| 2026-09-14 | Forecasting horario a una hora con target `pm25_t_plus_1`. | Pronóstico diario con un día de anticipación. |
| 2026-09-14 | Limitar los datos a PM2.5 y variables temporales. | PM2.5 más meteorología SIATA asignada por estación. |

## Pendiente

- Agregar la meteorología de minuto a hora aplicando la bandera `calidad` y
  cuantificar la cobertura válida por variable y estación.
- Reproducir en el notebook los conteos de eventos y transiciones de
  `context.md` antes de citarlos.
- Evaluar sensibilidad a ceros, valores extremos, definición de media diaria
  (calendario vs. máximo de media móvil) y exclusión de BEL-FEVE y MED-SCRI,
  sin usar información del periodo de prueba.
