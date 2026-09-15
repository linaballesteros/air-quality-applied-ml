# Correspondencia entre estaciones PM2.5 y meteorológicas

Calculada el 2026-09-14 con las coordenadas oficiales de SIATA:

- Red de calidad del aire: dataset *Información de la Red de Calidad del
  Aire*, DOI `10.83041/XTI3FH`, archivo `Estaciones_calidad_aire.tab`.
- Red meteorológica: dataset *Información de la Red Meteorológica*, DOI
  `10.83041/NXHIKW`, archivo `Estaciones_meteorologica.tab`.

Ambos se descargan a `data/raw/network/` con
`python scripts/download_meteo_dataset.py`. La distancia es haversine entre
coordenadas publicadas. La cobertura de meses se verificó contra el catálogo
de archivos de cada dataset meteorológico para 2018-01 a 2025-12.

## Asignación vigente

Criterio: estación meteorológica más cercana instalada antes de 2018-01-01,
salvo que una más cercana instalada en 2018 cubra casi toda la ventana.

| Estación PM2.5 | Municipio | Cobertura PM2.5 2018–25 | Meteorológica | Distancia | Meses con archivo (de 96) | Nota |
| --- | --- | --- | --- | --- | --- | --- |
| CEN-TRAF | Medellín | 94,2 % | 202 AMVA | 1,2 km | 96 | |
| ITA-CJUS | Itagüí | 96,8 % | 252 Alcaldía Envigado | 2,0 km | 96 | |
| ITA-CONC | Itagüí | 95,3 % | 206 Colegio Concejo de Itagüí | 0,1 km | 96 | |
| MED-ALTA | Medellín | 94,9 % | 197 Universidad de Medellín | 0,9 km | 96 | |
| MED-BEME | Medellín | 96,3 % | 197 Universidad de Medellín | 1,4 km | 96 | Comparte estación con MED-ALTA. |
| EST-HOSP | La Estrella | 97,4 % | 229 Alcaldía La Estrella | 0,4 km | 95 | Falta 2024-08. |
| BAR-TORR | Barbosa | 93,2 % | 82 I.E. Manuel José Caicedo | 0,5 km | 95 | Falta 2025-11. |
| COP-CVID | Copacabana | 96,6 % | 73 Ciudadela Educativa La Vida | 0,0 km | 96 | Mismo sitio. |
| MED-VILL | Medellín | 94,7 % | 68 Jardín Botánico | 1,5 km | 94 | Faltan 2023-10 y 2023-11. |
| MED-ARAN | Medellín | 96,2 % | 68 Jardín Botánico | 2,8 km | 94 | Comparte estación con MED-VILL. |
| MED-TESO | Medellín | 95,3 % | 59 ISAGEN | 1,6 km | 96 | |
| ENV-HOSP | Envigado | 96,4 % | 252 Alcaldía Envigado | 0,7 km | 96 | Comparte estación con ITA-CJUS. |
| CAL-JOAR | Caldas | 94,0 % | 105 Parque 3 Aguas | 0,4 km | 96 | |
| SAB-RAME | Sabaneta | 92,7 % | 229 Alcaldía La Estrella | 2,7 km | 95 | La 318 está a 0,0 km pero inicia 2018-06. |
| **BEL-FEVE** | Bello | 95,3 % | 271 Jorge Eliécer Gaitán | 1,0 km | **79** | Sin archivos desde 2024-08. La alternativa previa a 2018 (73) queda a 7,0 km. |
| **MED-SCRI** | Medellín (San Cristóbal) | 95,3 % | 201 Torre SIATA | **5,8 km** | 96 | San Cristóbal no tiene meteorológica propia antes de 2024. |

Estaciones meteorológicas únicas requeridas: 59, 68, 73, 82, 105, 197, 201,
202, 206, 229, 252 y 271. La correspondencia está codificada en
[`../src/data/stations.py`](../src/data/stations.py).

## Decisiones asociadas

- BEL-FEVE y MED-SCRI se conservan con su asignación imperfecta y se reportan
  como limitación; se evaluará la sensibilidad de los resultados al
  excluirlas.
- La cobertura real por variable se calcula con
  `python scripts/build_meteo_hourly.py` (ver sección siguiente).

## Cobertura horaria válida 2018–2025

Porcentaje de las 70.128 horas de la ventana con valor válido tras aplicar la
bandera `calidad` y exigir 45 minutos válidos por hora. Reproducible con
`python scripts/build_meteo_hourly.py`; resultado del 2026-09-14.

| Meteorológica | h | t | pr | vv | vv_max | dv | p |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 59 | 94,5 | 94,1 | 94,5 | 94,5 | 94,5 | 94,5 | 94,5 |
| 68 | 93,9 | 92,2 | 93,9 | 93,8 | 93,8 | 93,8 | 93,9 |
| 73 | 96,1 | 93,2 | 96,1 | 96,0 | 96,0 | 93,5 | 96,1 |
| 82 | 95,8 | 94,0 | 95,8 | 95,6 | 95,6 | 95,6 | 95,8 |
| 105 | 95,2 | 91,8 | 95,2 | 95,4 | 95,4 | 95,4 | 95,4 |
| 197 | 87,9 | 90,7 | 90,7 | 92,2 | 91,5 | 92,2 | 92,2 |
| 201 | 95,8 | 88,1 | 95,8 | 95,8 | 95,8 | 95,8 | 95,8 |
| 202 | 97,7 | 94,4 | 97,7 | 97,8 | 97,8 | 97,8 | 97,8 |
| 206 | 94,8 | 92,9 | 94,8 | **32,8** | **32,8** | **32,8** | 94,8 |
| 229 | 90,3 | 92,8 | 92,4 | 92,7 | 91,6 | 92,7 | **74,3** |
| 252 | 95,8 | 95,8 | **14,6** | 95,7 | 94,6 | 95,7 | 95,8 |
| 271 | 77,2 | 79,6 | 79,6 | 79,6 | 78,4 | 79,6 | 79,6 |

Huecos estructurales (sensor ausente durante periodos largos, no ruido):

| Estación | Variable | Periodo sin datos | Estaciones PM2.5 afectadas | Alternativa a evaluar |
| --- | --- | --- | --- | --- |
| 206 | viento (`vv`, `vv_max`, `dv`) | mediados de 2019 a mediados de 2024 | ITA-CONC | 397 *Concejo de Itagüí - Thies*, mismo sitio, instalada 2019-09-27 |
| 252 | presión (`pr`) | desde 2019 | ITA-CJUS, ENV-HOSP | Presión de 59 o 197 (variable espacialmente suave) o excluir `pr` |
| 229 | precipitación (`p`) | 2022 a 2024, parcial | EST-HOSP, SAB-RAME | 318 *Rafael J. Mejía* (Sabaneta, desde 2018-06) o red pluviométrica |
| 271 | todas | desde 2024-08 | BEL-FEVE | Ninguna cercana anterior a 2018; reportar como limitación |

Ninguna alternativa se ha incorporado todavía; la decisión se toma al
construir los predictores.

## Fechas de operación de PM2.5

El archivo `Fechas_monitoreo_calidad_aire.tab` publica las fechas de
activación y suspensión de PM2.5 por estación. Para las 16 seleccionadas, la
activación es anterior a 2018-03-18 (SAB-RAME es la más reciente) y ninguna
registra suspensión dentro de la ventana.
