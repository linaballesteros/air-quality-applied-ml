

<!-- Contexto original conservado como referencia histórica. -->

````md
# Contexto completo del proyecto — Aprendizaje de Máquina Aplicado ST1631

## 1. Contexto académico

Este proyecto corresponde al curso:

**Aprendizaje de Máquina Aplicado — ST1631**  
**Universidad EAFIT**

Integrantes:

- Lina Sofía Ballesteros Merchán
- Alejandro Ríos Muñoz

El proyecto final del curso consiste en desarrollar un **short paper de Machine Learning**.

La entrega está dividida en dos partes. Actualmente estamos trabajando en:

# Short Paper — Entrega 1

La Entrega 1 busca validar principalmente:

1. que exista un problema real y relevante;
2. que ese problema pueda abordarse mediante Machine Learning;
3. que existan datos suficientes y pertinentes;
4. que la pregunta de investigación sea coherente con esos datos;
5. que el análisis exploratorio respalde la viabilidad del proyecto.

Para esta primera entrega todavía NO se requiere desarrollar el modelado completo.

---

# 2. Requerimientos oficiales de la Entrega 1

El documento debe tener:

- formato IEEE;
- entre 3 y 5 páginas, sin contar referencias;
- mínimo 3 referencias válidas;
- paper en PDF;
- notebook de EDA obligatorio (`.ipynb`) o enlace a repositorio público;
- nombres completos de los integrantes.

Las fuentes válidas incluyen:

- papers académicos;
- informes técnicos;
- documentación oficial de datasets.

No deben utilizarse blogs o Wikipedia como fuente principal.

El documento debe tener, en este orden:

1. Título tentativo
2. Introducción
3. Planteamiento del problema
4. Trabajos relacionados
5. Pregunta de investigación
6. Caracterización de los datos
7. Insights preliminares del EDA
8. Referencias

La introducción debe tener aproximadamente **300–500 palabras** y construirse como un embudo:

contexto general → problema local → problema específico.

Los trabajos relacionados deben contener entre **2 y 4 referencias**, aproximadamente **150–250 palabras**, explicando:

- qué problema abordó cada trabajo;
- qué datos utilizó;
- qué método/modelo utilizó;
- qué resultados obtuvo;
- qué oportunidad queda para nuestro proyecto.

La pregunta de investigación debe ser explícita y empíricamente respondible.

La caracterización del dataset debe dejar completamente claro:

- fuente;
- número de registros;
- número de variables;
- granularidad;
- periodo temporal;
- qué representa una observación;
- target;
- tipo de target;
- valores faltantes;
- duplicados;
- características relevantes del dataset.

La sección de EDA del paper NO debe mostrar todo el análisis.

Solo debe presentar **2 o 3 hallazgos importantes**.

El notebook, en cambio, debe contener el análisis completo:

- carga;
- limpieza;
- estadísticas descriptivas;
- nulos;
- duplicados;
- outliers;
- distribución de variables;
- visualizaciones;
- relaciones entre variables;
- comentarios Markdown explicando cada análisis.

Toda cifra mencionada en el paper debe estar calculada y demostrable en el notebook.

---

# 3. Tema escogido

## Predicción de contaminación atmosférica por PM2.5 en el Valle de Aburrá

Título tentativo actual:

> **Predicción de concentraciones de PM2.5 en el Valle de Aburrá mediante aprendizaje automático con datos de la red SIATA**

No cambiar este título sin una razón metodológica clara.

---

# 4. Problema general

El Valle de Aburrá presenta episodios de deterioro de la calidad del aire asociados, entre otros contaminantes, al material particulado fino PM2.5.

El PM2.5 corresponde a partículas con diámetro aerodinámico igual o inferior a aproximadamente 2.5 µm.

Por su tamaño, estas partículas pueden penetrar profundamente en el sistema respiratorio.

La problemática tiene relevancia particular para población susceptible, incluyendo:

- niños;
- adultos mayores;
- personas con enfermedades respiratorias.

Existe evidencia académica local que relaciona mayores concentraciones de PM2.5 con eventos respiratorios en Medellín y otros municipios del Valle de Aburrá.

El objetivo del proyecto NO es simplemente describir contaminación histórica.

El objetivo es estudiar si los datos disponibles permiten **anticipar o estimar concentraciones horarias de PM2.5 mediante Machine Learning**.

