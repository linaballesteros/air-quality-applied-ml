\documentclass[conference]{IEEEtran}
\IEEEoverridecommandlockouts

% =================================================
% PAQUETES
% =================================================

\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[spanish,es-noquoting]{babel}

\usepackage{cite}
\usepackage{amsmath,amssymb}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{array}
\usepackage{textcomp}
\usepackage{xcolor}
\usepackage{hyperref}

\hypersetup{
    colorlinks=true,
    linkcolor=black,
    citecolor=black,
    urlcolor=blue
}

% =================================================
% DOCUMENTO
% =================================================

\begin{document}

% =================================================
% TÍTULO
% =================================================

\title{Predicción de concentraciones de PM2.5 en el Valle de Aburrá mediante aprendizaje automático con datos de la red SIATA}

% Reemplazar con sus nombres completos
\author{
\IEEEauthorblockN{
Lina Sofía Ballesteros Merchán,
Alejandro Ríos Muñoz
}

\IEEEauthorblockA{
Universidad EAFIT\\
Aprendizaje de Máquina Aplicado ST1631\\
Medellín, Colombia
}
}

\maketitle


% =================================================
% I. INTRODUCCIÓN
% =================================================

\section{Introducción}
\label{sec:introduccion}

La contaminación atmosférica constituye un problema ambiental y de salud
pública debido a la exposición de la población a contaminantes capaces de
afectar los sistemas respiratorio y cardiovascular. Entre ellos, el material
particulado fino PM$_{2.5}$ corresponde a partículas con un diámetro
aerodinámico inferior a 2.5 $\mu$m, cuyo tamaño reducido favorece su
penetración en las zonas profundas del sistema respiratorio
\cite{grisales2022relacion}. La exposición a este contaminante ha sido
relacionada con diferentes afectaciones respiratorias, lo que hace
especialmente relevante su seguimiento en entornos urbanos con episodios de
deterioro de la calidad del aire \cite{parra2020analitica}.

Esta problemática es de gran importancia en el Valle de Aburrá, pues la
configuración geográfica del territorio, caracterizada por un valle estrecho
rodeado de montañas, junto con determinadas condiciones meteorológicas, puede
dificultar la dispersión de los contaminantes y favorecer su acumulación
\cite{baena2019red}. Estudios realizados en la región han encontrado evidencia
de la relación entre las concentraciones de PM$_{2.5}$ y diferentes eventos
de salud. Parra-Sánchez et al. identificaron asociaciones entre este
contaminante y las atenciones médicas por infección respiratoria aguda,
enfermedad pulmonar obstructiva crónica y asma en Medellín
\cite{parra2020analitica}. De manera similar, Grisales-Romero et al.
reportaron incrementos significativos de enfermedad respiratoria aguda en
menores de cinco años y adultos de 65 años o más en municipios del Valle de
Aburrá ante aumentos en la concentración de PM$_{2.5}$
\cite{grisales2022relacion}.

El comportamiento del PM$_{2.5}$ no depende únicamente de las emisiones, sino
también de condiciones meteorológicas que intervienen en su transporte,
dispersión y acumulación. Variables como la temperatura, la humedad, la
precipitación y el viento han sido utilizadas para estudiar y predecir sus
concentraciones \cite{kleine2017modeling}. En el contexto local,
Baena-Salazar et al. desarrollaron una red neuronal artificial para
pronosticar la concentración diaria de PM$_{2.5}$ en el Valle de Aburrá con
un día de anticipación a partir de información meteorológica y de calidad del
aire \cite{baena2019red}. Trabajos más recientes también han explorado el
pronóstico horario y espaciotemporal de PM$_{2.5}$ en Medellín mediante
técnicas de aprendizaje de máquina \cite{ganan2026spatiotemporal}. Estos
antecedentes muestran que la información histórica disponible puede utilizarse
para estudiar relaciones predictivas entre las condiciones ambientales y las
concentraciones del contaminante.



\subsection{Planteamiento del problema}
\label{sec:problema}

