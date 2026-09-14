

Hindawi
Journal of Electrical and Computer Engineering
Volume 2017, Article ID 5106045, 14 pages
https://doi.org/10.1155/2017/5106045


# Research Article


# Modeling PM2.5 Urban Pollution Using Machine Learning and Selected Meteorological Parameters


# Jan Kleine Deters,1 Rasa Zalakeviciute,2 Mario Gonzalez,2 and Yves Rybarczyk2,3


University of Twente, Enschede, Netherlands
2
Intelligent &Interactive Systems Lab (SI2 Lab),
3
DEE, Nova University of Lisbon and CTS, UNINOVA,


1


FICA, Universidad de Las Am ´ericas, Quito, Ecuador
Monte de Caparica, Portugal


Correspondence should be addressed to Yves Rybarczyk; y.rybarczyk@fct.unl.pt


Received 24 February 2017; Revised 23 April 2017; Accepted 11 May 2017; Published 18 June 2017


Academic Editor: Lei Zhang


Copyright © 2017 Jan Kleine Deters et al. This is an open access article distributed under the Creative Commons Attribution
License, which permits unrestricted use, distribution, and reproduction in any medium, provided the original work is properly
cited.


Outdoor air pollution costs millions of premature deaths annually, mostly due to anthropogenic fine particulate matter (or
PM2.5). Quito, the capital city of Ecuador, is no exception in exceeding the healthy levels of pollution. In addition to the impact
of urbanization, motorization, and rapid population growth, particulate pollution is modulated by meteorological factors and
geophysical characteristics, which complicate the implementation of the most advanced models of weather forecast. Thus, this paper
proposes amachinelearningapproachbasedonsixyearsofmeteorologicalandpollutiondataanalysestopredicttheconcentrations
of PM2.5 from wind (speed and direction) and precipitation levels. The results of the classification model show a high reliability in
the classification of low (<10 𝜇g/m3) versus high (>25𝜇g/m3)andlow(<10𝜇g/m3) versus moderate (10-25 𝜇g/m3) concentrations
of PM2.5. Aregression analysis suggests a better prediction of PM2.5 when the climatic conditions are getting more extreme (strong
winds or high levels of precipitation). The high correlation between estimated and real data for a time series analysis during the
wet season confirms this finding. The study demonstrates that the use of statistical models based on machine learning is relevant
to predict PM2.5 concentrations from meteorological data.


# 1. Introduction


The effects of rapid growth of the world's population are
reflected in the overuse and scarcity of natural resources,
deforestation, climate change, and especially environmental
pollution. Currently, more than half of the global population
lives in urban areas, and this number is expected to grow to
about 66% by 2050, mostly due to the urbanization trends
in developing countries [1]. According to the latest urban air
quality database, 98% of cities in low and middle income
countries with more than 100,000inhabitants do not meet the
World Health Organization (WHO)airqualityguidelines [2].
A recent study using a global atmospheric chemistry
model estimated that 3.3 million annual premature deaths
worldwide are linked to outdoor air pollution, which is ex-
pected to double by 2050, mostly due to anthropogenic fine
particulate matter (aerodynamic diameter < 2.5 𝜇m; PM2.5)


[3]. Over the last decade, evidence has been growing that


exposure to fine particulate air pollution has adverse effects
on cardiopulmonary health [4].
Arecent air quality study in Quito, the capital of Ecuador,
concurs that long-term levels of fine particulate pollution are
not only exceeding the WHO's recommended levels of
10 𝜇g/m3 but also are higher than the national standards of
15 𝜇g/m [5]. And even though the overall levels of fine par-
ticulate pollution have been decreasing due to active efforts
of the local and national governments in the last decade,
in some locations of the city the air quality has continued to
deteriorate. The latter reflects the global trends of urbaniza-
tion and motorization.
In addition to the impact of urbanization and rapid
population growth, the pollution levels in the cities are mod-
ulated by meteorological factors [6]. Most importantly, the
depth of mixing layer (the lower layer of troposphere mixing
surface emissions) often depends on solar radiation and thus
temperature in the area. The shallower the mixing depth is,




2


Journal of Electrical and Computer Engineering


the less diluted the daily emissions get. Therefore, tempera-
ture shows a reducing impact on fine particulate matter levels,
throughconvection[7].Inaddition,theformationandevolu-
tion of photochemical smog are dependent on solar radiation
and temperature; meanwhile, wind speed tends to
ventilate air pollutants and/or transport them to other areas,
even if the emission sources are not present in that region
[8, 9]. Thiscanresultinincreasedlevelsofairpollutiondown-
wind from the original source, which directly depends on
the wind direction [8]. Increased relative humidity has been
shown tomakeevenfineparticlesheavier,helpingthedry
deposition process of removal, while precipitation has adirect
effect of scavenging by wet deposition [7, 8]. In addition,
some studies differentiate between the seasons, as different
parameters have different effects during the year, due to the
combination of conditions [8, 9]. Thus, it is clearly impos-
sible to rely on a single parameter to fully understand the
urban pollution, especially if the study area is in a nonho-
mogeneous and complex terrain. This fact justifies the elab-
oration of models that take into account heterogeneous data
to predict air quality.
Currently, three major approaches are used to forecast
PM2.5 concentrations: statistical models, chemical transport,
and machine learning. Statistical models, which are mainly
based on single variable linear regression, have shown a nega-
tive correlation between different meteorological parameters
(wind, precipitation, and temperature) and PM concentra-
tions (PM10,PM2.5,andPM1.0) [7].Chemicaltransportand
Atmospheric Dispersion Modeling are numerical methods,
and the most advanced ones are WRF-Chem and CMAQ.
These models can be used to predict atmospheric pollution,
but their accuracy relies on an updated source list that is very
difficult to produce [10]. In addition, complex geophysical
characteristics of locations with complex terrain complicate
the implementation of these models of weather and pollution
forecast mostly due to the complexity of the air flows (wind
speed and direction) around the topographic features [11,


12]. Unlike a pure statistical method, a machine learning


approach can consider several parameters in a single model.
The most popular classifiers to forecast pollution from mete-
orological data are artificial Neural Networks [13-15]. Other
successful studies use hybrid or mixed models that combine
several artificial intelligence algorithms, such as fuzzy logic
and Neural Network [16], or Principal Component Analysis
and Support Vector Machine [17], or numerical methods and
machine learning [10].
Recent studies show that the machine learning approach
seems to overcome the other two methods for forecasting
pollution[9,10].Thisisthereasonwhyitisincreasinglyused
to predict air quality [13, 17-21]. However, the data mining
does not only differ from one study to another, in terms of
classification algorithms, but also regarding the used features.
Some of them consider a quite exhaustive list of meteoro-
logical factors [15, 16], whereas others proceed with a careful
selection [13, 14, 17, 22] or do not even use climatic parameters
at all [18]. Since machine learning is a very promising method
to forecast pollution, we propose applying this approach
to predict PM2.5 concentration in Quito. This prediction is
basedonaselectionofmeteorologicalfeaturesfortwomain


