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
| `pm25` | `float64` (derivada) | Medición de la estación en la hora `t`. Insumo de las medias diarias y de predictores autorregresivos. | µg/m³ | Se cuantifica antes de construir el target | Proviene del valor de la columna de estación. |
| `pm25_mean` | `float64` (derivada) | Media de PM2.5 de la estación en el día calendario `d`, calculada solo si hay al menos 18 horas válidas. | µg/m³ | Nulo si el día tiene menos de 18 horas | Predictor principal (persistencia) y base del target. |
| `pm25_mean_d_plus_1` | `float64` (derivada) | Media diaria de la misma estación en el día siguiente `d+1`. | µg/m³ | Nulo si falta la media del día siguiente | **Variable objetivo de regresión.** Nunca debe incluirse entre los predictores. |
| `prevencion_d_plus_1` | `bool` (derivada) | Indicador `pm25_mean_d_plus_1 >= 38`, Nivel de Prevención de la Resolución 2254 de 2017. | No aplica | Igual que el target | Solo para evaluación; no se entrena como clasificación. |

## Forma de los datos

La fuente está en formato ancho: cada fila representa una hora y cada columna
de estación contiene una medición. Para el análisis se transforma a formato
largo, donde cada fila representa una combinación estación-hora. Luego se
agrega por estación y día calendario para obtener `pm25_mean` y, dentro de
cada estación y respetando el tiempo, se desplaza un día hacia atrás para
crear el target `pm25_mean_d_plus_1`.

## Meteorología (pendiente de agregación)

Archivos minutales por estación con columnas `codigo`, `fecha_hora`, `h`,
`t`, `pr`, `vv`, `vv_max`, `dv`, `dv_max`, `p` y `calidad`; ver
[`../data/raw/meteo/README.md`](../data/raw/meteo/README.md) y la
correspondencia en [`station_matching.md`](station_matching.md). Las
variables horarias derivadas se documentarán aquí cuando exista el loader.

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