---

# 5. Problema específico planteado

Actualmente la red de monitoreo permite conocer las concentraciones medidas por las estaciones.

Sin embargo, desde una perspectiva preventiva, resulta más útil poder anticipar el comportamiento esperado del contaminante.

El proyecto busca determinar si la información histórica ambiental disponible puede utilizarse para predecir concentraciones horarias de PM2.5.

La utilidad potencial sería apoyar:

- monitoreo ambiental;
- análisis preventivo;
- toma de decisiones;
- sistemas de alerta;
- protección de población vulnerable.

NO afirmar que el proyecto va a construir un sistema oficial de alertas.

La redacción correcta debe ser prudente:

> el modelo podría apoyar o aportar información a mecanismos de alerta y prevención.

---

# 6. Pregunta de investigación actual

La pregunta principal propuesta es:

> **¿Es posible predecir la concentración horaria de PM2.5 en estaciones del Valle de Aburrá a partir de variables meteorológicas, temporales y de contaminantes relacionados mediante modelos supervisados de regresión?**

Esta pregunta todavía debe validarse frente a la estructura real de los datos.

Hay una decisión metodológica pendiente muy importante:

## ¿Qué significa exactamente “predecir concentración horaria”?

Antes de entrenar modelos se debe decidir si se quiere:

### Opción A — estimación contemporánea

Predecir PM2.5 de la hora `t` usando variables disponibles también en la hora `t`.

Ejemplo:

`PM2.5(t) = f(temperatura(t), humedad(t), PM10(t), hora, estación, ...)`

Esto es más cercano a una tarea de **estimación**.

### Opción B — forecasting real

Predecir:

`PM2.5(t+1)`

usando solamente información disponible hasta:

`t`

Ejemplo:

`PM2.5(t+1) = f(PM2.5(t), PM10(t), temperatura(t), humedad(t), hora(t), ...)`

Esto sí constituye una predicción futura/forecast.

La decisión NO debe tomarse arbitrariamente.

Primero se debe revisar:

- qué variables existen;
- cómo están estructuradas;
- qué fechas tienen;
- qué datos meteorológicos pueden sincronizarse;
- qué nivel de completitud presentan.

Para un proyecto de curso, un horizonte `t+1 hora` sería conceptualmente muy interesante si los datos lo permiten.

---

# 7. Tipo de Machine Learning

El proyecto queda definido principalmente como:

**Aprendizaje supervisado**

y específicamente:

**Regresión**

porque la variable objetivo es una cantidad numérica continua:

> concentración de PM2.5 en µg/m³.

NO mezclar en esta etapa regresión con clasificación ICA.

La idea inicial incluía:

- regresión de PM2.5;
- o clasificación de categoría ICA.

Se decidió mantener solo REGRESIÓN como problema principal para que:

- el target sea inequívoco;
- la pregunta de investigación sea clara;
- el proyecto no tenga dos objetivos diferentes.

La clasificación de ICA podría mencionarse en el futuro como posible extensión.

---

# 8. Dataset principal

La fuente principal prevista es el repositorio oficial de datos de SIATA:

**Material Particulado - PM2.5**

Repositorio:

https://datos.siata.gov.co/dataset.xhtml?persistentId=doi:10.83041/AUWZWT

DOI:

**10.83041/AUWZWT**

Autor institucional:

**SIATA (AMVA)**

Descripción:

> Histórico de Material Particulado - PM2.5

El dataset se encuentra en el Repositorio de Datos SIATA / Red de Calidad del Aire.

La versión consultada actualmente es:

**Versión 4.0**

La página contiene archivos históricos mensuales.

Ejemplos:

- `Estaciones_PM2.5_2013_01.tab`
- `Estaciones_PM2.5_2013_02.tab`
- `Estaciones_PM2.5_2013_03.tab`

El repositorio reporta actualmente 162 archivos tabulares públicos.

Los archivos mensuales iniciales tienen 6 variables y típicamente:

- 672 observaciones para meses de 28 días;
- 720 para meses de 30 días;
- 744 para meses de 31 días.

Esto sugiere fuertemente una estructura horaria, pero debe verificarse directamente en los archivos.

NO asumir los nombres exactos de las columnas hasta leerlos.

---

# 9. Datos adicionales potenciales

El proyecto originalmente contempla utilizar:

