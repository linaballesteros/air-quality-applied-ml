# Predicción de PM2.5 en el Valle de Aburrá

Este proyecto estudia si es posible pronosticar, con un día de anticipación,
la concentración media diaria de PM2.5 por estación en el Valle de Aburrá.
Para ello utiliza el histórico del contaminante, variables temporales y
mediciones meteorológicas públicas de SIATA.

Autores: Lina Sofía Ballesteros Merchán y Alejandro Ríos Muñoz.

El repositorio contiene el análisis exploratorio, el modelado, la
presentación final y el código necesario para obtener, validar y preparar los
datos utilizados.

## Contenido principal

Los dos notebooks están guardados con sus salidas para que las tablas, cifras
e interpretaciones se puedan visualizar directamente en GitHub o Jupyter sin
repetir primero las descargas.

[`notebooks/01_eda_pm25.ipynb`](notebooks/01_eda_pm25.ipynb) documenta la fuente y estructura de los datos, la calidad y
cobertura, la construcción de la variable objetivo
`pm25_mean_d_plus_1`, los nulos, duplicados y valores extremos, los patrones
temporales y espaciales, la línea base de persistencia y la relación
descriptiva con la meteorología. Cada visualización está acompañada por una
interpretación.

[`notebooks/02_modelado.ipynb`](notebooks/02_modelado.ipynb) construye la
tabla de predictores con ventanas de tiempo y compara la persistencia con
Gradient Boosting sin y con meteorología mediante origen móvil (prueba en
2022, 2023, 2024 y 2025). Evalúa el error, los avisos de Nivel de Prevención
a igual número de avisos y el error en los días críticos, interpreta el
modelo con SHAP y replica el periodo de validación de Baena-Salazar et al.
Todas las cifras del paper final salen de estos dos notebooks.

La presentación final está en
[`presentacion/index.html`](presentacion/index.html) (se abre en el
navegador y funciona sin internet) y en
[`presentacion/presentacion.pdf`](presentacion/presentacion.pdf).

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
jupyter lab
```

Los scripts de descarga no repiten un archivo que ya exista con el MD5
correcto. En una conexión convencional, PM2.5 tarda cerca de un minuto y la
meteorología puede tardar diez minutos o más. `build_meteo_hourly.py` aplica
las banderas de calidad, exige al menos 45 minutos válidos por hora y genera
`data/interim/meteo_hourly.csv`.

La réplica de Baena-Salazar et al. (sección 12 de `02_modelado.ipynb`)
necesita además la meteorología 2013–2016 de dos estaciones (78 archivos,
unos 210 MB):

```bash
python scripts/download_meteo_dataset.py --stations 203,206 --start 2013-01 --end 2016-03 --skip-network
```

Después de abrir cada notebook, seleccione **Restart Kernel and Run All Cells**.
Las celdas de carga comprueban que los datos de cada sección estén presentes y
muestran el comando necesario cuando falta una etapa.

Para ejecutar únicamente el análisis de PM2.5, basta con realizar su descarga
y ejecutar las secciones 1 a 11 del notebook. Las secciones 12 a 15 requieren
también la descarga y agregación meteorológica. El notebook incluido conserva
las salidas de todas las secciones. `02_modelado.ipynb` necesita todas las
descargas y se ejecuta completo en unos tres minutos.

## Organización del repositorio

```text
data/
  raw/             ubicación de los archivos originales descargados
  interim/         tabla meteorológica horaria generada localmente
notebooks/
  01_eda_pm25.ipynb  análisis exploratorio completo
  02_modelado.ipynb  predictores, modelos, avisos, SHAP y réplica de Baena-Salazar
presentacion/
  index.html         presentación final (gráficos dibujados desde datos.js)
  datos.js           cifras de la presentación, exportadas por 02_modelado.ipynb
  presentacion.pdf   versión en PDF de las diapositivas
scripts/
  download_pm25_dataset.py  descarga y valida el histórico de PM2.5
  download_meteo_dataset.py descarga y valida meteorología y metadatos de red
  build_meteo_hourly.py     agrega los registros minutales a resolución horaria
  profile_pm25.py           reproduce el perfil general del histórico
src/data/
  load_pm25.py      carga y valida los archivos mensuales de PM2.5
  load_meteo.py     interpreta calidad y agrega las mediciones meteorológicas
  stations.py       ventana analítica, correspondencias y DOI meteorológicos
src/features/
  build_features.py tabla de predictores con rezagos y ventanas de tiempo
src/models/
  evaluation.py     origen móvil, métricas y regla de aviso
tests/
  test_load_pm25.py      pruebas del cargador con la muestra descargada
  test_load_meteo.py     pruebas de calidad y agregación meteorológica
  test_build_features.py pruebas de la tabla de predictores
  test_evaluation.py     pruebas del origen móvil y las métricas
```

`data/raw` y `data/interim` se crean o completan durante la reproducción.
Los README dentro de `data/raw` registran la procedencia, el esquema y el
comando exacto de descarga de cada fuente.

## Resultados

El análisis utiliza ocho años completos, de 2018 a 2025, y 16 estaciones con
al menos 90% de cobertura horaria. La tabla supervisada contiene 44.399
registros estación-día con la media actual y la variable objetivo del día
siguiente. El notebook conserva los valores altos porque pueden representar
episodios reales, no imputa faltantes durante el EDA y utiliza la persistencia
diaria como línea base.

En los cuatro años de prueba (2022–2025, fuera de muestra):

| Resultado | Persistencia | GB sin meteorología | GB con meteorología |
| --- | --- | --- | --- |
| MAE (µg/m³) | 3,37 | 2,77 | 2,74 |
| R² | 0,56 | 0,71 | 0,71 |
| Inicios de episodio avisados a igual número de avisos (de 123) | 0 | 29 | 30 |

Según SHAP, el PM2.5 del día actual es la entrada con más peso (49,5 % de la
importancia) y la meteorología aporta el 8,6 %.
