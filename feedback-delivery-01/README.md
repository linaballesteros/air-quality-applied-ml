# Feedback de la Entrega 1 y plan para la entrega final

Carpeta de uso interno: vive solo en `development` y no se lleva a `main`.

- `applied_ml_delivery-checked.pdf`: el paper de la Entrega 1 con las
  anotaciones del profesor.
- [`respuestas.md`](respuestas.md): respuesta a cada duda, con cifras
  verificadas y textos borrador listos para el paper y la presentación.

## 1. Qué dijo el profesor

### Comentario general (texto)

1. Trabajar con **Gradient Boosting**.
2. En la entrega final, **comparar nuestros resultados con Baena-Salazar et
   al. [3]**.
3. Usar **ventanas de tiempo** (rezagos de varios días) y un **análisis SHAP**
   para ver si, como en Baena-Salazar, el PM2.5 del día anterior es la
   entrada de mayor peso.
4. Duda sobre los datos: el notebook muestra 5 estaciones en un archivo y
   después "un montón". Pide explicarlo en la próxima clase y en la
   presentación final.

### Anotaciones en el PDF

| Pág. | Texto resaltado | Comentario |
| --- | --- | --- |
| 1 | "…favorecer su acumulación [3]" | Sin comentario (señala la cita de Baena-Salazar). |
| 1 | "…la media del día actual como pronóstico del siguiente" | Sin comentario (señala la persistencia). |
| 2 | Segunda mitad de la pregunta de investigación | "Es válido tener 2 preguntas de investigación; si lo necesita, divídalas." |
| 2 | "No se imputaron faltantes ni se eliminaron valores extremos." | "¿Existían faltantes y qué se hizo con ellos? El proceso de extracción de medias y cambios de tamaño quedaría mejor en un diagrama de flujo." |
| 2 | "Para el análisis se tomó la ventana 2018–2025" | "¿Por qué no todos?" |
| 3 | Párrafo de la Tabla II | "Desarrollen un poco más la idea de la Tabla II; profundicen la explicación." |

## 2. Plan de trabajo para la entrega final

Cada tarea apunta a una observación concreta. La guía oficial de la Entrega 2
todavía no está publicada; cuando salga, se ajusta este plan.

### A. Responder en la próxima clase (sin código)

- [ ] Explicar la composición de los datos: archivos mensuales con columnas
      distintas según qué estaciones existían. Guion y tabla en
      [`respuestas.md` §1](respuestas.md#1-por-qué-5-estaciones-en-un-archivo-y-después-muchas).

### B. Modelado (núcleo de la entrega final)

- [ ] Construir la tabla de predictores con **ventanas de tiempo**: rezagos
      de PM2.5 de 1 a 7 días, medias y desviación móviles de 3 y 7 días,
      máximo y media de las últimas horas del día `d`, meteorología del día
      `d` y lluvia acumulada de 3 días (entrada que usó Baena-Salazar).
- [ ] Entrenar **XGBoost** (Gradient Boosting) con origen móvil: probar en
      2022, 2023, 2024 y 2025 entrenando con los años anteriores.
      XGBoost acepta faltantes sin imputar, lo que encaja con la decisión
      de no imputar.
- [ ] Comparar tres configuraciones: persistencia, XGBoost sin meteorología
      y XGBoost con meteorología (responde las dos preguntas, ver C).
- [ ] Calibrar el umbral de aviso solo con train/validación y comparar con
      persistencia a igual número de avisos (decisión vigente).
- [ ] **SHAP** (`shap.TreeExplainer`) sobre el modelo con meteorología:
      porcentaje de importancia del PM2.5 de ayer frente al 34,2 % de
      Baena-Salazar, y figura de resumen.

### C. Paper

- [ ] **Dividir la pregunta en dos** (borrador en
      [`respuestas.md` §5](respuestas.md#5-dos-preguntas-de-investigación)).
- [ ] Explicar **por qué 2018–2025** y no todo el histórico (texto en
      [`respuestas.md` §2](respuestas.md#2-por-qué-la-ventana-20182025-y-no-todos-los-años)).
- [ ] Añadir un **diagrama de flujo** de datos: de archivos mensuales a la
      tabla supervisada, con cuántos registros se pierden en cada paso y
      por qué (cifras en [`respuestas.md` §3](respuestas.md#3-faltantes-qué-había-y-qué-se-hizo)).
- [ ] Ampliar el párrafo de la **Tabla II** (borrador en
      [`respuestas.md` §4](respuestas.md#4-tabla-ii-explicación-ampliada)).
- [ ] Nueva subsección de **comparación con Baena-Salazar** (diseño y
      resultado preliminar en [`respuestas.md` §6](respuestas.md#6-comparación-con-baena-salazar-et-al)).

### D. Notebook

- [ ] Añadir tras la sección 4.1 una tabla o figura de **estaciones activas
      por año**, para que la duda del profesor quede resuelta al leerlo.
- [ ] Nuevo notebook `02_modelado.ipynb` para B, con las cifras que citará
      el paper.
- [ ] Añadir `scikit-learn`, `xgboost` y `shap` a `requirements.txt`.

### E. Pendientes que ya existían y siguen abiertos

- [ ] Resolver los huecos meteorológicos de `docs/station_matching.md`
      (viento de 206, presión de 252, lluvia de 229, estación 271).
- [ ] Filtrar las 7 horas con presión de 0 hPa.

## 3. Dificultades a decidir entre los dos

1. **Comparación exacta con Baena-Salazar.** Su estudio usa 2013–2016,
   tres estaciones (ITA-CONC, MED-UNNV y MED-MANT) y la altura de la capa de
   mezcla. MED-MANT no está en el dataset de PM2.5, MED-UNNV se retiró en
   2020, no tenemos capa de mezcla y la meteorología descargada empieza en
   2018. Propuesta: replicar su periodo de validación solo con PM2.5 para
   ITA-CONC y MED-UNNV, y comparar en nuestra ventana con sus mismas
   métricas. Hay que comprobar si SIATA publica meteorología de 2013–2016
   para esas estaciones.
2. **Métricas de Baena-Salazar poco definidas.** No explican cómo calculan el
   "error" porcentual y parecen reportar r² sobre calibración y validación
   juntas. La comparación debe decirlo explícitamente.
3. **Requisitos de la Entrega 2 sin publicar.** La guía oficial aún no
   existe (la de la Entrega 1 solo dice que cubrirá metodología,
   resultados, conclusiones y abstract). Este plan se revisa cuando salga.
4. **Semestre 2026 disponible.** El dataset llega hasta junio de 2026 e
   incluye la temporada crítica de febrero–marzo. Podría servir como prueba
   final que ningún modelo ha visto, pero exigiría descargar la meteorología
   de 2026.