### Variable objetivo

PM2.5

### Posibles predictores ambientales

- PM10
- NO2
- O3
- CO
- SO2

### Posibles variables meteorológicas

- temperatura;
- humedad;
- precipitación;
- velocidad del viento;
- dirección del viento;
- presión;
- radiación.

### Variables temporales derivables

- hora;
- día de la semana;
- día;
- mes;
- año;
- fin de semana;
- posiblemente variables cíclicas de hora/mes.

NO incluir automáticamente todas estas variables.

Antes de usarlas se debe confirmar:

1. si existen datos disponibles;
2. si tienen rango temporal compatible;
3. si se pueden unir por estación;
4. si se pueden unir por fecha/hora;
5. si tienen suficiente completitud.

---

# 10. Advertencia metodológica importante

NO construir el dataset final haciendo joins sin entender primero la granularidad.

Antes de integrar datasets se debe inspeccionar:

- identificador de estación;
- fecha;
- hora;
- zona horaria;
- granularidad;
- frecuencia;
- nombres de estación;
- cambios históricos de estaciones;
- duplicados;
- valores faltantes;
- códigos especiales para datos inválidos.

La clave de integración probablemente será algo similar a:

`station_id + datetime`

pero esto debe validarse con los archivos reales.

---

# 11. Fuentes académicas recopiladas

Actualmente existen las siguientes fuentes principales.

## Baena-Salazar et al. (2019)

**Red neuronal artificial aplicado para el pronóstico de eventos críticos de PM2.5 en el Valle de Aburrá**

DYNA, 86(209), 347–356.

DOI:

`10.15446/dyna.v86n209.63228`

Aporta:

- antecedente directamente en Valle de Aburrá;
- pronóstico de concentración diaria PM2.5;
- un día de anticipación;
- tres estaciones;
- red neuronal artificial;
- variables meteorológicas;
- variables de calidad del aire.

Variables utilizadas incluyeron, entre otras:

- altura de capa de mezcla;
- temperatura;
- humedad;
- radiación;
- precipitación;
- precipitación acumulada;
- viento;
- concentraciones históricas del contaminante.

Es uno de los antecedentes locales más importantes.

---

## Parra-Sánchez et al. (2020)

**Analítica de datos: incidencia de la contaminación ambiental en la salud pública en Medellín (Colombia)**

Revista de Salud Pública, 22(6).

DOI:

`10.15446/rsap.V22n6.78985`

Aporta:

- contexto Medellín;
- datos de PM2.5 de SIATA;
- meteorología de SIATA;
- relación entre PM2.5 y atenciones por:
  - IRA;
  - EPOC;
  - asma.

Variables meteorológicas estudiadas:

- velocidad del viento;
- temperatura;
- presión;
- precipitación;
- humedad;
- radiación.

También muestra problemas reales de calidad de datos:

- granularidad;
- completitud;
- consistencia;
- necesidad de depuración.

Es una fuente especialmente relevante para justificar:

- importancia local;
- uso de datos SIATA;
- necesidad de revisar calidad de datos.

---

## Grisales-Romero et al. (2022)

**Relación de PM2.5 y Enfermedad Respiratoria Aguda en un territorio de Colombia: Modelos Aditivos Generalizados**

Universidad y Salud, 24(1), 45–54.

DOI:

`10.22267/rus.222401.256`

Aporta:

- evidencia local;
- Valle de Aburrá;
- población menor de 5 años;
- población de 65 años o más;
- asociación entre incrementos de PM2.5 y enfermedad respiratoria aguda.

Estudia datos de 2008–2015.

Es especialmente útil para justificar:

- relevancia de salud pública;
- población susceptible;
- necesidad de monitoreo/previsión.

---

## Kleine Deters et al. (2017)

**Modeling PM2.5 Urban Pollution Using Machine Learning and Selected Meteorological Parameters**

Journal of Electrical and Computer Engineering.

DOI:

`10.1155/2017/5106045`

Aporta:

- aplicación directa de Machine Learning a PM2.5;
- seis años de datos;
- variables meteorológicas;
- viento;
- precipitación;
- clasificación y regresión.

Es particularmente útil para justificar que:

> las variables meteorológicas pueden contener información predictiva sobre PM2.5.

---

## Joharestani et al. (2019)