reasons: first because amodelusingonlymeteorological data,
which can be easily obtained in any urban area, is cheaper
than an air quality monitoring system and second because a
generalmodelthatmayworkforanycityisnotrealistic[10],
help which implies that a selection of meteorological parameters
mustbeperformedinordertofindthebestmodelforthecap-
ital city of Ecuador. Quito is located in the Andes cordillera in
thetropicalclimatezone,characterizedbytwoseasonswith
different accumulation of precipitation. However, the temper-
ature, the pressure, and even the amount of solar radiation do
notvarymuchduringtheyear.Moreover,thewinddirection
and speed highly depend on the topographic features of com-
plex terrain in which a city is positioned and usually present
one of the biggest challenges in forecasting weather and
air quality. Therefore, this research aims to study the con-
nectivity between three selected meteorological factors, wind
speed, wind direction, and precipitation, and PM2.5 pollution
in two districts located in northwestern Quito.
In this work, we first present a spatial visualization of
the distribution of fine particulate matter trends according to
wind (speed and direction) and precipitation parameters in
two locations in Quito. This part includes a description of the
preparation of the data for classification. Then, various
machine learning models are exploited to classify different
levels of PM2.5, namely, Boosted Trees and Linear Support
Vector Machines. Finally, aNeural Network regression and a
time series analysis are applied to provide insight about the
parametric boundaries, in which the classification models
perform adequately. In the final section, we draw up the main
conclusions and suggestions for future work.


# 2. Data Collection


2.1. Site Description. Unlike most of South America, the most


urbanized continent on the planet (81%), Ecuador, is one
of the few countries in the region with only 64% of total
population living inurbanareas[23]. However, the rate of
urbanization has increased over the past decade. Quito
sprawls north to south on a long plateau lying on the east side
of the Pichincha volcano (alt. 4,784 m.a.s.l., meters above sea
level) in the Andes cordillera at an altitude of 2,850 m.a.s.l.
(see Figure 1). According to the 2010 census, Quito's metro
area is currently 4,217.95 km2 with a population over 2,239,191
andisexpectedtoincreasetoalmost2.8millionby2020,
making the city the most populous city in the country,
overgrowing Guayaquil [24]. The city is contained within a
number of valleys at 2,300-2,450 m.a.s.l. and terraces varying
from 2,700 to 3,000 m.a.s.l. altitude. Due to Quito's location
on the Equator, the city receives direct sunlight almost all year
round, and, due to its altitude, Quito's climate is mild,
spring-like all year round. The region has two seasons, dry
(June-August, average precipitation 14 mm/month) and wet
(September-May, average precipitation 59 mm/month), with
most of the rainfall in the afternoons. Quito's temperature
is almost constant, around 14.5∘C, with the prevailing winds
fromtheeast.However,duetoacomplexterrain,thewindsin
the city are highly variable most of the year (dry season is
windier), challenging weather prediction in the region.




Journal of Electrical and Computer Engineering


N


Cotocollao


Belisario


3


(a) (b)


Figure 1: Topographic map (b) of Quito's urban area (green areas) and Google maps images (a) of the air quality measurement sites (red
dots) Cotocollao and Belisario.


For the purpose of this study, the two northwestern air
quality monitoring points are presented: Cotocollao and
Belisario (see red dots in Figure 1). These districts were
chosen to show the variation and complexity of the prediction
of fine particulate matter trends even within a relatively small
area of Quito with similar topographical characteristics (ap-
proximately the same altitude and directly east of the Pichin-
cha volcano).


# 2.2. Air Quality Measurements Monitoring Network and


Instrumentation. The municipal office of environmental
quality, Secretaria de Ambiente,hasbeencollectingairquality
and meteorological data since May 1, 2007, in several sites
around the city. The measurement sites run by the Secretaria
de Ambiente are located in representative areas throughout
the city, varying by altitudes depending on municipal dis-
tricts. We used the real meteorological and PM2.5 concen-
tration data from the two most northwestern automatic
data collection stations: Belisario (alt. 2,835 m.a.s.l., coord.
78∘29󸀠24󸀠󸀠W, 0∘10󸀠48󸀠󸀠S) and Cotocollao (alt. 2,739 m.a.s.l.,
coord. 78∘29󸀠50󸀠󸀠W, 0∘6󸀠28󸀠󸀠S) (see Figure 1). These two sites
are approximately 9km apart from each other. The Belisario
measurement site is less than 100 m west of a busy road
(Avenida America), 200 m northwest of a busy roundabout,
andlessthan1,000mtotheeastofamajorouterhighway
(Ave. Antonio Jose de Sucre), which runs along the west
side of the city, intended to reduce the traffic inside the city
(Figure 1). TheCotocollao monitoring site is located in a resi-
dential area, with only a few busier streets, and the same outer
highway(Ave. Antonio Jose deSucre)250mtothenorth.
Both monitoring sites are inside of the "Pico y Placa" zone,
implemented in 2010, which, based on the last number of car


license plates, limits rush hour traffic reducing the number of
personal vehicles by approximately 20% during the weekdays.
The monitoring stations are positioned on the roofs of
relatively tall buildings. Fine particulate matter (PM2.5)mea-
surements are conducted using instrumentation validated by
the Environmental Protection Agency (EPA) of the United
States. For PM2.5 Thermo Scientific FH62C14-DHS Contin-
uous, 5014i (EPA Number EQPM-0609-183), was used. The
detection limit for this instrument is 5 𝜇g/m3 for one-hour
averaging. The aerosol data is collected at 10 s intervals, and
from this then 10 min, 1-hour, and 24-hour averages are
calculated. The latter averaging data is presented in this work.
Wind velocity is measured using MetOne/010C and wind
direction using MetOne/020C instrumentation. The wind
speed sensor and wind direction starting threshold is
0.22 m/s, and the accuracies are 0.07 m/s and 3∘,respectively.
The precipitation is measured using MetOne/382 and Thies
Clima/5.4032.007 equipment. All meteorological parameters
have been validated using Vaisala/MAWS100 weather station.


# 3. Data Preparation


In this section the method for the preparation of the data
is presented, in order to proceed with the classification. It
includes refining steps to discard useless data, transforma-
tions to visually examine and understand the data, and
creation of an averaged intensity map of the PM2.5 concentra-
tions with respect to the selected meteorological parameters
(wind and precipitation).


3.1. Data Refinement. For this study we analyzed the data of


sixyears,startingJune2007andendingJuly2013.Thetwo




<table>
 <tr>
  <th>4</th>
  <th>Journal of Electrical and Computer Engineering</th>
 </tr>
 <tr>
  <td></td>
  <td>&gt;25 &gt;25</td>
 </tr>
 <tr>
  <td>35</td>
  <td>35</td>
 </tr>
 <tr>
  <td></td>
  <td>20 20</td>
 </tr>
 <tr>
  <td>20</td>
  <td>20</td>
 </tr>
 <tr>
  <td></td>
  <td>15 15</td>
 </tr>
 <tr>
  <td>10</td>
  <td>10</td>
 </tr>
</table>


10


N


1. 


E


0
5


5


5


5


5


W


1. 


5


0


0


1. (b)


N


E


0
5


W


S


5


Figure 2: Data distribution for (a) Cotocollao and (b) Belisario, in terms of wind direction, wind speed, precipitation, and PM2.5
concentrations (color scale). The inner circle represents wind speeds up to 2 m/s and the outer circle represents wind speeds up to 4 m/s.


datasets (one for each monitoring point) are composed out of
2,223 instances. Each data point consists of 4 parameters
indicating daily values of precipitation accumulation (mm),
wind direction (0-360∘), wind speed (m/s), and observed fine
particle concentrations (𝜇g/m3).
The datasets are cleaned by discarding data points that
include any missing values. These data points represent 2.8%
and 2.4% of the total data for Belisario and Cotocollao,
respectively. It has been demonstrated that missing data of
these magnitudes do not influence the classification perfor-
mance [25]. In addition, considering the very low number
of missing values, it is preferable to remove them instead
of performing an interpolation, taking into account the
following: (i) we proceed with an analysis on discrete vari-
ables (day-by-day) and not a time series forecasting and (ii)
the PM2.5 concentrations are very inconstant from one day
to another. Weekend days are also removed from the dataset
because the distribution of PM2.5 concentrations during the
weekdays and weekends is very different for Quito. This
could introduce an additional level of complexity in data
classification as during the weekdays there are clear rush hour
peaks (morning and evening), while on Saturdays PM2.5 lev-
els increase between late morning and late afternoon hours.
In addition, Sundays can be identified by a drop of PM2.5
concentration. These patterns are dictated by human activity
changes during the week, therefore, clearly showing PM2.5
dependability on traffic. After cleaning, the final datasets are
composed of 1,527 instances for Belisario and 1,536 instances
for Cotocollao.