El monitoreo de la calidad del aire permite conocer las concentraciones de
PM$_{2.5}$ registradas en distintos puntos del Valle de Aburrá; sin embargo,
para la gestión preventiva de episodios de contaminación resulta relevante
contar con herramientas capaces de anticipar su comportamiento. Esta necesidad
adquiere especial importancia debido a que las concentraciones del contaminante
están condicionadas tanto por las emisiones como por factores meteorológicos
que afectan su transporte, dispersión y acumulación
\cite{baena2019red,kleine2017modeling}. En el contexto local, además, se ha
documentado la relación entre mayores concentraciones de PM$_{2.5}$ y eventos
de salud respiratoria, particularmente en grupos de población vulnerables
\cite{parra2020analitica,grisales2022relacion}.

Por tanto, el problema abordado en este proyecto consiste en determinar si es
posible estimar la concentración horaria de PM$_{2.5}$ en estaciones del
Valle de Aburrá a partir de información ambiental disponible. Para ello se
utilizarán registros históricos de la red SIATA, considerando como posibles
variables predictoras información meteorológica, variables temporales y
mediciones de otros contaminantes atmosféricos que puedan integrarse de manera
consistente con los registros de PM$_{2.5}$. La disponibilidad de estas
mediciones hace posible formular el problema como una tarea de aprendizaje
supervisado de regresión, cuya variable objetivo será la concentración horaria
de PM$_{2.5}$ expresada en $\mu$g/m$^3$.

Un modelo con capacidad para anticipar estas concentraciones podría complementar
los procesos actuales de monitoreo al proporcionar información previa sobre el
comportamiento esperado del contaminante. Esto podría ser útil para apoyar la
toma de decisiones de las autoridades ambientales y fortalecer mecanismos de
prevención y alerta frente a episodios de deterioro de la calidad del aire,
con especial relevancia para poblaciones susceptibles a sus efectos
respiratorios.

% =================================================
% II. TRABAJOS RELACIONADOS
% =================================================

\section{Trabajos relacionados}
\label{sec:trabajos}

En esta sección se presentarán entre dos y cuatro trabajos relacionados
con el problema seleccionado.

Para cada trabajo se recomienda explicar brevemente:

\begin{itemize}
    \item Qué problema abordaron los autores.
    \item Qué conjunto de datos utilizaron.
    \item Qué técnica o modelo de Machine Learning aplicaron.
    \item Qué resultados principales obtuvieron.
\end{itemize}

Finalmente, se debe explicar qué oportunidad queda abierta a partir de
los trabajos existentes y cómo el proyecto propuesto se relaciona con
ellos.

Cuando se seleccionen las fuentes académicas reales del proyecto,
se agregarán aquí las citas correspondientes.


% =================================================
% III. PREGUNTA DE INVESTIGACIÓN
% =================================================

\section{Pregunta de investigación}
\label{sec:pregunta}

La pregunta de investigación principal del proyecto será formulada
de manera que pueda responderse empíricamente utilizando los datos
disponibles.

Una estructura posible es:

\begin{quote}
\textit{¿Es posible predecir [variable objetivo] a partir de
[variables predictoras] mediante técnicas de Machine Learning con
un desempeño adecuado para [caso de uso]?}
\end{quote}

Una vez seleccionado el problema definitivo, esta pregunta deberá
ajustarse específicamente al dominio y a los datos utilizados.

El problema corresponde a una tarea de aprendizaje
\textbf{supervisado o no supervisado}.

Si se trata de aprendizaje supervisado, se deberá indicar además si es
un problema de:

\begin{itemize}
    \item Clasificación, o
    \item Regresión.
\end{itemize}

Si se trata de aprendizaje no supervisado, se deberá indicar si el
objetivo principal es, por ejemplo, realizar segmentación o agrupamiento
de observaciones.


% =================================================
% IV. CARACTERIZACIÓN DE LOS DATOS
% =================================================

\section{Caracterización de los datos}
\label{sec:datos}

