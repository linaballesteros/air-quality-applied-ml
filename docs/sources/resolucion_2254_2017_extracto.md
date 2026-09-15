# Resolución 2254 de 2017 (MinAmbiente) — extracto verificado

Norma de calidad del aire de Colombia. Consultada el 2026-09-14 en la copia
del régimen legal de Bogotá
(<https://www.alcaldiabogota.gov.co/sisjur/normas/Norma1.jsp?i=82634>).
Antes de citar en el paper, confirmar cada cifra en el PDF oficial
(<https://www.ins.gov.co/Normatividad/Resoluciones/RESOLUCI%C3%93N%202254%20DE%202017.pdf>).

## Tres umbrales distintos para PM2.5 (24 horas)

| Concepto | Artículo | PM2.5 24 h (µg/m³) | Uso |
| --- | --- | --- | --- |
| Nivel máximo permisible | Art. 2 (vigente desde 2018-07-01) | 37 | Cumplimiento de la norma de calidad del aire. No es un umbral de alerta. |
| Nivel de Prevención | Art. 10, Tabla 4 | 38–55 | Declaración de niveles que activan medidas. Alerta: 56–150. Emergencia: ≥151. Aplicable a PM2.5 desde 2018-07-01. |
| ICA Naranja (dañina a grupos sensibles) | Art. 20, Tabla 6 | 40,5–65,4 | Índice de comunicación al público. Verde 0–15,4; amarillo 15,5–40,4; rojo 65,5–150,4; púrpura 150,5–250,4; marrón ≥250,5. |

## Disposiciones relevantes para el proyecto

- **Art. 11, constatación:** los niveles se declaran "a través del uso de
  medias móviles de 24 horas de concentración del contaminante de interés".
- **Art. 11, pronóstico:** "Se podrá declarar un nivel con anticipación cuando
  el modelo de pronóstico indique dicha condición".
- **Art. 2, parágrafo 2:** "El promedio de concentraciones de diferentes
  puntos de monitoreo no será válido para evaluar el cumplimiento de dichos
  niveles"; la evaluación es por punto de monitoreo.

## Uso en el proyecto

- Umbral principal de evaluación: **Nivel de Prevención, ≥38 µg/m³**.
- Umbral secundario: ICA Naranja, ≥40,5 µg/m³.
- El target del proyecto (media del día calendario por estación) es una media
  de 24 horas; la relación con la media móvil se documenta en
  [`../decisions.md`](../decisions.md).