3.2. Data Transformation. To represent the data according to
a wind rose plot, the linear scale of wind direction (0-360∘)


is transformed from polar to Cartesian coordinates where
angles increase clockwise and both 0∘ and 360∘ are north


(N) (see Figure 2). Thismathematicaltransformation (see (1))


permits amore accurate feature representation of the data for
wind direction around the north axis. Otherwise, wind
direction angles slightly higher than 0∘
and slightly lower than
360∘ would be considered as two opposing directions. This is
useful for classification models that are implemented in the
next stage. This relates to machine learning models that
improve performance if there are continuous relationships
between parameters (optimization: smoother clustering task)


[26]. This transformation ensures both valid and more infor-


mative representation of the original data. In addition, this
representation can be completed by the precipitation levels,
which are plotted on the 𝑧-axis(Figure2).Thecolorrangeis
mapped from concentrations 0 𝜇g/m3 to >25𝜇g/m3. The
threshold of 25 𝜇g/m3 indicates the values from which the 24-
hour concentrations of PM2.5 are harmful according to inter-
national health standards.


𝑥=sin(Wind Direction ⋅2𝜋)⋅Wind Speed,
360∘
𝑦=cos(Wind Direction ⋅2𝜋)⋅Wind Speed.
360∘


(1)


Avisual inspection of the transformed data shows that the
wind directions corresponding to precipitation are north
(N) for Cotocollao (Figure 2(a)) and east (E) for Belisario
(Figure 2(b)). The stronger winds tend to take place between
south (S) and southeast (SE) for Cotocollao and between
southwest (SW) and SE in Belisario. As expected, in both
cases these stronger winds seem to account for relatively low
levels of PM2.5.


3.3. Trend Analyses. In order to obtain general trends in the


distribution of the PM2.5 concentrations as a function of




Journal of Electrical and Computer Engineering


windspeedandwinddirection,thedataareusedtogenerate
convolutional based spatial representations. Convolution-
based models for spatial data have increased in popularity as
a result of their flexibility in modeling spatial dependence
and their ability to accommodate large datasets [27]. This
generated Convolutional Generalization Model (CGM) [28]
is an averaged value of the PM2.5 pollutionlevel(PL),inwhich
the regional quantity of influence per data point is modeled as
a 2D Gaussian matrix (see (2)). A Gaussian convolution is
applied (i) to spatially interpolate data, in order to get a
2D representation from the points' coordinates calculated in


(1) and (ii) to smooth the PL concentration values of this


representation. A Gaussian kernel is used because it inhibits
the quality of monotonic smoothing, and as there is no prior
knowledge about the distribution, a kernel density function
with high entropy minimizes the information transfer of the
convolutionsteptotheprocesseddata[29].This2DGaussian
matrix is multiplied by the PL of the given data point and
added to the CGM at the coordinates corresponding to the
wind speed and direction of this point. Then, the quantity of
influence is added to the point. The final step is to divide the
total amount of each cell by the quantity of influence, which
results inageneralizedaveragevalue.