**PM2.5 Prediction Based on Random Forest, XGBoost, and Deep Learning Using Multisource Remote Sensing Data**

Atmosphere, 10(7), 373.

DOI:

`10.3390/atmos10070373`

Aporta:

- Random Forest;
- XGBoost;
- Deep Learning;
- predicción de PM2.5;
- comparación de modelos.

Puede utilizarse en trabajos relacionados.

---

## Gañan Cardenas (2026)

Tesis doctoral:

**Spatiotemporal forecasting of PM2.5 in the urban areas of Medellín using machine learning**

Universidad Nacional de Colombia.

Aporta:

- antecedente local muy reciente;
- reconstrucción espaciotemporal;
- forecasting horario;
- Medellín / Valle de Aburrá;
- LASSO;
- Transformers;
- meteorología;
- sensores;
- múltiples fuentes ambientales.

Debe utilizarse como referencia complementaria, no como modelo que este proyecto tenga que replicar.

El alcance de esta tesis es considerablemente superior al alcance académico del curso.

---

# 12. Introducción actual del paper

La introducción ya se está redactando en Overleaf.

Su estructura conceptual es:

### Párrafo 1

PM2.5 como problema ambiental y de salud pública.

### Párrafo 2

Contexto específico del Valle de Aburrá y evidencia local sobre salud.

### Párrafo 3

Relación del comportamiento del PM2.5 con meteorología y posibilidad de utilizar datos históricos para predicción.

### Planteamiento del problema

Problema concreto:

> determinar si es posible estimar/predecir la concentración horaria de PM2.5 utilizando información ambiental disponible.

El planteamiento conecta:

- impacto;
- beneficiarios;
- SIATA;
- datos;
- ML supervisado;
- regresión.

---

# 13. EDA — objetivo real

El EDA NO debe convertirse en una colección de gráficas sin propósito.

Debe permitir responder:

## A. ¿Tenemos datos suficientes?

Determinar:

- rango temporal;
- cantidad de observaciones;
- estaciones;
- frecuencia;
- cobertura;
- continuidad.

## B. ¿Cuál es la calidad de los datos?

Analizar:

- nulls;
- duplicados;
- registros imposibles;
- valores extremos;
- gaps temporales;
- estaciones con poca cobertura.

## C. ¿Cómo se comporta PM2.5?

Analizar:

- media;
- mediana;
- desviación;
- percentiles;
- distribución;
- outliers;
- evolución temporal.

## D. ¿Existe estructura temporal?

Analizar PM2.5 por:

- hora;
- día de semana;
- mes;
- año.

NO afirmar de antemano que existen picos en marzo/octubre.

La propuesta inicial tenía como hipótesis:

> posibles picos de contaminación en ciertos periodos del año.

Eso debe demostrarse con el dataset.

## E. ¿Hay diferencias entre estaciones?

Analizar:

- distribución por estación;
- promedio;
- mediana;
- número de registros;
- cobertura temporal;
- missingness.

## F. ¿Existen posibles predictores útiles?

Una vez integrados otros datasets:

- PM2.5 vs PM10;
- PM2.5 vs NO2;
- PM2.5 vs O3;
- PM2.5 vs temperatura;
- PM2.5 vs humedad;
- PM2.5 vs precipitación;
- PM2.5 vs viento.

Utilizar:

- correlaciones;
- scatterplots;
- agregaciones temporales;
- análisis por estación.

NO concluir causalidad a partir de correlación.

---

# 14. EDA mínimo esperado en el notebook

El notebook debe incluir como mínimo:

## 1. Imports y configuración

Ejemplo:

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
````

Agregar otras librerías solo si son necesarias.

---

## 2. Carga de datos

Leer los archivos `.tab` correctamente.

Investigar primero:

* delimitador;
* encoding;
* tipos;
* nombres reales de columnas.

No asumir `sep="\t"` sin verificar, aunque es probable.

---

## 3. Inspección inicial

Ejecutar:

```python
df.head()
df.tail()
df.shape
df.columns
df.info()
df.describe()
```

---

## 4. Calidad

Analizar:

```python
df.isna().sum()
df.isna().mean()
df.duplicated().sum()
```

Además:

* valores imposibles;
* valores negativos;
* códigos sentinela;
* discontinuidades temporales.

---

## 5. Fecha y hora

Identificar la columna temporal real.

