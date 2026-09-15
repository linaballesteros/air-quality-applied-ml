"""Carga, decodificación de calidad y agregación horaria de la red meteorológica.

Los archivos minutales de SIATA no tienen celdas vacías: los faltantes se
marcan con ``-999`` y los datos dudosos con la columna ``calidad``. La
gramática de la bandera se verificó contra los 64 valores observados en los
1.131 archivos descargados el 2026-09-14 y contra la Tabla 3 del documento
*Generalidades Meteorológicas* (P-GAA-SIATA-108):

- ``1``/``2``: confiable (tiempo real / diferido).
- ``15…``/``25…``: dudoso; tras el prefijo, cada dígito señala una variable:
  ``1`` p, ``3`` t, ``4`` h, ``5`` pr, ``6`` vv y vv_max (``61`` solo vv,
  ``62`` solo vv_max), ``7`` dv y dv_max (``71`` solo dv, ``72`` solo dv_max).
- ``151``/``251``: dudoso en todas las variables.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

from .load_pm25 import _detect_delimiter, _detect_encoding

DATETIME_COLUMN = "fecha_hora"
STATION_COLUMN = "codigo"
QUALITY_COLUMN = "calidad"
METEO_VARIABLES = ["h", "t", "pr", "vv", "vv_max", "dv", "dv_max", "p"]
MISSING_SENTINEL = -999.0

_DIGIT_TO_VARIABLES = {
    "1": ("p",),
    "3": ("t",),
    "4": ("h",),
    "5": ("pr",),
    "6": ("vv", "vv_max"),
    "7": ("dv", "dv_max"),
}
_SUBINDEX = {
    ("6", "1"): ("vv",),
    ("6", "2"): ("vv_max",),
    ("7", "1"): ("dv",),
    ("7", "2"): ("dv_max",),
}
ALL_DOUBTFUL = frozenset(METEO_VARIABLES)


@lru_cache(maxsize=None)
def decode_quality(flag: str) -> frozenset[str]:
    """Retorna el conjunto de variables marcadas como dudosas por ``flag``.

    Un valor confiable retorna el conjunto vacío. Una bandera que no sigue la
    gramática documentada se trata como dudosa en todas las variables, que es
    la interpretación conservadora.
    """
    text = str(flag).strip()
    if text in {"1", "2"}:
        return frozenset()
    if len(text) < 3 or text[0] not in "12" or text[1] != "5":
        return ALL_DOUBTFUL
    rest = text[2:]
    if rest == "1":
        return ALL_DOUBTFUL
    doubtful: set[str] = set()
    index = 0
    while index < len(rest):
        digit = rest[index]
        following = rest[index + 1] if index + 1 < len(rest) else None
        if (digit, following) in _SUBINDEX:
            doubtful.update(_SUBINDEX[(digit, following)])
            index += 2
            continue
        if digit not in _DIGIT_TO_VARIABLES:
            return ALL_DOUBTFUL
        doubtful.update(_DIGIT_TO_VARIABLES[digit])
        index += 1
    return frozenset(doubtful)


def read_meteo_file(path: str | Path, *, add_source_file: bool = True) -> pd.DataFrame:
    """Lee un archivo mensual minutal y convierte ``-999`` en ``NaN``.

    No aplica la bandera de calidad; ver :func:`mask_doubtful`.
    """
    path = Path(path)
    encoding = _detect_encoding(path)
    delimiter = _detect_delimiter(path, encoding)
    frame = pd.read_csv(
        path,
        sep=delimiter,
        encoding=encoding,
        dtype={QUALITY_COLUMN: str},
        na_values=[],
        keep_default_na=False,
    )
    expected = [STATION_COLUMN, DATETIME_COLUMN, *METEO_VARIABLES, QUALITY_COLUMN]
    missing = [column for column in expected if column not in frame.columns]
    if missing:
        raise ValueError(f"Faltan columnas {missing} en {path.name}")

    frame[DATETIME_COLUMN] = pd.to_datetime(frame[DATETIME_COLUMN], format="%Y-%m-%d %H:%M:%S")
    frame[STATION_COLUMN] = frame[STATION_COLUMN].astype(int)
    for column in METEO_VARIABLES:
        values = pd.to_numeric(frame[column], errors="coerce")
        frame[column] = values.mask(values <= MISSING_SENTINEL)
    if frame[DATETIME_COLUMN].duplicated().any():
        raise ValueError(f"Timestamps duplicados en {path.name}")
    if add_source_file:
        frame["source_file"] = path.name
    return frame


def mask_doubtful(frame: pd.DataFrame) -> pd.DataFrame:
    """Reemplaza por ``NaN`` los valores marcados como dudosos en ``calidad``."""
    result = frame.copy()
    flags = result[QUALITY_COLUMN].astype(str)
    for flag in flags.unique():
        doubtful = decode_quality(flag)
        if doubtful:
            result.loc[flags == flag, list(doubtful)] = np.nan
    return result


def aggregate_hourly(frame: pd.DataFrame, *, min_minutes: int = 45) -> pd.DataFrame:
    """Agrega registros minutales a una fila por estación y hora.

    La hora ``HH:00`` resume los minutos ``HH:00``–``HH:59``. Cada variable
    se agrega solo si tiene al menos ``min_minutes`` minutos válidos:
    medias de ``t``, ``h``, ``pr`` y ``vv``; máximo de ``vv_max``; suma de
    ``p`` sin reescalar; dirección resultante de ``dv`` ponderada por ``vv``.
    Se conserva el número de minutos válidos por variable.
    """
    data = frame.copy()
    data["hour"] = data[DATETIME_COLUMN].dt.floor("h")
    radians = np.deg2rad(data["dv"])
    weight = data["vv"].where(data["dv"].notna())
    data["_u"] = -weight * np.sin(radians)
    data["_v"] = -weight * np.cos(radians)

    grouped = data.groupby([STATION_COLUMN, "hour"], sort=True)
    counts = grouped[METEO_VARIABLES].count()
    hourly = pd.DataFrame(
        {
            "t": grouped["t"].mean(),
            "h": grouped["h"].mean(),
            "pr": grouped["pr"].mean(),
            "vv": grouped["vv"].mean(),
            "vv_max": grouped["vv_max"].max(),
            "p": grouped["p"].sum(min_count=1),
        }
    )
    u_mean = grouped["_u"].mean()
    v_mean = grouped["_v"].mean()
    hourly["dv"] = (np.rad2deg(np.arctan2(-u_mean, -v_mean)) + 360.0) % 360.0
    counts_dv = grouped["_u"].count()

    for column in ["t", "h", "pr", "vv", "vv_max", "p"]:
        hourly[column] = hourly[column].where(counts[column] >= min_minutes)
        hourly[f"n_{column}"] = counts[column]
    hourly["dv"] = hourly["dv"].where(counts_dv >= min_minutes)
    hourly["n_dv"] = counts_dv

    hourly = hourly.reset_index().rename(columns={"hour": DATETIME_COLUMN})
    return hourly


def load_meteo_station(
    paths: str | Path | Iterable[str | Path],
    *,
    pattern: str = "Estacion_meteorologica_*.tab",
    apply_quality: bool = True,
    min_minutes: int = 45,
) -> pd.DataFrame:
    """Carga los meses de una estación y retorna la tabla horaria.

    ``paths`` puede ser el directorio de la estación o una lista de archivos.
    """
    if isinstance(paths, (str, Path)):
        candidate = Path(paths)
        files = sorted(candidate.glob(pattern)) if candidate.is_dir() else [candidate]
    else:
        files = sorted(Path(path) for path in paths)
    if not files:
        raise FileNotFoundError("No se encontraron archivos meteorológicos")

    frames = []
    for file in files:
        frame = read_meteo_file(file, add_source_file=False)
        if apply_quality:
            frame = mask_doubtful(frame)
        frames.append(aggregate_hourly(frame, min_minutes=min_minutes))
    hourly = pd.concat(frames, ignore_index=True)
    if hourly[[STATION_COLUMN, DATETIME_COLUMN]].duplicated().any():
        raise ValueError("Horas duplicadas entre archivos mensuales")
    return hourly.sort_values([STATION_COLUMN, DATETIME_COLUMN]).reset_index(drop=True)