1 [ [ [1]
CGM(rows,colums) = PL36 [ [ [ [4 6]
[
1]


[4][14641]. (2)


The general tendencies are as follows: (i) strong winds
result in low PM2.5 concentrations and (ii) the strongest
winds generally come from the similar direction (SE for
Cotocollao and S for Belisario). The results of CGMs for both
sites are shown in Figure 3 as an overlay on top of the geo-
graphic location of their respective monitoring stations. Main
highways are indicated in green. The highest concentrations
of PM2.5 (from yellow to red) tend tobebroughtbythe
winds coming from these main highways. It is to note that
higher wind speeds for Cotocollao tend to be on the axis of
Quito'sformerairport(grey-greenarea,centerofthemap,see
Figure 3), currently transformed into a city park. This traffic
and structure free corridor seems to accelerate wind speeds,
which may explain the reduction of PM2.5 concentrations due
tobetterventilationofthispartofthecity.
During the study, average PM2.5 concentrations in Coto-
collao and Belisario are 15.6 𝜇g/m3 and 17.9 𝜇g/m3, respec-
tively, both exceeding the national standards. During the
studied six years, the area of Belisario was more polluted with
more variation in PM2.5 concentrations (higher deviation,
see Figure 4) and more turbulent (Figure 3) than Cotocollao.
These factors could be the result of Belisario being more
urbanized.


# 4. Classification Models


Machine learning models are used to separate the data in
different classes of PM2.5 concentrations. Supervised learning


1km


N


>25


<table>
 <tr>
  <th></th>
  <th></th>
  <th></th>
 </tr>
</table>


0


5


Figure 3: CGM visualization, positioned on top of the geographic
location of the respective monitoring stations (northwestern part
of Quito). The northern CGM visualization is Cotocollao and the
southern one is Belisario. Main highways are represented in green.


0.1


0.09


0.08


0.07


0.06


0.05


0.04


0.03


0.02


0.01


0


5


10


15


20


Real value (g/3)


25


30


Cotocollao
Belisario


Figure 4: Distribution of PM2.5 concentrations (June 2007 to July
2013) for Cotocollao and Belisario. Dashed black line represents the
national standards and the class seperation boundary (15 𝜇g/m3).


techniques are applied to create models on this classification
task.HereweintroduceBoostedTrees(BTs) andLinearSup-
port Vector Machines (L-SVM). ABTcombines weak learn-
ers (simple rules) to create a classification algorithm, where
each misclassified data point per learner gains weight. A
following learner optimizes the classification of the high-
est weighted region. Boosted Trees are known for their




6


Table 1: Binary classification with class separation at 15 𝜇g/m3.
Location
Model


<table>
 <tr>
  <th></th>
  <td></td>
  <td></td>
 </tr>
 <tr>
  <th></th>
  <td>Belisario</td>
  <td>Cotocollao</td>
 </tr>
 <tr>
  <th>BT</th>
  <td>83.2%</td>
  <td>67.6%</td>
 </tr>
 <tr>
  <th>L-SVM</th>
  <td>79.8%</td>
  <td>66.3%</td>
 </tr>
</table>


insensibility to overfitting and for the fact that nonlinear
relationships between the parameters do not influence the
performance. A L-SVM separates classes with optimal dis-
tance. Convex optimization leads the algorithm to not focus
on local minima. As these two models are well established
andinhibitdifferentqualities,theyareusedinthissection.All
computations and visualizations are executed in MathWorks
Matlab 2015. Toolboxes for the classifications, the statistics,
and machine learning processes are used in all the stages. Fur-
thermore, Matlab's integrated tools for distribution fitting and
curve fitting are applied for the different analyses. The initial
parameters provided by the Matlab toolbox software are used
in this work. ADAboostlearningmethodwithatotalamount
of 30 learners and a maximum number of splits being 20 at
a learning rate of 0.1 are the default parameters for the BT.
The SVM is initialized with a linear kernel of scale 1.0, a box
constrained level of 1.0, and an equal learning rate of 0.1.
Fluctuations in yearly PM2.5 concentrations are not taken
into account in this classification process as a previous
analysis showed a small variation in fine particulate matter
pollution levels during the studied period [5]. A binary clas-
sification is performed to set a baseline comparison between
the different sites. Then, a three-class classification is carried
out to assess the separability between three ranges of concen-
trations of PM2.5 (based on WHO guidelines) and provide
insight into general classification rules.


4.1. Binary Classification. In this first classification two class-


es are used, which represent values above and below 15 𝜇g/m3.
ThelattervalueisselectedasitistheNationalAirQuality
Standard of Ecuador for annual PM2.5 concentrations (equiv-
alent toWHO'sInterimTarget-3)[30].Duetothenormal
distribution of the datasets, as shown in Figure 4, a higher
accuracy for Belisario than Cotocollao is expected, partially
because of a priori imbalanced class distribution. Aprevious
study using the same classification shows an accuracy of
only 65% for Cotocollao by applying the trees.J48 algorithm,
which is a decision tree implementation integrated in the
WEKA machine learning workbench [5].
Classification with both BT and L-SVM shows similar
results. Table 1 presents the results of this first classification.
The implementation of the classification for Belisario outper-
forms that of Cotocollao. It also suggests that the extreme lev-
els(lowandhigh)ofPM2.5 couldbemorestraightforwardto
classify with the current parameters, implying a higher class
separability for the Belisario dataset (wider distribution).
Tables 2 and 3 show that the concentrations above 15 𝜇g/m3
for both sites are better classified than those below the
15 𝜇g/m3 boundary. This is less surprising for Belisario due to


Journal of Electrical and Computer Engineering


Table 2: Confusion matrix of binary classification for Cotocollao
using a BT. Rows represent the true class and columns represent the
predicted class.


<15


51.1% 48.9%


20.3%


>15 TPR/FNR


1. %


48.9%


1. %


79.7% 20.3%


Class


<15
>15


Table 3: Confusion matrix of Binary classification for Belisario
using a BT. Rows represent the true class and columns represent the
predicted class.


<table>
 <tr>
  <th>Class</th>
  <th>&lt;15</th>
  <th>&gt;15 TPR/FNR</th>
 </tr>
 <tr>
  <td></td>
  <td></td>
  <td></td>
 </tr>
 <tr>
  <td></td>
  <td></td>
  <td></td>
 </tr>
 <tr>
  <td></td>
  <td></td>
  <td></td>
 </tr>
 <tr>
  <td></td>
  <td></td>
  <td></td>
 </tr>
 <tr>
  <td></td>
  <td></td>
  <td></td>
 </tr>
 <tr>
  <td></td>
  <td></td>
  <td></td>
 </tr>
</table>


the earlier mentioned class imbalance. For Cotocollao, how-
ever, the poor performance for this class can indicate that this
class is less distinctive; thus the model optimizes the class
above 15 𝜇g/m3. Note that it is crucial to be able to classify
nonattainment (PM2.5 > 15 𝜇g/m3) instances, as wrongly
identified nonviolating national standards (PM2.5 < 15 𝜇g/
m3) levels would be a less costly error.
In Figure 5(a) Receiver Operating Characteristic (ROC)
curves comparison is shown for the binary classifiers pre-
sented in Table 1, namely, the BT and L-SVM classifiers.
Figure 5(a) depicts the ROC curves for Cotocollao dataset
and Figure 5(b) the ROC curves for Belisario dataset. Once
the classifiers models are built for every dataset, a validation
set is presented to the model, in order to predict the class
label. It is also of interest to have the classification scores of the
model which indicate the likelihood that the predicted label
comes from a particular class. The ROC curves are con-
structed with this scored classification and the true labels in
the validation dataset (Figure 5).
ROCcurvesareusefultoevaluate binary classifiers and to
compare their performances in a two-dimensional graph that
plots the specificity versus sensitivity. The specificity mea-
sures the true negative rate, that is, the proportion of negatives
that have been correctly classified: true negatives/negatives =
true negatives/(true negatives + false positives). Likewise, the
sensitivity measures the true positive rate, that is, the propor-
tion of positives correctly identified: true positives/positives


= true positives/(true positives + false negatives). The area


undertheROCcurve(AUC)canbeusedasameasureof
the expected performance of the classifier, and the AUC of a
classifier is equal to the probability that the classifier will
rank a randomly chosen positive instance higher than a
randomly chosen negative instance [31]. Figure 5(b) shows
the performance of the BT and L-SVM classifiers for the
Belisario dataset. The BT outperforms the L-SVM classifier
in all regions of the ROC space, with [AUC(BT) = 0.72] >
[AUC(L-SVM) = 0.66], which means a better performance




Journal of Electrical and Computer Engineering


100


80


60


40


20


<table>
 <tr>
  <th>100</th>
 </tr>
 <tr>
  <td>80</td>
 </tr>
 <tr>
  <td>60</td>
 </tr>
 <tr>
  <td>40</td>
 </tr>
 <tr>
  <td>20</td>
 </tr>
 <tr>
  <td>0</td>
 </tr>
</table>


7


0


100 80 60 40 20 0
Specificity (%)


100 80 60 40 20 0
Specificity (%)


BT, AU = 59.1%


L-SVM, AU = 56.2%


BT, AU = 71.8%
L-SVM, AU = 65.9%


1. (b)


Figure 5: ROC curves for Cotocollao (a) and Belisario (b).


for the BT classifier. The BT classifier has a fair performance
separating the two classes in the Belisario dataset.
InFigure5(a)theROCcurvesandAUCarepresentedfor
the Cotocollao dataset. Again, BT performs better than the
L-SVM classifier with [AUC(BT)
0.59] > [AUC(L-SVM)
a poor performance separating the two classes, with a perfor-
mancejust slightlybetterwhen comparedtoarandomclas-
sifier with AUC = 0.5. Theclassification result is clearly better
for Belisario than for Cotocollao. Thus, a three-class classi-
fication should identify if for both sites; the extreme concen-
trationscouldbebetterclassifiedthanthemoderateonesand
clarify the low performance for Cotocollao.


<table>
 <tr>
  <th>Class</th>
  <th>&lt;10</th>
  <th>10-25 &gt;25 TPR/FNR</th>
 </tr>
 <tr>
  <td>= =</td>
  <td></td>
  <td></td>
 </tr>
 <tr>
  <td>0.56]. This time the classifiers for the Cotocollao dataset have &lt;10</td>
  <td>76.3%</td>
  <td>16.3% 7.4%</td>
 </tr>
 <tr>
  <td></td>
  <td></td>
  <td></td>
 </tr>
</table>


4.2. Three-Class Classification. To further analyze the differ-


ences of multiple categories of concentration levels, a three-
class classification is performed using WHO's guidelines for
pollution concentrations as class boundaries. According to
these guidelines, health risks are considered low if PM2.5 <
10 𝜇g/m3 (long term, annual WHO's recommended level),
moderate if 10 𝜇g/m3 > PM2.5 < 25 𝜇g/m3, and high if
PM2.5 > 25 𝜇g/m (short term, 24-hour WHO's recom-
mended level). The objective is to identify if these main
pollution thresholds are indeed well separable and thus the
weather parameters can account for PM2.5 pollution in these
three ranges of air quality.
In both studied districts the classes < 10 𝜇g/m3 and >25
𝜇g/m3 are relatively small with approximately 10% of the
data compared to the class 10-25 𝜇g/m3.Duetothisfact,an
alternative BT algorithm is used to take into account these
imbalanced classes. This RusBoosted Tree (RBT) approach


Table 4: Confusion matrix of three-class classification for Cotocol-
laousingaRBT.Rowsrepresentthetrueclassandcolumnsrepresent
the predicted class.


23.7%
28.8%


28.3% 28.8% 42.9% 71.2%
73.4%
6.3% 20.3% 73.4% 26.6%


10-25


>25


endeavors to find an even distribution of performance for
all classes instead of finding a global optimum [32]. This
leads to a better representation of the separability. The true
positive versus false negative rate (TPR/FNR) is shown for
each class in the confusion matrices of Cotocollao (Table 4)
and Belisario (Table 5).
Tables 4 and 5 show that the correctness in classifying
concentrations < 10 𝜇g/m3 seems to perform adequately.
Also, the correct classification for concentrations > 25 𝜇g/
m3 in Cotocollao is fair. However, the false positive rate of
this classification is extremely high, because 42.9% of the
10-25 𝜇g/m3 class gets classified as class > 25 𝜇g/m3. For
Belisario, the separation of classes 10-25 𝜇g/m3 and >25𝜇g/
m3 is deficient. In both cases, only the extreme low values can
be classified well. Thus, the hypothesis of the extreme concen-
trations in PM2.5 being more straightforward to classify (see
Section 4.1) is only partially verified.
Analyzing the wrongly classified samples of class 10-25
𝜇g/m3 shows that, for samples classified as <10 𝜇g/m3, the




8


0.14


0.08


<table>
 <tr>
  <th>0.2</th>
 </tr>
 <tr>
  <td>0.11</td>
 </tr>
 <tr>
  <td>0.02</td>
 </tr>
</table>


Journal of Electrical and Computer Engineering


0.02


12


16 20
Real value (g/3)


24


12


16 20
Real value (g/3)


24


10-25g/3 classified as <10g/3
10-25g/3 classified as >25g/3


10-25g/3 classified as <10g/3
10-25g/3 classified as >25g/3


(a) (b)


Figure 6: Wrongly classified samples of class 10-25 𝜇g/m3 with their real value distributions for Cotocollao (a) and Belisario (b).


Table 5: Confusion matrix of three-class classification for Belisario
using a RBT. Rows represent the true class and columns represent
the predicted class.


<table>
 <tr>
  <th>Class</th>
  <th>&lt;10</th>
  <th>10-25</th>
  <th>25 TPR/FNR</th>
 </tr>
 <tr>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
 </tr>
 <tr>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
 </tr>
 <tr>
  <td></td>
  <td></td>
  <td></td>
  <td>15.2%</td>
 </tr>
 <tr>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
 </tr>
 <tr>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
 </tr>
 <tr>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
 </tr>
 <tr>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
 </tr>
 <tr>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
 </tr>
 <tr>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
 </tr>
</table>


real values tend to be relatively close to 10 𝜇g/m3. This
evidence is even stronger for Belisario (Figure 6(b)), than for


Cotocollao (Figure 6(a)). This indicates a changeover in val-
ues around the decision boundary. The same does not apply
to the wrongly classified samples that are grouped as
>25𝜇g/m3. As shown in Figure 6 these values are mostly nor-
mally distributed around the mean of class 10-25 𝜇g/m3.Even
though for Belisario the mean is shifted, it is not evident
that wrongly classified samples of class 10-25 𝜇g/m3 into class
25 𝜇g/m3 tend to be closer to values of 25 𝜇g/m3, asthis
shift is mainly caused by the fact that the mean value of the
Belisario initial data is higher (see Figure 4). We can conclude
that the low performance for Cotocollao in the previous
section (Section 4.1) is mainly caused by the fact that the clas-
sifier tries to separate values in the range of 10-25 𝜇g/m3 and
>25𝜇g/m3, which are poorly separable according to the
three-class classification.
Theseresultsshowthatvaluesof10-25𝜇g/m3 and >25𝜇g/
m3 are not well separable and thus not largely influenced by
the used meteorological parameters. On the contrary, lower


values seem to be largely predictable by wind and precipita-
tion conditions. This statement gains confidence by looking
at the wrongly classified data points discussed previously (see
Figure 6).


4.3. Classification Rules. Binary classification between all dif-


ferent classes with the use of RBTs provides general rules
for classifying the different levels of PM2.5 in terms of the
parameter space. Here, the well performing rules in classi-
fying PM2.5 concentrations < 10 𝜇g/m3 are discussed. The
rulesandtheirperformancecanbeseeninTable6.Thistable
shows that rules separating classes < 10 𝜇g/m3 versus 10-25
𝜇g/m3 and <10 𝜇g/m3 versus >25𝜇g/m3 have a high percent-
age of accuracy. On the contrary, the separation between
10-25 𝜇g/m3 and >25𝜇g/m3 is less accurate.
Figure 7 provides a visualization of the data according to
the class separation in Table 6 for the example of Cotocollao.
The RBT classification of the data as seen in Figures 7(a) and
7(b) creates two clusters for class < 10 𝜇g/m3. Inthecaseof
Belisario, the RBT classifications result in identifying only
one cluster for class < 10 𝜇g/m3.
It is to note that, for Cotocollao, the performance increas-
es drastically comparing the binary classifications of <10 𝜇g/3
m3 versus 10-25 𝜇g/m3 and <10 𝜇g/m3 versus >25𝜇g/m
(from 73.2% up to 88.9%, see Table 6). In contrast, the per-
formance for Belisario for these two classifications does not
differ (from 86.7% to 88.8%). This indicates that the data for
Cotocollao are less separable at the 10-25 𝜇g/m3 class than for
Belisario.
To sum up the outcomes of the classification models, the
binary classification utilizing the National and International
Air Quality Standards as class labels (PM2.5 < 15 𝜇g/m3,
PM2.5 > 15 𝜇g/m3) showedahighdifferenceinperformance




Journal of Electrical and Computer Engineering


9


Table 6: Classification rules and pairwise comparisons between the different classes and their respective performance.


Location


Classification


Cotocollao


Belisario


Classification rules


Wind speed > 2.5 m/s
Wind direction = S-SE


Wind speed > 2.2 m/s
Wind direction = SE-SW


<10 𝜇g/m3 versus
10-25 𝜇g/m3


Wind direction = NW-NE
Precipitation > 15 mm


Classification performance


1. % (Figure 7(a)) 86.7%


Classification rules


Wind speed >2m/s
Wind direction = S-SE


Wind speed >2m/s
Wind direction = SE-SW


<10 𝜇g/m3 versus
>25𝜇g/m3


Wind direction = NW-NE
Precipitation >1mm


Classification performance


1. % (Figure 7(b)) 88.8%


10-25 𝜇g/m3 versus
>25𝜇g/m


60.0% 64.1%


35


35


20


20


10


N


<table>
 <tr>
  <th>0</th>
  <td>0</td>
  <td></td>
 </tr>
 <tr>
  <th>5</th>
  <td>5</td>
  <td></td>
 </tr>
 <tr>
  <th></th>
  <td>5</td>
  <td>5</td>
 </tr>
 <tr>
  <th>W</th>
  <td></td>
  <td></td>
 </tr>
</table>


5


E


S


10


N


5


E


<10g/3
10-25g/3


<10g/3
>25g/3


(a) (b)


Figure 7: Data split for three different classes (see Table 6): (a) <10 𝜇g/m3 versus 10-25 𝜇g/m3 and (b) <10 𝜇g/m3 versus >25𝜇g/m3.Both(a)
and (b) are results for Cotocollao mapped in terms of wind direction, wind speed, and precipitation. The inner circle represents wind speeds


upto2m/sandtheoutercirclerepresentswindspeedsupto4m/s.


between the two sites. In order to explain this difference and
the misclassifications, the analysis was refined to a three-class
classification based on WHO's guidelines regarding the con-
sequences of PM2.5 concentrations on health risks as low
(PM2.5 < 10 𝜇g/m3), moderate (PM2.5 =10-25𝜇g/m3), and
high (PM2.5 > 25 𝜇g/m3). This classification showed high


performance in categorizing low concentrations in contrast to
high concentrations. Next, we proposearegressionanalysisto
pinpoint the upper boundary of PM2.5 values, for which the
weather parameters are still able to explain variation in
pollution levels that are not described by the classification
analysis.




10


5


<table>
 <tr>
  <th></th>
  <th></th>
  <th></th>
  <th></th>
  <th></th>
  <th></th>
  <th></th>
  <th></th>
  <th></th>
  <th></th>
  <th></th>
 </tr>
</table>


JournalofElectricalandComputerEngineering


0


0


Precipitation (mm)


25


0


Wind speed (m/s)


5


Cotocollao
Belisario


Cotocollao
Belisario


(a) (b)


Figure 8: Decrease in average prediction error with increasing parameter values (precipitation and wind speed) for Cotocollao (orange) and
Belisario (blue).


# 5. Regression Analyses


In this section an additional machine learning analysis, based
on BT, L-SVM, and Neural Networks (NN), is used to per-
form a regression for both sites. Default parameters provided
by the Matlab toolbox software are used to set up the models.
NN are appropriate models for highly nonlinear model-
ing and when no prior knowledge about the relationship
between the parameters is assumed. The NN consist of 10
nodes in 1 hidden layer, trained with a Levenberg-Marquardt
procedure, in combination with a random data division.
Identifying the correlation between the real and predicted
values gives us the topological coherence between the input
and output parameter values. In addition, the error related to
the parameter values provides insight regarding the predic-
tion confidence for determined weather conditions. Also, the
analysis of the data trend over time will inform on the appli-
cability of a time series forecasting. Finally, the CGM is used
to remark on the possibility of optimizing the regression.


5.1. Regression Models. A regression is performed with three


different classifiers. Bin sizes of 0.5 𝜇g/m3 (0-35 𝜇g/m3 range)
areusedforthemodelsthatoutputdiscreteclassvalues(BT


and SVM). This relatively small bin size permits these
models to perform regression as their output values closely
approach continuous values. Theadditional parameters of the
models are set up as explained in the binary and three-class
classification (Sections 4.1 and 4.2). The models are trained
with 10-fold cross-validation. The test set is 20% of the


original data. Unlike the NN continuous output values, the
discrete output values of the other models can have an effect
on the classification error. However, as the bin size is relatively
small, we expect the errors related to these types of output to
be marginal.


𝑛 ∑ (𝑦𝑖 - 𝑦̂𝑖)2 . (3)
𝑖=1


MSE = 1
𝑛 ⋅


The mean squared error (MSE) is used to measure the
classification performance (see (3)). The MSE is the averaged
squared error per prediction. The mean absolute percentage
error (MAPE) is used to express the average prediction error
in terms of percentage of a data point's real value (see (4)).
TheMAPEfunctionprovides amore intuitive understanding
of the performance.


MAPE = ∑𝑛𝑖=1 󵄨 󵄨 󵄨 󵄨(𝑦𝑖 - 𝑦̂𝑖)/𝑦󵄨
𝑛 󵄨 .


(4)


An analysis of the confidence levels in relation to the pre-
cipitation and wind speed parameters is shown in Figure 8.
The prediction confidence rises when the parameter values
increase. A level of confidence is explained as the average
prediction error (absolute difference between the real and the
predicted values, root of MSE) at a certain interval with
respect to an input parameter. In Figure 8, fitted lines repre-
sent the predicted data in terms of their absolute error with
respect to precipitation and wind speed for both sites. The
decrease in errors can be seen with respect to increasing




Journal of Electrical and Computer Engineering


11


6.0


40 5.5
5.0
30
4.5


<table>
 <tr>
  <th></th>
  <th></th>
  <th></th>
  <th></th>
  <th></th>
  <th></th>
  <th></th>
 </tr>
 <tr>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
 </tr>
 <tr>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
 </tr>
 <tr>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
 </tr>
 <tr>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
 </tr>
</table>


20 4.0


3.5


10


3.0


0 2.5


160 180 200 220 240 260 280
Day counter


Predicted P2.5 concentration
Real P2.5 concentration
Precipitation
Wind speed
Wave 1


Figure 9: Neural Network's regressive prediction of Cotocollao PM2.5 concentration (light grey) compared to the real data (dark grey) during
the wet season plotted against daily rain accumulation and wind speed thresholds, >1mmand>2.5m/s,respectively (see Table 6, thresholds
obtained from 3-class classification). The dashed black line represents the national standards for PM2.5 annual concentrations.


values of these specified input parameters. It suggests that the
prediction of PM2.5 concentration is morereliable for extreme
than moderate climatic conditions.
Figure 9 shows an example of the comparison of the
predictive models of PM2.5 concentration and the real PM2.5
concentration for Cotocollao during six months of a wet
season (first half of 2008). The graph shows the 5-point box-
smoothed data to demonstrate the good prediction of the
tendency of the PM2.5 concentrations. Besides a certain gap,
the estimated values seem to fairly correlate with the real data.
The correlation analysis shows a significant positive corre-
lation between the real concentrations and the predicted
concentrations, 𝑟(130) = 0.5, 𝑝 < 0.000. Also, themodel
performance is relatively good throughout the study period.
The correlation analysis for all of the data shows a significant
positive correlation between the real and predicted PM2.5
concentrations, 𝑟(1534) = 0.34, 𝑝 < 0.000.
This visualization shows that the error of predicted
concentration seems to increase when PM2.5 concentration
increases. The reduction in both real and estimated PM2.5
concentrations coincides with rain events and wind speeds
above the thresholds defined in Table 6 (>1mmand>2.5m/s,
resp.).
The results of the MSE for the regression show that in
both city sites a NN performs the best (see Table 7). The
correlation analysis shows that there is a logarithmic relation-
ship between the real particle concentration values and the
prediction (Figure 10). It means that there is an overpredic-
tion for low values and an underprediction for high values
and an overall decrease in correlation as values get higher. The
correlation seems the best for values around 17 𝜇g/m3 for Cot-
ocollao and 19 𝜇g/m3 for Belisario.
To sum up, the present input parameters do not well
describeanincreaseinPM2.5 concentrations if these levels are
transcending values over 20 𝜇g/m3,aserrorsincreaseatthis
point and prediction values stagnate. Thus, additional param-
eters must be considered for the prediction of PM2.5 levels


Table 7: MSE and MAPE of the NN, L-SVM, and BT on regression.


<table>
 <tr>
  <th></th>
  <td></td>
  <td></td>
 </tr>
 <tr>
  <th></th>
  <td>Belisario</td>
  <td>Cotocollao</td>
 </tr>
 <tr>
  <th>NN</th>
  <td>22.1 (26%)</td>
  <td>40.7 (40%)</td>
 </tr>
 <tr>
  <th>L-SVM</th>
  <td>26.8 (28%)</td>
  <td>41.8 (41%)</td>
 </tr>
 <tr>
  <th>BT</th>
  <td>28.5 (30%)</td>
  <td>44.4 (42%)</td>
 </tr>
 <tr>
  <th>Table 8:</th>
  <td>MSE and MAPE of CGM and</td>
  <td>NN regression.</td>
 </tr>
 <tr>
  <th></th>
  <td></td>
  <td></td>
 </tr>
 <tr>
  <th></th>
  <td>Belisario</td>
  <td>Cotocollao</td>
 </tr>
 <tr>
  <th>CGM</th>
  <td>15.6 (22%)</td>
  <td>15.0 (25%)</td>
 </tr>
 <tr>
  <th>NN</th>
  <td>22.1 (26%)</td>
  <td>40.7 (40%)</td>
 </tr>
</table>


beyond this concentration threshold, since meteorological
factors alone are not able to account for the whole particulate
matter concentrations. For instance, considering human
activity (e.g., car traffic), which is the main source of pollu-
tion, should contribute to the reduction of the overprediction
and underprediction observed in our model.


5.2. Optimization. TheCGM,asappliedinSection 3.3, could


be used in classification tasks. In this section a 10-fold
cross-validation on regression with this model is applied to
compare it with the best performing model (NN).
TheresultsshowasubstantialreductioninMSEwith
the CGM regression compared to the NN regression for the
two city sites (see Table 8). It is to note that this diminution is
particularly high in the case of Cotocollao. It seems that the
model is able to better handle the dense (see Figure 4) and
noisy (as stated in Section 4.3) data of Cotocollao than the
NN. The similar performance in both sites means that this
model has the potential to be applied in various situa-
tions with similar expected error rates. Further development




12 JournalofElectricalandComputerEngineering


<table>
 <tr>
  <th></th>
  <th></th>
  <th></th>
  <th></th>
  <th></th>
  <th></th>
  <th></th>
 </tr>
 <tr>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
 </tr>
 <tr>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
 </tr>
 <tr>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
 </tr>
 <tr>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
 </tr>
 <tr>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
  <td></td>
 </tr>
</table>


0


15


Real value (g/3)


30


Cotocollao
Belisario


Figure 10: Fitted lines representing the correlation between pre-
dicted values and real values through aNNalgorithmforCotocollao
(orange) and Belisario (blue).


should aid in qualifying the true robustness of this approach
byexploitingthe possibility ofmodeling with other spatial
dependencies, such as density of measurements and day-
by-day shifts, which represent the degree of freedom of
parameters related to readings of the previous day(s). The
latter dependency could be combined with linear quadratic
estimation (LQE) techniques such as Kalman filters to im-
prove the precision.


# 6. Conclusions and Perspectives


This study proposes amachine learning approach to predict
PM2.5 concentrations from meteorological data in a high-
elevation mid-sized city (Quito, Ecuador). Standard levels of
fine particulate matter are classified by using different
machine learning models. This classification is performed on
six years' records of daily meteorological values of wind speed
(m/s), wind direction (0-360∘), and precipitation accumu-
lation (mm) for two air quality monitoring sites located in
Quito (Cotocollao and Belisario). Although these sites are
both in Quito's urbanized area, they exhibit differences in
spread and dominance regarding wind features (speed and
direction) that account for high PM2.5 concentrations and
distribution of pollution levels over the years. This could be
causedbythefactthatBelisarioismoreurbanizedthanCoto-
collao and more importantly due to the extremely complex
terrain of the city.
For these two different districts the results show a high
reliability in the classification of low (<10 𝜇g/m3) versus
high (>25𝜇g/m3) and low(<10𝜇g/m3) versus moderate


(10-25 𝜇g/m3) PM2.5 concentrations. We found well defined
clusters, within the parameter space, for PM2.5 concentrations
< 10 𝜇g/m3. Theregressionanalysisshowsthattheused
parameters can predict PM2.5 concentrations up to 20 𝜇g/m3
and the accuracy of the predictions is improved in condi-


tions of strong winds and high precipitation for both Coto-
collao and Belisario. There is a significant positive correlation
between the real concentrations and the predicted concen-
trations for all the study period. Theslightlyhighercorre-
lation during the rainy season confirms that the model can
predict PM2.5 concentrations better for more extreme weath-
er conditions.
Usingaconvolutionalbasedspatialrepresentation(CGM)
to perform regression shows improving performance com-
pared to various used machine learning algorithms (NN, L-
SVM, and BT). In addition to this model, finding trends over
periods of time with the use of time series algorithms could
further improvethepredictionandwouldmakealong-term
forecasting of PM2.5 concentrations possible [13].
Themaincontribution of this study is to propose an alter-
native approach to chemical transport numerical modeling,
such as WRF-Chem or CMAQ, the performance of which
depends on several input parameters (emission inventory,
orography, etc.) and the accuracy of built-in meteorological
models (WRF, MM5). The application of numerical models
for complex terrain regions is challenging, since important
topographic features are not well represented [11, 33]. This
produces imprecisions in not only forecasting air quality, but
also relevant meteorology [10, 12, 34, 35]. Here, the proposed
model provides a more reliable and more economical alter-
native to predict PM2.5 levels, as it only requires meteoro-
logical data acquisition. In addition, accurate meteorological
technology is far more affordable compared to air quality
sensors that can exceed the price over 100 times. Finally, this
model is based on the three basic meteorological parameters
(wind speed, wind direction, and precipitation), which have a
straightforward effect on pollution. Thus, by considering that
our model has a good prediction efficiency for a city of such
a complex topography, we argue that it could be success-
fully applied in other tropical locations (regions of reduced
changes in solar angle, temperature, and relative humidity).
Also, this work provides an insight into the main limi-
tations regarding PM2.5 prediction from meteorological data
andmachinelearning.Theclassificationandregressionshow
that concentrations > 20 𝜇g/m3 seem to be influenced more
by additional parameters than the meteorological factors
used in this study. For example, although daily temperature,
solar radiation, and pressure do not vary much during the
year, they might make a difference if analyzed during different
times of the day, causing different pollution levels in the city.
An interesting approach to tackle this limitation would be to
consider a hybrid model that would mix a numerical method
(WRF-Chem or CMAQ) with machine learning algorithms


[10].
Other climatic conditions and unusual impactful events


causing higher pollution levels (festivities, wild fires, acci-
dents, seasonal variability, or natural calamities) could also
explain changes in PM2.5 concentrations exceeding 20 𝜇g/m3.




## Journal of Electrical and Computer Engineering


13


Future work will consist ofidentifyingtheparametersor
events causing values above this threshold. Furthermore, we
intend to improve our CGManduseittoclassify outliers and
find their cause. Considering the diverse machine learning
models used in air quality prediction, such as Neural Network
[13-15], regression [18], decision trees, and Support Vector
Machine[17],weappliedandtestedmostoftheseclassifiersin
this study. Alternative approaches to improve the accuracy of
our model would consist of performing a prediction based on
an ensemble of different algorithms of data processing and
modeling [16, 17, 22].


# Conflicts of Interest


# The authors declare that there are no conflicts of interest regarding the publication of this paper.


# Acknowledgments


# Theauthors would like to thank David R. Sannino for editing the text.


# References


1. [1] United Nations, Department of Economic and Social Affairs (2015). World Population Prospects, the 2015 Revision, in Population Division edited, UN.

2. [2] World Health Organization, Media Centre (2016). Air pollution levels rising in many of the world's poorest cities. http://www .who.int/mediacentre/news/releases/2016/air-pollution-rising/. [3] J. Lelieveld, J. S. Evans, M. Fnais, D. Giannadaki, and A. Pozzer, "Thecontribution of outdoor air pollution sources to premature mortality on a global scale," Nature,vol. 525,no.7569,pp.367- 371, 2015.


[4] C.A.PopeandD.W.Dockery,"Healtheffectsoffineparticulate
air pollution: lines that connect," Journal of the Air and Waste
Management Association,vol. 56,no.6,pp.709-742,2006.
[5] Y. Rybarczyk and R. Zalakeviciute, "Machine learning approach
to forecasting urban pollution: a case study of Quito," in
Proceedings of the IEEE Ecuador Technical Chapters Meeting,
(ETCM '16),Guayaquil,Ecuador,2016.
[6] M.A.Pohjola,A.Kousa,J.Kukkonenetal.,"Thespatialand
temporalvariation ofmeasured urbanPM10 and PM2.5 in the
Helsinki metropolitan area," Water, Air and Soil Pollution: Focus,
vol. 2, no. 5, pp. 189-201, 2002.
[7] Y. Li, Q.Chen,H.Zhao,L.Wang,andR.Tao,"Variationsin
pm10, pm2.5 and pm1.0 in an urban area of the sichuan basin
and their relation to meteorological factors," Atmosphere,vol. 6,
no. 1, pp. 150-163, 2015.
[8] J. Wang and S. Ogawa, "Effects of meteorological conditions on
PM2.5 concentrations in Nagasaki, Japan," International Journal
of Environmental Research and Public Health, vol. 12,no.8,pp.
9089-9101, 2015.
[9] F.Zhang,H.Cheng,Z.Wangetal.,"Fineparticles(PM2.5)at
a CAWNET background site in central China: chemical com-
positions, seasonal variations and regional pollution events,"
Atmospheric Environment,vol. 86,pp.193-202,2014.


[10] X. Xi, Z. Wei, R. Xiaoguang et al., "A comprehensive evalu-
ation of air pollution prediction improvement by a machine
learning method," in Proceedings of the 10th IEEE International


Conference on Service Operations and Logistics, and Informatics,
SOLI 2015 - In conjunction with ICT4ALL '15, pp. 176-181,
Hammamet, Tunisia, November 2015.


1. [11] P. A. Jimenez and J. Dudhia, "Improving the representation of resolved and unresolved topographic effects on surface wind in the WRF model," Journal of Applied Meteorology and Climatology, vol. 51,no.2,pp.300-316,2012.

2. [12] R. Parra and V. D´ıaz, "Preliminary comparison of ozone con- centrations provided by the emission inventory/WRF-Chem model and the air quality monitoring network from the Distrito Metropolitano de Quito (Ecuador)," in Proceedings of the 8th annual WRF User's Workshop, NCAR, Boulder, Colo, USA. [13] X. Ni, H. Huang, and W. Du, "Relevance analysis and short- term prediction of PM2.5 concentrations in Beijing based on multi-source data," Atmospheric Environment,vol. 150,pp.146- 161, 2017.


[14] J.Chen,H.Chen,Z.Wu,D.Hu,andJ.Z.Pan,"Forecasting
smog-related health hazard based on social media and physical
sensor," Information Systems,vol. 64,pp.281-291,2017.
[15] J. Zhang and W. Ding, "Prediction of air pollutants concen-
tration based on an extreme learning machine: the case of
Hong Kong," International Journal of Environmental Research
and Public Health,vol. 14,no.2,p.114,2017.


[ 16 ] P. J ia ng , Q. Dong, an d P. Li , "A nove l hy br id s t ra t eg y fo r PM2.5
concentration analysis and prediction," Journal of Environmen-
tal Management,vol. 196,pp.443-457,2017.


1. [17] K. P. Singh, S. Gupta, and P. Rai, "Identifying pollution sources and predicting urban air quality using ensemble learning methods," Atmospheric Environment,vol. 80,pp.426-437,2013.

2. [18] C. Brokamp, R. Jandarov, M.B.Rao,G.LeMasters,andP. Ryan, "Exposure assessment models for elemental components of particulate matter in an urban environment: a comparison of regression and random forest approaches," Atmospheric Envi- ronment,vol. 151,pp.1-11,2017.

3. [19] M. Arhami, N. Kamali, and M. M. Rajabi, "Predicting hourly air pollutant levels using artificial neural networks coupled with uncertainty analysis by Monte Carlo simulations," Environmen- tal Science and Pollution Research,vol. 20,no.7,pp.4777-4789, 2013.

4. [20] A. Russo, F. Raischel, and P. G. Lind, "Air quality prediction using optimal neural networks with stochastic variables," Atmo- spheric Environment,vol. 79,pp.822-830,2013. [21] M. Fu, W. Wang, Z. Le, and M. S. Khorram, "Prediction of particular matter concentrations by developed feed-forward neural network with rolling mechanism and gray model," Neural Computing and Applications,vol. 26,no.8,pp.1789-1797, 2015. [22] W. Sun and J. Sun, "Daily PM2.5 concentration prediction based on principal component analysis and LSSVM optimized by cuckoo search algorithm," Journal of Environmental Manage- ment,vol. 188,pp.144-152,2017. [23] United Nations Development Programme (UNDP), Human development report 2014, Sustaining Human Progress: Reduc- ing Vulnerabilities and Building Resilience. [24] Instituto Nacional de Estadistica y Censos (INEC), Quito, el cant ´on m ´as poblado del Ecuador en el 2020, 2013. [25] E. Acu˜na and C. Rodriguez, "The treatment of missing values and its effect on classifier accuracy," in Classification, Clustering, and Data Mining Applications, D. Banks, F.R.McMorris, P. Arabie, and W. Gaul, Eds., pp. 639-647, Springer, Berlin, Heidelberg, 2004.




## 14 JournalofElectricalandComputerEngineering


1. [26] I. Mierswa, M. Wurst, R. Klinkenberg, M. Scholz, and T. Euler, "Yale: rapid prototyping for complex data mining tasks," in Proceedings of 12th ACM SIGKDD International Conference on Knowledge DiscoveryandDataMining, pp.935-940,Philadel- phia, PA, USA, 2006. [27] C. A. Calder and N. Cressie, "Some topics in convolution- based spatial modeling," in Proceedings of the 56th Session of the International Statistics Institute, International Statistics Institute, Netherlands, 2007. [28] F. Fouedjio, N. Desassis, and J. Rivoirard, "A generalized convolution model and estimation for non-stationary random functions," Spatial Statistics, vol. 16,pp.35-52,2016. [29] J. Babaud, A. P. Witkin, M. Baudin, and R. O. Duda, "Unique- ness of the Gaussian kernel for scale-space filtering," IEEE Transactions on Pattern Analysis and Machine Intelligence, vol. 8,no.1,pp.26-33,1986. [30] MA, "Ministerio Del Ambiente: Norma de Calidad del Aire Ambiente oNivel de Inmision Libro VI Anexo 4, 2015". [31] T. Fawcett, "An introduction to ROC analysis," Pattern Recogni- tion Letters, vol.27,no.8,pp.861-874,2006. [32] C. Seiffert, T. M. Khoshgoftaar, J. Van Hulse, and A. Napolitano, "RUSBoost: A hybrid approach to alleviating class imbalance," IEEE Transactions on Systems, Man, and Cybernetics Part A:Systems and Humans,vol.40,no. 1,pp.185-197,2010. [33] P. A. Jimenez and J. Dudhia, "On the ability of the WRF model to reproduce the surface wind direction over complex terrain," Journal of Applied Meteorology and Climatology, vol. 52,no.7, pp. 1610-1617, 2013. [34] A. Meij, A. De Gzella, C. Cuvelier et al., "The impact of MM5 and WRF meteorology over complex terrain on CHIMERE model calculations," Atmospheric Chemistry and Physics, vol. 9, no.17,pp.6611-6632,2009. [35] P. Saide, G. Carmichael, S. Spak et al., "Forecasting urban PM10andPM2.5pollutionepisodesinverystablenocturnal conditions and complex terrain using WRF-Chem CO tracer model," Atmospheric Environment, vol. 45, no. 16, pp. 2769- 2780, 2011.