Convertirla con:

```python
pd.to_datetime(...)
```

Verificar errores de conversión.

Crear, si aplica:

```python
hour
day_of_week
month
year
```

---

## 6. Variable objetivo PM2.5

Analizar:

* histograma;
* boxplot;
* promedio;
* mediana;
* desviación;
* percentiles;
* mínimos/máximos.

---

## 7. Análisis temporal

Gráficas recomendadas:

* PM2.5 promedio por hora;
* PM2.5 promedio por mes;
* PM2.5 promedio por año;
* serie temporal;
* heatmap hora × mes si aporta información.

---

## 8. Estaciones

Analizar:

* número de observaciones por estación;
* periodo disponible por estación;
* PM2.5 promedio por estación;
* porcentaje de nulos por estación;
* boxplot de PM2.5 por estación.

---

## 9. Relaciones entre variables

Solo después de integrar datos complementarios.

Analizar correlaciones y relaciones visuales.

---

## 10. Markdown explicativo

CADA sección del notebook debe tener celdas Markdown explicando:

* qué se analiza;
* por qué;
* qué se observa;
* qué implicación tiene para el proyecto.

No dejar gráficas sin interpretación.

---

# 15. Insights que podrían terminar en el paper

El paper debe tomar SOLO 2–3 hallazgos del notebook.

Ejemplos de categorías de hallazgos válidos:

* estructura horaria;
* variación mensual;
* diferencias entre estaciones;
* correlación entre PM2.5 y otro contaminante;
* relación con meteorología;
* porcentaje relevante de missing values;
* disponibilidad temporal insuficiente en alguna estación.

IMPORTANTE:

Estos son ejemplos.

NO convertirlos en afirmaciones hasta obtener los resultados reales.

---

# 16. Modelado futuro — Entrega 2

No desarrollar todavía todo esto salvo que sea necesario para decidir el EDA.

Posibles modelos:

### Baseline

Regresión lineal.

### Modelos de comparación

* Random Forest Regressor;
* XGBoost Regressor;
* posiblemente LightGBM si está permitido.

Métricas probables:

* MAE;
* RMSE;
* R².

IMPORTANTE:

Si se decide hacer forecasting temporal `t+1`, NO realizar un train/test split aleatorio tradicional.

Se debería mantener orden temporal.

Esto se decidirá formalmente para la Entrega 2.

---

# 17. Organización recomendada del repositorio
el repo esta creado y clonado en 

`air-quality-applied-ml`

Organizarlo así:

```text
air-quality-applied-ml/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── raw/
│   │   ├── pm25/
│   │   ├── pm10/
│   │   ├── meteorology/
│   │   └── other_pollutants/
│   │
│   ├── interim/
│   │   └── README.md
│   │
│   └── processed/
│       └── README.md
│
├── notebooks/
│   ├── 01_data_inspection_pm25.ipynb
│   ├── 02_data_cleaning_pm25.ipynb
│   ├── 03_eda_pm25.ipynb
│   └── 04_data_integration.ipynb
│
├── src/
│   ├── __init__.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── load_pm25.py
│   │   ├── clean_pm25.py
│   │   └── merge_sources.py
│   │
│   └── utils/
│       ├── __init__.py
│       └── paths.py
│
├── figures/
│   ├── eda/
│   └── paper/
│
├── paper/ --> esto mejor no, lo estamos haciendo en overleaf junto con mi compañero, pero por lo menos que tengamos seccion para ir organizando las partes del entregable que requieren manejo y analisis de acuerdo a lo que hagamos en codigo 
│   ├── main.tex
│   └── referencias.bib
│
└── docs/
    ├── data_dictionary.md
    ├── methodology_notes.md
    └── decisions.md
```

Esta estructura puede simplificarse si el proyecto sigue siendo pequeño.

NO crear arquitectura innecesariamente compleja.

---

# 18. Qué debe ir en Git y qué no

NO subir datos crudos enormes si no es necesario.

Añadir a `.gitignore`, por ejemplo:

```gitignore
data/raw/*
data/interim/*
data/processed/*
!data/raw/README.md
!data/interim/README.md
!data/processed/README.md

__pycache__/
.ipynb_checkpoints/
.venv/
.env
```

Los README dentro de las carpetas de datos deben explicar:

