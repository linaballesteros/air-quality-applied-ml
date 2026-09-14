# Diccionario inicial de datos — PM2.5

Fuente: SIATA, *Histórico de Material Particulado - PM2.5*, DOI
`10.83041/AUWZWT`, versión 4.0. Este diccionario describe los archivos
originales descargados; se actualizará al integrar otras fuentes.

| Campo | Tipo cargado | Descripción verificable | Unidad | Nulos | Observaciones |
| --- | --- | --- | --- | --- | --- |
| `fecha_hora` | `datetime64` | Fecha y hora de la medición. Se usa para ordenar la serie y derivar hora, día de semana, mes y año. | Hora local; zona horaria explícita pendiente. | 0 en los 162 archivos | Frecuencia horaria continua entre 2013-01-01 y 2026-06-30. |
| Columnas con código de estación, p. ej. `MED-UNNV` | `float64` | Promedio horario de concentración de PM2.5 medido en la estación del encabezado. | µg/m³ | Variable por estación y periodo | Hay 33 códigos históricos y 30 variantes de schema. |
| `source_file` | `string` (derivada) | Nombre del archivo mensual del cual proviene la fila. | No aplica | 0 | La añade el loader; no existe en el archivo original. |
| `station_id` | `string` (derivada) | Código de estación obtenido al transformar el dataset a formato largo. Permite distinguir el punto de monitoreo. | No aplica | 0 | Variable identificadora/categórica; no es una concentración. |
| `pm25` | `float64` (derivada) | Medición de la estación en la hora `t`. Se puede usar como predictor para anticipar la siguiente hora. | µg/m³ | Se cuantifica antes de construir el target | Proviene del valor de la columna de estación. |
| `pm25_t_plus_1` | `float64` (derivada) | Concentración de la misma estación una hora después. | µg/m³ | Aparece como nulo si falta la medición siguiente | **Variable objetivo de regresión.** Nunca debe incluirse entre los predictores. |

## Forma de los datos

La fuente está en formato ancho: cada fila representa una hora y cada columna
de estación contiene una medición. Para el análisis se transforma a formato
largo, donde cada fila representa una combinación estación-hora. Luego,
dentro de cada estación y respetando el tiempo, se desplaza `pm25` una fila
hacia atrás para crear el target `pm25_t_plus_1`.

## Ejemplo de lectura de columnas originales

| Columna | Significado documentado por SIATA |
| --- | --- |
| `MED-UNNV` | Universidad Nacional de Colombia, Núcleo El Volador. |
| `CEN-TRAF` | Estación Tráfico Centro, ubicada en el Museo de Antioquia. |
| `ITA-CJUS` | Casa de Justicia de Itagüí. |
| `ITA-CONC` | Concejo de Itagüí. |
| `CAL-LASA` | Corporación Universitaria Lasallista. |

Fuente: [`sources/siata_informe_operacion_agosto_2019.md`](sources/siata_informe_operacion_agosto_2019.md).

## Pendientes documentales

- Confirmar oficialmente zona horaria y significado de valores cero.
- Vincular cada código con nombre, municipio, coordenadas y tipo de estación.
- Completar el diccionario de los 33 códigos históricos de estación; el
  informe oficial consultado documenta directamente los códigos principales
  de la muestra inicial.
