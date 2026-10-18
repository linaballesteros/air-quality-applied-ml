"""Evaluación con origen móvil y reglas de aviso de Nivel de Prevención.

Para cada año ``Y`` el modelo se entrena solo con los años anteriores a ``Y``
y predice ``Y``. El umbral de aviso de un año de prueba se calibra con las
predicciones de años anteriores (también fuera de muestra) y se congela
antes de mirar el año de prueba.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable

import numpy as np
import pandas as pd

PREVENTION_THRESHOLD = 38.0  # Nivel de Prevención PM2.5 24 h, Resolución 2254 de 2017, Tabla 4


def regression_metrics(y_true: pd.Series, y_pred: pd.Series) -> dict[str, float]:
    error = y_true - y_pred
    return {
        "MAE": float(error.abs().mean()),
        "RMSE": float(np.sqrt((error**2).mean())),
        "R2": float(1 - (error**2).sum() / ((y_true - y_true.mean()) ** 2).sum()),
    }


def warning_metrics(
    y_true: pd.Series,
    y_pred: pd.Series,
    starts: pd.Series,
    alert_threshold: float,
    event_threshold: float = PREVENTION_THRESHOLD,
) -> dict[str, float]:
    """Precisión y recall de avisar "mañana en prevención" cuando la
    predicción alcanza ``alert_threshold``; ``starts`` marca los inicios de
    episodio (hoy fuera de prevención, mañana dentro)."""
    event = y_true >= event_threshold
    alert = y_pred >= alert_threshold
    hits = event & alert
    return {
        "eventos": int(event.sum()),
        "avisos": int(alert.sum()),
        "precision": float(hits.sum() / alert.sum()) if alert.sum() else np.nan,
        "recall": float(hits.sum() / event.sum()) if event.sum() else np.nan,
        "inicios": int(starts.sum()),
        "inicios_avisados": int((hits & starts).sum()),
    }


def threshold_for_budget(y_true: pd.Series, y_pred: pd.Series, event_threshold: float = PREVENTION_THRESHOLD) -> float:
    """Umbral de aviso con el que el número de avisos iguala el número de
    eventos observados en el periodo de calibración."""
    n_events = int((y_true >= event_threshold).sum())
    if n_events == 0:
        return event_threshold
    return float(np.sort(y_pred.to_numpy())[::-1][n_events - 1])


def rolling_origin_predictions(
    data: pd.DataFrame,
    years: Iterable[int],
    fit_predict: Callable[[pd.DataFrame, pd.DataFrame], np.ndarray],
    year_column: str = "year",
) -> pd.Series:
    """Predicción fuera de muestra de cada año entrenando solo con los años
    anteriores. Devuelve una serie alineada con el índice de ``data``."""
    predictions = []
    for year in years:
        train = data[data[year_column] < year]
        test = data[data[year_column] == year]
        predictions.append(pd.Series(fit_predict(train, test), index=test.index))
    return pd.concat(predictions)
