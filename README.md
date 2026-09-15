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
.venv\Scripts\activate
pip install -r requirements.txt
```

## Reproducción

```bash
python scripts/download_pm25_dataset.py --all
python scripts/download_meteo_dataset.py
python scripts/profile_pm25.py
jupyter lab
```

Abrir `notebooks/01_eda_pm25.ipynb` para reproducir la inspección y el EDA
documentado. El estado y las decisiones vigentes se mantienen en
[`context.md`](context.md).

## Estructura

```text
data/       archivos originales de PM2.5, meteorología y redes (excluidos de Git)
docs/       contexto, decisiones, diccionario, cruce de estaciones y fuentes
notebooks/  análisis reproducibles de la entrega
scripts/    descarga y perfil de los datasets
src/        funciones reutilizables de carga, validación y correspondencia de estaciones
```
