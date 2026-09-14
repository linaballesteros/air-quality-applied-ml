# Predicción de PM2.5 en el Valle de Aburrá

Proyecto del curso Aprendizaje de Máquina Aplicado — ST1631 de la Universidad
EAFIT. Estudia la viabilidad de estimar o anticipar concentraciones horarias
de PM2.5 con datos públicos de SIATA y aprendizaje supervisado de regresión.

Autores: Lina Sofía Ballesteros Merchán y Alejandro Ríos Muñoz.

## Datos

Fuente principal: SIATA, *Histórico de Material Particulado - PM2.5*, DOI
[`10.83041/AUWZWT`](https://datos.siata.gov.co/dataset.xhtml?persistentId=doi:10.83041/AUWZWT).

Los datos crudos no se versionan. Para descargarlos y validar cada archivo con
el MD5 oficial:

```bash
python scripts/download_pm25_dataset.py --all
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
python scripts/profile_pm25.py
jupyter lab
```

Abrir `notebooks/01_eda_pm25.ipynb` para reproducir la inspección y el EDA
documentado. El estado y las decisiones vigentes se mantienen en
[`context.md`](context.md).

## Estructura

```text
data/       archivos originales de PM2.5 (excluidos de Git)
docs/       contexto, decisiones, diccionario y fuentes consultables
notebooks/  análisis reproducibles de la entrega
scripts/    descarga y perfil del dataset
src/        funciones reutilizables de carga y validación
```