El conjunto de datos utilizado en este proyecto proviene de
\textit{[indicar fuente del dataset]}.

El dataset contiene aproximadamente \textbf{XX registros} y
\textbf{XX variables}. Cada observación representa
\textit{[explicar qué representa una fila del dataset]}.

Las variables incluyen información relacionada con
\textit{[describir de manera general los principales grupos de variables]}.

La variable objetivo del proyecto es:

\begin{quote}
\texttt{nombre\_variable\_objetivo}
\end{quote}

Esta variable es de tipo \textit{[numérica / categórica / binaria]}.

Si el problema es de clasificación, la variable objetivo contiene
\textbf{XX clases}. La distribución de dichas clases deberá analizarse
para determinar si el conjunto de datos se encuentra balanceado o
desbalanceado.

Si el problema es de regresión, se deberá analizar la distribución de
la variable objetivo, incluyendo medidas descriptivas y posibles valores
atípicos.

La Tabla~\ref{tab:dataset} resume las características principales
del conjunto de datos.

\begin{table}[htbp]
\centering
\caption{Características generales del conjunto de datos}
\label{tab:dataset}

\begin{tabular}{ll}
\toprule
\textbf{Característica} & \textbf{Valor} \\
\midrule
Número de registros & XX \\
Número de variables & XX \\
Variable objetivo & \texttt{target} \\
Tipo de variable objetivo & Categórica / Numérica \\
Tipo de problema & Clasificación / Regresión \\
Valores faltantes & XX \% \\
Registros duplicados & XX \\
\bottomrule
\end{tabular}

\end{table}


% =================================================
% V. INSIGHTS PRELIMINARES
% =================================================

\section{Insights preliminares del análisis exploratorio}
\label{sec:eda}

El análisis exploratorio de los datos permite evaluar la calidad
del conjunto de datos y determinar si existen patrones suficientes
para abordar la pregunta de investigación planteada.

En el documento se presentarán únicamente los dos o tres hallazgos
más importantes obtenidos durante el EDA. El análisis completo,
incluyendo limpieza de datos, estadísticas descriptivas,
visualizaciones, valores nulos, duplicados y valores atípicos,
se encontrará en el notebook entregado junto con este documento.


\subsection{Distribución de la variable objetivo}

El primer aspecto analizado corresponde a la distribución de la
variable objetivo.

Aquí se deberá indicar si la variable se encuentra balanceada,
desbalanceada o si presenta alguna característica importante que
pueda afectar posteriormente el entrenamiento de los modelos.


% =================================================
% EJEMPLO DE FIGURA
% =================================================

% Cuando tengan una gráfica, pueden descomentar este bloque:
%
% \begin{figure}[htbp]
%     \centering
%     \includegraphics[width=\columnwidth]
%     {figuras/distribucion_target.png}
%     \caption{Distribución de la variable objetivo.}
%     \label{fig:target}
% \end{figure}


\subsection{Relaciones entre variables}

El análisis exploratorio también permitirá identificar posibles
relaciones entre las variables predictoras y la variable objetivo.

En esta subsección se describirán uno o dos patrones particularmente
relevantes para justificar la viabilidad del problema planteado.

Por ejemplo, puede analizarse si una determinada variable presenta
diferencias claras entre las clases del target o si existe una
correlación aparente entre determinadas variables numéricas.


\subsection{Calidad de los datos}

Finalmente, se analizarán aspectos relacionados con la calidad de
los datos, tales como:

\begin{itemize}
    \item Valores faltantes.
    \item Registros duplicados.
    \item Posibles valores atípicos.
    \item Variables con poca variabilidad.
    \item Variables que podrían requerir transformación.
\end{itemize}

Estos hallazgos serán importantes posteriormente para definir las
decisiones de preprocesamiento y construcción de los modelos de
Machine Learning.


% =================================================
% REFERENCIAS
% =================================================

\bibliographystyle{IEEEtran}
\bibliography{referencias}

\end{document}