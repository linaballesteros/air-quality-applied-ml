"""Tabla de predictores estación-día para pronosticar la media de PM2.5 de mañana.

Cada fila es una estación en un día ``d``. Todos los predictores usan solo
información observada hasta el final del día ``d``; el target es la media del
día ``d + 1``. Las variables de calendario describen el día ``d + 1``, que se
conoce de antemano. No se imputa: un predictor sin datos suficientes queda
vacío.
"""

from __future__ import annotations

import pandas as pd

MIN_HOURS_PER_DAY = 18
EVENING_HOURS = range(18, 24)
MIN_EVENING_HOURS = 4
LAG_DAYS = 6

PM25_FEATURES: list[str] = [
    "pm25_mean",
    *[f"pm25_lag{k}" for k in range(1, LAG_DAYS + 1)],
    "pm25_roll3_mean",
    "pm25_roll7_mean",
    "pm25_roll7_std",
    "pm25_diff1",
    "pm25_max",
    "pm25_evening_mean",
]
METEO_FEATURES: list[str] = ["t", "h", "pr", "vv", "vv_max", "p", "p_sum3"]
CALENDAR_FEATURES: list[str] = ["target_month", "target_day_of_week"]
TARGET = "pm25_mean_d_plus_1"

# Agregación diaria de cada variable meteorológica horaria.
METEO_DAILY_AGG: dict[str, str] = {
    "t": "mean",
    "h": "mean",
    "pr": "mean",
    "vv": "mean",
    "vv_max": "max",
    "p": "sum",
}


def _complete_grid(frame: pd.DataFrame, key: str, start: str, end: str) -> pd.DataFrame:
    """Reindexa a todas las fechas de la ventana para que desplazar una fila
    equivalga exactamente a un día."""
    dates = pd.date_range(start, end, freq="D")
    index = pd.MultiIndex.from_product([sorted(frame[key].unique()), dates], names=[key, "date"])
    return frame.set_index([key, "date"]).reindex(index).reset_index()


def daily_pm25(hourly: pd.DataFrame, start: str, end: str) -> pd.DataFrame:
    """Agrega PM2.5 horario en formato largo (``station_id``, ``fecha_hora``,
    ``pm25``) a estación-día."""
    hourly = hourly.assign(date=hourly["fecha_hora"].dt.floor("D"), hour=hourly["fecha_hora"].dt.hour)
    grouped = hourly.groupby(["station_id", "date"])["pm25"]
    daily = grouped.agg(pm25_mean="mean", valid_hours="count", pm25_max="max").reset_index()
    enough = daily["valid_hours"] >= MIN_HOURS_PER_DAY
    daily[["pm25_mean", "pm25_max"]] = daily[["pm25_mean", "pm25_max"]].where(enough, axis=0)

    evening = (
        hourly[hourly["hour"].isin(EVENING_HOURS)]
        .groupby(["station_id", "date"])["pm25"]
        .agg(["mean", "count"])
    )
    evening_mean = evening["mean"].where(evening["count"] >= MIN_EVENING_HOURS).rename("pm25_evening_mean")
    daily = daily.merge(evening_mean.reset_index(), on=["station_id", "date"], how="left")
    daily = _complete_grid(daily, "station_id", start, end)
    daily["valid_hours"] = daily["valid_hours"].fillna(0).astype(int)
    return daily


def daily_meteo(hourly: pd.DataFrame, start: str, end: str) -> pd.DataFrame:
    """Agrega la tabla meteorológica horaria (``codigo``, ``fecha_hora`` y
    variables) a estación-día, exigiendo 18 horas válidas por variable.

    Las presiones de 0 hPa no son físicas (la presión en el valle ronda
    840 hPa) y la bandera de calidad no las marca; se tratan como faltantes.
    """
    hourly = hourly.assign(date=hourly["fecha_hora"].dt.floor("D"))
    hourly["pr"] = hourly["pr"].where(hourly["pr"] > 0)
    variables = list(METEO_DAILY_AGG)
    grouped = hourly.groupby(["codigo", "date"])
    values = grouped.agg(METEO_DAILY_AGG)
    counts = grouped[variables].count()
    daily = values.where(counts >= MIN_HOURS_PER_DAY).reset_index()
    daily = _complete_grid(daily, "codigo", start, end)
    daily["p_sum3"] = daily.groupby("codigo")["p"].transform(lambda s: s.rolling(3, min_periods=3).sum())
    return daily


def build_features(
    pm25_hourly: pd.DataFrame,
    meteo_hourly: pd.DataFrame,
    station_to_meteo: dict[str, int],
    start: str,
    end: str,
) -> pd.DataFrame:
    """Construye la tabla estación-día con predictores y target.

    ``start`` y ``end`` (``YYYY-MM-DD``) delimitan los días ``d``; el target
    del último día queda vacío. Las filas sin media de hoy o sin target se
    conservan: el filtrado corresponde a cada experimento.
    """
    pm25_hourly = pm25_hourly[pm25_hourly["station_id"].isin(station_to_meteo)]
    table = daily_pm25(pm25_hourly, start, end)
    by_station = table.groupby("station_id")["pm25_mean"]

    for k in range(1, LAG_DAYS + 1):
        table[f"pm25_lag{k}"] = by_station.shift(k)
    table["pm25_roll3_mean"] = by_station.transform(lambda s: s.rolling(3, min_periods=2).mean())
    table["pm25_roll7_mean"] = by_station.transform(lambda s: s.rolling(7, min_periods=5).mean())
    table["pm25_roll7_std"] = by_station.transform(lambda s: s.rolling(7, min_periods=5).std())
    table["pm25_diff1"] = table["pm25_mean"] - table["pm25_lag1"]
    table[TARGET] = by_station.shift(-1)

    target_date = table["date"] + pd.Timedelta(days=1)
    table["target_month"] = target_date.dt.month
    table["target_day_of_week"] = target_date.dt.dayofweek

    meteo = daily_meteo(meteo_hourly, start, end)
    table["codigo"] = table["station_id"].map(station_to_meteo)
    table = table.merge(meteo, on=["codigo", "date"], how="left")
    columns = [
        "station_id", "date", "codigo", "valid_hours",
        *PM25_FEATURES, *METEO_FEATURES, *CALENDAR_FEATURES, TARGET,
    ]
    return table[columns].sort_values(["station_id", "date"]).reset_index(drop=True)
