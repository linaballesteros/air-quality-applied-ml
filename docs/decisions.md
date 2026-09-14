# Registro de decisiones

## Decisiones vigentes

| Fecha | Decisión | Justificación |
| --- | --- | --- |
| 2026-09-14 | Descargar los archivos originales mediante `?format=original`. | El endpoint por defecto de Dataverse entrega una representación tabulada generada; el original conserva el archivo publicado y coincide con el MD5 oficial. |
| 2026-09-14 | Detectar codificación y delimitador en el loader. | La extensión `.tab` no garantiza tabuladores: la muestra original de 2013-01 usa comas. |
| 2026-09-14 | Permitir cambios de estaciones entre meses y conservar `source_file`. | Se observaron 30 variantes de schema y 33 estaciones históricas. Exigir igualdad descartaría cambios reales de la red. |
| 2026-09-14 | Mantener datos crudos, intermedios y procesados fuera de Git. | Los archivos pueden reproducirse desde la API y no deben inflar el repositorio. |
| 2026-09-14 | Definir forecasting de PM2.5 a una hora como problema de la Entrega 1. | Produce un target inequívoco (`pm25_t_plus_1`), es coherente con el título y puede evaluarse con los datos disponibles. |
| 2026-09-14 | Limitar por ahora los datos a PM2.5 y variables temporales derivadas. | La Entrega 1 exige demostrar viabilidad; no conviene crear infraestructura para fuentes todavía no inspeccionadas. |
| 2026-09-14 | Trabajar inicialmente con 2018–2025 y 16 estaciones con cobertura ≥90%. | Conserva ocho años completos y entre 92,67% y 97,41% de cobertura por estación. |
| 2026-09-14 | No imputar faltantes en el EDA; excluir solo pares sin medición actual o target de la tabla supervisada. | Mantiene transparentes los datos observados y deja 1.050.341 pares utilizables. |
| 2026-09-14 | Conservar ceros y valores fuera de límites IQR. | SIATA reporta mínimos horarios de 0,0 y los extremos pueden ser episodios reales; no existe evidencia para eliminarlos. |

## Pendiente para la Entrega 2

- Definir los cortes temporales de entrenamiento, validación y prueba.
- Comparar los modelos contra el baseline de persistencia (MAE 4,98 µg/m³ en
  el EDA completo; deberá recalcularse únicamente sobre el test futuro).
- Evaluar sensibilidad a ceros y valores extremos sin usar información del
  periodo de prueba para decidir su tratamiento.
