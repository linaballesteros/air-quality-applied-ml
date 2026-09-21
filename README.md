# Predicción de PM2.5 en el Valle de Aburrá

Este proyecto estudia si es posible pronosticar, con un día de anticipación,
la concentración media diaria de PM2.5 por estación en el Valle de Aburrá.
Para ello utiliza el histórico del contaminante, variables temporales y
mediciones meteorológicas públicas de SIATA.

Autores: Lina Sofía Ballesteros Merchán y Alejandro Ríos Muñoz.

El repositorio contiene el análisis exploratorio y el código necesario para
obtener, validar y preparar los datos utilizados.

## Contenido principal

El archivo principal es
[`notebooks/01_eda_pm25.ipynb`](notebooks/01_eda_pm25.ipynb). Está guardado con
sus salidas para que las tablas, cifras e interpretaciones se puedan visualizar
directamente en GitHub o Jupyter sin repetir primero las descargas.

El notebook documenta la fuente y estructura de los datos, la calidad y
cobertura, la construcción de la variable objetivo
`pm25_mean_d_plus_1`, los nulos, duplicados y valores extremos, los patrones
temporales y espaciales, la línea base de persistencia y la relación
descriptiva con la meteorología. Cada visualización está acompañada por una
interpretación.

## Fuentes de datos

La fuente principal es el dataset público de SIATA *Histórico de Material
Particulado - PM2.5*, DOI
[`10.83041/AUWZWT`](https://datos.siata.gov.co/dataset.xhtml?persistentId=doi:10.83041/AUWZWT).
La versión 4.0 utilizada en el análisis contiene 162 archivos mensuales
entre enero de 2013 y junio de 2026.

La meteorología proviene de la colección *Meteorológica* de SIATA. Cada
estación se publica como un dataset independiente. Los DOI y la
correspondencia entre las 16 estaciones de PM2.5 y las 12 estaciones
meteorológicas utilizadas están declarados en `src/data/stations.py`.

Los scripts consultan la API oficial, descargan el formato original y validan
el MD5 publicado por SIATA. La descarga de PM2.5 ocupa cerca de 15 MB. La
meteorología minutal ocupa aproximadamente 3 GB, por lo que se debe disponer de
espacio adicional para la tabla horaria intermedia.

## Requisitos e instalación

Se recomienda Python 3.11 o 3.12. Desde la raíz del repositorio, cree un
entorno virtual e instale las dependencias.

En Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

En Linux o macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Reproducción completa

Ejecute los siguientes comandos desde la raíz del repositorio y en este orden:

```bash
python scripts/download_pm25_dataset.py --all
python scripts/download_meteo_dataset.py
python scripts/build_meteo_hourly.py
python -m unittest discover -v
jupyter lab notebooks/01_eda_pm25.ipynb
```

Los scripts de descarga no repiten un archivo que ya exista con el MD5
correcto. En una conexión convencional, PM2.5 tarda cerca de un minuto y la
meteorología puede tardar diez minutos o más. `build_meteo_hourly.py` aplica
las banderas de calidad, exige al menos 45 minutos válidos por hora y genera
`data/interim/meteo_hourly.csv`.

Después de abrir el notebook, seleccione **Restart Kernel and Run All Cells**.
Las celdas de carga comprueban que los datos de cada sección estén presentes y
muestran el comando necesario cuando falta una etapa.

Para ejecutar únicamente el análisis de PM2.5, basta con realizar su descarga
y ejecutar las secciones 1 a 11 del notebook. Las secciones 12 a 15 requieren
también la descarga y agregación meteorológica. El notebook incluido conserva
las salidas de todas las secciones.

## Organización del repositorio

```text
data/
  raw/             ubicación de los archivos originales descargados
  interim/         tabla meteorológica horaria generada localmente
notebooks/
  01_eda_pm25.ipynb  análisis exploratorio completo
scripts/
  download_pm25_dataset.py  descarga y valida el histórico de PM2.5
  download_meteo_dataset.py descarga y valida meteorología y metadatos de red
  build_meteo_hourly.py     agrega los registros minutales a resolución horaria
  profile_pm25.py           reproduce el perfil general del histórico
src/data/
  load_pm25.py      carga y valida los archivos mensuales de PM2.5
  load_meteo.py     interpreta calidad y agrega las mediciones meteorológicas
  stations.py       ventana analítica, correspondencias y DOI meteorológicos
tests/
  test_load_pm25.py pruebas del cargador con la muestra descargada
  test_load_meteo.py pruebas de calidad y agregación meteorológica
```

`data/raw` y `data/interim` se crean o completan durante la reproducción.
Los README dentro de `data/raw` registran la procedencia, el esquema y el
comando exacto de descarga de cada fuente.

## Resultados reproducidos por el notebook

El análisis utiliza ocho años completos, de 2018 a 2025, y 16 estaciones con
al menos 90% de cobertura horaria. La tabla supervisada contiene 44.399
registros estación-día con la media actual y la variable objetivo del día
siguiente. El notebook conserva los valores altos porque pueden representar
episodios reales, no imputa faltantes durante el EDA y utiliza la persistencia
diaria como línea base. Este análisis caracteriza la viabilidad del problema y
establece la información que se utilizará posteriormente para entrenar y
comparar modelos.