* de dónde se descargan los datos;
* DOI;
* fecha de descarga;
* instrucciones para reproducir el dataset.

---

# 19. README principal esperado

Debe contener:

## Project title

Predicción de concentraciones de PM2.5 en el Valle de Aburrá mediante aprendizaje automático.

## Course

Aprendizaje de Máquina Aplicado ST1631 — Universidad EAFIT.

## Authors

* Lina Sofía Ballesteros Merchán
* Alejandro Ríos Muñoz

## Objective

Breve descripción del problema.

## Data source

SIATA.

DOI del dataset PM2.5:

`10.83041/AUWZWT`

## Repository structure

Explicar las carpetas.

## Setup

Por ejemplo:

```bash
python -m venv .venv
pip install -r requirements.txt
```

## Reproducibility

Explicar:

1. descargar datos;
2. ponerlos en `data/raw`;
3. correr notebooks en orden.

---

# 20. Qué quiero que hagas como Codex

Actúa como un ingeniero de Machine Learning que también entiende investigación académica.

NO empieces entrenando modelos.

Primero revisa el repositorio actual completo.

## Paso 1 — inspección del repo

ten presente que en la carpeta Machine_Learning_Applied se encuentran todos los archivos y carpetas del material del curso, de los que deberias basarte a la hora de realizar analisis y generar codigo

---

## Paso 2 — propuesta de reorganización

Compara el repo real con la estructura recomendada.

Propón cambios mínimos y razonables.

Evita overengineering.

Antes de mover o eliminar archivos importantes, explícame qué quieres hacer.

---

## Paso 3 — dataset

Revisa cómo podemos trabajar con:

SIATA PM2.5:

