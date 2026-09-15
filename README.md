# Predicción de PM2.5 en el Valle de Aburrá

Proyecto del curso Aprendizaje de Máquina Aplicado — ST1631 de la Universidad
EAFIT. Estudia si es posible pronosticar, con un día de anticipación, la
concentración media diaria de PM2.5 por estación en el Valle de Aburrá con
datos públicos de SIATA (histórico del contaminante y meteorología) y
aprendizaje supervisado de regresión.

Autores: Lina Sofía Ballesteros Merchán y Alejandro Ríos Muñoz.

## Datos

Fuente principal: SIATA, *Histórico de Material Particulado - PM2.5*, DOI
[`10.83041/AUWZWT`](https://datos.siata.gov.co/dataset.xhtml?persistentId=doi:10.83041/AUWZWT).

Meteorología: colección *Meteorológica* de SIATA, una estación por dataset;
la correspondencia con las estaciones PM2.5 está en
[`docs/station_matching.md`](docs/station_matching.md).

Los datos crudos no se versionan. Para descargarlos y validar cada archivo con
el MD5 oficial:

```bash
python scripts/download_pm25_dataset.py --all
python scripts/download_meteo_dataset.py
```

## Instalación

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate       # Linux / macOS
pip install -r requirements.txt
```

## Puesta en marcha en una máquina nueva

Ejecutar en este orden desde la raíz del repositorio (tiempos aproximados):

```bash
python scripts/download_pm25_dataset.py --all   # 162 archivos, 15 MB, ~1 min
python scripts/download_meteo_dataset.py        # 1.131 archivos, 3 GB, ~10 min
python scripts/build_meteo_hourly.py            # tabla horaria en data/interim, ~2 min
python -m unittest discover -q                  # 13 pruebas
jupyter lab                                     # abrir notebooks/01_eda_pm25.ipynb
```

Ninguna descarga se repite si el archivo ya existe con el MD5 correcto. El
notebook está guardado con sus salidas; puede leerse sin ejecutarlo, pero
para reejecutarlo se necesitan las tres primeras líneas.

## Dónde está cada cosa

- Estado, pregunta vigente, cifras verificadas y siguientes pasos:
  [`context.md`](context.md).
- Qué debe decir cada sección del paper: [`docs/entrega1_contenido.md`](docs/entrega1_contenido.md).
- Borrador del paper y referencias: [`paper/`](paper/).
- Decisiones metodológicas con justificación: [`docs/decisions.md`](docs/decisions.md).

## Estructura

```text
data/       archivos originales de PM2.5, meteorología y redes (excluidos de Git)
docs/       decisiones, diccionario, cruce de estaciones, guía de la entrega y fuentes
notebooks/  EDA ejecutado de la Entrega 1
paper/      borrador IEEEtran del short paper y referencias
scripts/    descarga, perfil y agregación de los datasets
src/        funciones reutilizables de carga, validación y correspondencia de estaciones
tests/      pruebas unitarias de los loaders
```
