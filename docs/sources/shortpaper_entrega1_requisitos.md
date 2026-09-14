

Machine Learning Applied - Short-Paper, Entrega 1


# Short-Paper - Entrega 1


Machine Learning Applied - Parámetros y guía de escritura


Contexto de esta entrega


El short-paper es el proyecto final del curso: identificar un problema real
de su campo, investigación o compañía que pueda abordarse con Machine
Learning, y desarrollarlo rigor metodológico. La entrega se divide en dos
momentos: la Entrega 1 (que define este documento) cubre introducción,
planteamiento del problema, trabajos relacionados, pregunta de investigación
y caracterización de los datos con insights preliminares; la Entrega 2 (se
definirá más adelante) cubrirá la metodología profunda, resultados,
conclusiones y abstract.


El objetivo de dividir la entrega en dos momentos es que reciban
retroalimentación temprana sobre la viabilidad de su problema y sus datos,
antes de invertir tiempo en el modelado completo. Un problema mal planteado
o unos datos que no permiten responder la pregunta de investigación son
mucho más baratos de corregir ahora que en la Entrega 2.


Formato general del documento


<table>
 <tr>
  <th>Parámetro</th>
  <td>Especificación</td>
 </tr>
 <tr>
  <th>Extensión</th>
  <td>3 a 5 páginas (sin contar ni referencias).</td>
 </tr>
 <tr>
  <th>Formato</th>
  <td>IEEE</td>
 </tr>
 <tr>
  <th>Referencias mínimas</th>
  <td>Al menos 3 fuentes (papers, informes de<br/>industria, documentación del dataset).<br/>Wikipedia y blogs no cuentan como fuente<br/>principal.</td>
 </tr>
 <tr>
  <th>Formato de entrega</th>
  <td>Documento en PDF y notebook de EDA (.ipynb o<br/>link a - ambos</td>
 </tr>
 <tr>
  <th>Autoría</th>
  <td>Individual o en grupos de máximo 3 integrantes.<br/>Si es en grupo, incluir los nombres completos</td>
 </tr>
</table>


Componentes de la Entrega 1


El documento debe contener, en este orden, los siguientes componentes:


# 1. Título tentativo


Un título breve y descriptivo (máximo 20 palabras) que refleje el dominio de
aplicación y, si es posible, el tipo de problema (predicción, clasificación,
segmentación). No tiene que ser definitivo - es normal que cambie para la
Entrega 2 a medida que el problema se afina.


# 2. Introducción


Página 1 de 3




Machine Learning Applied - Short-Paper, Entrega 1


Presente el contexto general del dominio o industria donde se ubica el
problema, y por qué es relevante hoy, apoyándose en al menos 1-2 fuentes.
Aquí no se entra en detalle metodológico - esa profundidad es para la
Entrega 2. Extensión sugerida: 300-500 palabras.


Tip: piense en la introducción como un embudo - empieza amplio (el campo) y
termina estrecho (el problema puntual que van a abordar). Evite frases
genéricas de apertura ('en la actualidad, la tecnología avanza...') y vaya
directo al dominio específico.


# 3. Planteamiento del problema


Defina con precisión cuál es el problema específico que se va a abordar: qué
está fallando, qué es ineficiente, o qué decisión sería mejor si se tuviera
un modelo de ML que ayudara a tomarla. Explique el impacto de no resolverlo,
quién se beneficiaría de una solución, y conecte explícitamente el problema
con los datos que planean usar,el problema debe ser resoluble, al menos
parcialmente, con datos a los que tienen o tendrán acceso. (Incluir en la
introducción)


# 4. Trabajos relacionados


Un breve recuento de qué se ha hecho antes para abordar este problema o
problemas similares, con Machine Learning o con otros enfoques. Mencione 2-4
referencias y resuma qué enfoque usaron y qué resultados obtuvieron,
cerrando con qué oportunidad deja abierta ese trabajo previo para su propio
proyecto. Extensión sugerida: 150-250 palabras.


# 5. Pregunta de investigación


Formule 1 (máximo 2) preguntas de investigación centrales, redactadas de
forma explícita y respondible empíricamente con los datos disponibles (ej.
'¿Es posible predecir X a partir de Y con un desempeño aceptable para el
caso de uso?'). Indique qué tipo de problema de ML plantea la pregunta
(supervisado o no supervisado; si es supervisado, regresión o
clasificación), de forma coherente con la caracterización de datos.


# 6. Caracterización de los datos


Describa la fuente de los datos (dataset público, API, encuesta propia,
datos internos), el tamaño y granularidad del dataset. Especifique de forma
explícita y sin ambigüedad cuál es su variable objetivo (target): el nombre
exacto de la columna, su tipo, y si es categórica, cuántas clases tiene y si
están balanceadas; si el proyecto es no supervisado, indique en su lugar qué
variables pueden llegar a ser relevantes en el agrupamiento basado en los
hallazgos de su EDA


Tip: el target debe quedar identificado sin lugar a dudas - un lector que no
conozca su proyecto debe poder responder de inmediato '¿qué predice este
modelo?' con solo leer esta sección.


# 7. Insights preliminares (EDA)


Página 2 de 3




Machine Learning Applied - Short-Paper, Entrega 1


En el documento, presente de forma superficial y resumida los 2-3 hallazgos
más relevantes de su análisis exploratorio, los que mejor respalden la
viabilidad de responder su pregunta de investigación (ej. si la variable
objetivo está balanceada, si hay una relación aparente entre dos variables
clave, o si hay una limitación importante de calidad de datos). No es
necesario incluir código ni un gráfico por cada variable analizada; el EDA
completo y a profundidad va en el notebook (ver siguiente sección), aquí
solo se reportan las conclusiones que le importan al lector del paper, con
una gráfica o dos si ayudan a comunicar el punto.


# Notebook de EDA


El notebook (.ipynb) con el análisis exploratorio completo es un entregable
obligatorio de esta Entrega 1, y es donde debe vivir la profundidad del EDA:
carga y limpieza de datos, estadísticas descriptivas, identificación de
nulos/duplicados/outliers, y todas las visualizaciones relevantes, cada una
acompañada de una celda de markdown explicando qué se observa. El short-
paper solo debe resumir, en la Sección 7, las conclusiones de ese trabajo,
no debe repetir aquí todo lo que ya está documentado en el notebook.


El notebook debe respaldar exactamente lo que se reporta en el documento (si
en el texto dicen 'la variable objetivo está desbalanceada 80/20', esa cifra
debe verse calculada ahí).


Entréguelo como archivo .ipynb adjunto, o como enlace a un repositorio de
GitHub (verifique que sea público).


# Fechas y modo de entrega


Fecha límite de entrega: 19 de septiembre.


Modo de entrega: a través de la plataforma "Interactiva".


Formato de grupo: individual o en grupos de máximo 3 integrantes.


Página 3 de 3


