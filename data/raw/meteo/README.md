# Datos crudos de la red meteorológica

Fuente oficial: Repositorio de Datos SIATA, colección *Meteorológica*. Cada
estación es un dataset independiente con un archivo mensual y resolución de
un minuto. Los DOI de las estaciones requeridas están en
`src/data/stations.py`; la descripción de la red está en el dataset
*Información de la Red Meteorológica* (DOI `10.83041/NXHIKW`), descargado a
`data/raw/network/meteorologica/`.

- Consulta comprobada: `2026-09-14`
- Estructura local: `data/raw/meteo/<código>/Estacion_meteorologica_<código>_YYYY_MM.tab`
- Delimitador: coma, pese a la extensión `.tab`

Columnas de cada archivo: `codigo`, `fecha_hora`, `h` (humedad relativa, %),
`t` (temperatura, °C), `pr` (presión, hPa), `vv` y `vv_max` (velocidad del
viento promedio y máxima, m/s), `dv` y `dv_max` (dirección del viento, grados),
`p` (precipitación, mm) y `calidad`. No hay celdas vacías: los datos
dudosos se marcan con la bandera `calidad` (1 y 2 confiables; 151 dudoso en
todas las variables; 153 `t`, 154 `h`, 155 `pr`, 156x viento, 157x dirección,
1511 `p`; las banderas se concatenan cuando afectan a varias variables, por
ejemplo 1534). Ver `Generalidades_Meteorologicas.pdf`.

Descarga de las estaciones asignadas para la ventana 2018-01 a 2025-12:

```bash
python scripts/download_meteo_dataset.py
```

El script valida el MD5 publicado por Dataverse y no repite descargas
correctas. Los archivos están excluidos de Git. No editar los datos crudos.