[https://datos.siata.gov.co/dataset.xhtml?persistentId=doi:10.83041/AUWZWT](https://datos.siata.gov.co/dataset.xhtml?persistentId=doi:10.83041/AUWZWT)

Necesitamos:

1. decidir la mejor forma de descargarlo;
2. conservar una estructura reproducible;
3. no versionar innecesariamente datos pesados;
4. inspeccionar un archivo antes de procesar todos;
5. identificar el schema real.

Primero carga UN archivo, por ejemplo:

`Estaciones_PM2.5_2013_01.tab`
recuerda la estructura y ejemplos ya hechos en clase ** y tambien recuerda que al final hay unos entregables a nivel de notebook 

y muestra:

```python
head()
shape
columns
dtypes
info()
describe()
```

También revisa:

* encoding;
* delimiter;
* fecha/hora;
* estaciones;
* target real;
* valores faltantes.

NO escribas código asumiendo nombres de columnas.

---

## Paso 4 — crear loader reutilizable

Una vez entendido el schema real, crear una función reutilizable para cargar múltiples archivos mensuales.

Debe:

* recorrer archivos;
* cargar correctamente cada uno;
* validar columnas;
* añadir opcionalmente `source_file`;
* concatenar;
* verificar que los schemas sean compatibles.

---

## Paso 5 — crear data dictionary

Generar:

`docs/data_dictionary.md`

con columnas como:

| Columna | Tipo | Descripción | Unidad | Nulls | Observaciones |
| ------- | ---- | ----------- | ------ | ----- | ------------- |

NO inventar descripciones.

Si el significado de una columna no está documentado, marcarlo como pendiente.

---

## Paso 6 — notebook de EDA

El notebook debe estar orientado explícitamente a cumplir la Entrega 1.

No debe parecer un notebook exploratorio desordenado.

Utilizar secciones Markdown claras:

1. Objetivo
2. Fuente de los datos
3. Carga
4. Estructura
5. Calidad
6. Variable objetivo
7. Análisis temporal
8. Análisis por estación
9. Relaciones relevantes
10. Hallazgos principales
11. Limitaciones
12. Implicaciones para la pregunta de investigación

---

# 21. Qué NO hacer

No:

* entrenar modelos todavía sin entender los datos;
* asumir nombres de columnas;
* inventar resultados;
* afirmar correlaciones sin calcularlas;
* afirmar picos marzo/octubre sin demostrarlos;
* imputar datos antes de analizar missingness;
* eliminar outliers automáticamente;
* eliminar nulls automáticamente;
* hacer joins sin verificar granularidad;
* usar datos futuros para predecir datos pasados;
* crear data leakage;
* convertir el proyecto en una tesis de forecasting espaciotemporal;
* crear demasiada infraestructura innecesaria.

---

# 22. Principio metodológico

Toda decisión debe estar justificada.

Ejemplos:

No decir:

> “Eliminamos los nulls”.

Decir:

> “Se identificó X% de valores faltantes. Se evaluó su distribución por estación y periodo antes de decidir su tratamiento.”

No decir:

> “Quitamos outliers”.

Decir:

> “Se identificaron observaciones extremas y se evaluó si corresponden a episodios reales de contaminación o errores de medición.”

Esto es especialmente importante porque concentraciones altas de PM2.5 pueden ser justamente los eventos que queremos aprender a predecir.

---

# 23. Estado actual

Ya existe trabajo en:

* selección del problema;
* revisión bibliográfica;
* definición preliminar del target;
* introducción;
* planteamiento del problema;
* Overleaf;
* BibTeX.

Todavía falta principalmente:

* inspeccionar dataset real;
* confirmar schema;
* decidir rango temporal;
* decidir estaciones;
* confirmar si se integrarán meteorología y otros contaminantes;
* cerrar significado exacto de “predicción horaria”;
* construir EDA;
* obtener insights reales;
* caracterizar datos;
* escribir resultados EDA;
* completar trabajos relacionados;
* cerrar pregunta de investigación.

---

# 24. Tu prioridad inmediata

Primero revisa el repo y la data.

No programes a ciegas.

Quiero que al terminar la primera revisión puedas responder con evidencia:

1. ¿Qué columnas tiene PM2.5?
2. ¿Qué representa cada fila?
3. ¿Cuál es la granularidad exacta?
4. ¿Cuál es el rango temporal?
5. ¿Qué estaciones aparecen?
6. ¿Cuál es la columna objetivo?
7. ¿Cuántos valores faltantes existen?
8. ¿Hay duplicados?
9. ¿Hay códigos de datos inválidos?
10. ¿Cómo están representadas fecha y hora?
11. ¿Todos los archivos mensuales comparten schema?
12. ¿Qué tamaño tendrá el dataset consolidado?
13. ¿Tiene sentido trabajar con todas las estaciones?
14. ¿Qué rango temporal conviene usar?
15. ¿Qué datos adicionales debemos integrar para responder correctamente la pregunta de investigación?

Después de responder esto, proponme el plan exacto para completar el EDA de la Entrega 1.

```

Un ajuste importante que hice en ese prompt es separar **estimación contemporánea** de **forecasting real**. Eso todavía tenemos que decidir nosotros, porque “predecir concentración horaria” es ambiguo: predecir `PM2.5(t)` usando meteorología de `t` no es lo mismo que anticipar `PM2.5(t+1)`. Para un paper bien planteado, esa diferencia debe quedar cerrada antes de la pregunta final y antes del modelado.

Sobre la data, el repositorio oficial nos da una ventaja grande: los archivos están publicados de forma mensual y pueden descargarse directamente en formato tabular; además, SIATA identifica formalmente el dataset con DOI y pide que se cite en investigaciones que lo utilicen. :contentReference[oaicite:1]{index=1} Eso significa que en `data/raw/` yo **no versionaría los 162 archivos en Git**; dejaría un README con la fuente, DOI e instrucciones de descarga.

Y el enfoque que le estoy pidiendo a Codex para el EDA está alineado literalmente con el entregable: el notebook debe contener carga/limpieza, estadísticas descriptivas, nulos, duplicados, outliers y visualizaciones explicadas en Markdown; el paper solo debe tomar 2–3 hallazgos y cualquier cifra mencionada allí debe poder verificarse en el notebook. :contentReference[oaicite:2]{index=2} La caracterización, además, debe especificar tamaño, granularidad y target sin ambigüedad. :contentReference[oaicite:3]{index=3}

Yo haría ahora esto: **pásale este prompt a Codex dentro del repo y pídele primero únicamente que inspeccione la estructura actual y proponga la reorganización, sin modificar nada aún**. Después me traes lo que encontró y revisamos juntos si la estructura y el plan de datos tienen sentido antes de que empiece a mover archivos o escribir el EDA.
```

[1]: https://datos.siata.gov.co/dataset.xhtml?persistentId=doi%3A10.83041%2FAUWZWT "Material Particulado - PM2.5 - Red Calidad del Aire"
