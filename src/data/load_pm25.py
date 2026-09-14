"""Carga reproducible de archivos mensuales de PM2.5 publicados por SIATA."""

from __future__ import annotations

import csv
from collections.abc import Iterable
from pathlib import Path

import pandas as pd

DATETIME_COLUMN = "fecha_hora"


def _detect_encoding(path: Path) -> str:
    """Retorna la primera codificación que puede decodificar la muestra."""
    sample = path.read_bytes()[:65_536]
    for encoding in ("utf-8-sig", "utf-8", "cp1252"):
        try:
            sample.decode(encoding)
            return encoding
        except UnicodeDecodeError:
            continue
    raise ValueError(f"No se pudo detectar la codificación de {path}")


def _detect_delimiter(path: Path, encoding: str) -> str:
    """Detecta el delimitador sin asumir que la extensión .tab es suficiente."""
    sample = path.read_bytes()[:65_536].decode(encoding)
    try:
        return csv.Sniffer().sniff(sample, delimiters="\t,;|").delimiter
    except csv.Error as exc:
        raise ValueError(f"No se pudo detectar el delimitador de {path}") from exc


def read_pm25_file(
    path: str | Path,
    *,
    add_source_file: bool = False,
) -> pd.DataFrame:
    """Lee y valida un archivo mensual de PM2.5.

    La publicación usa formato ancho: una fila por instante y una columna por
    estación. La función no fija nombres de estaciones porque la red puede
    cambiar entre meses.
    """
    source = Path(path)
    if not source.is_file():
        raise FileNotFoundError(f"No existe el archivo: {source}")

    encoding = _detect_encoding(source)
    delimiter = _detect_delimiter(source, encoding)
    frame = pd.read_csv(source, sep=delimiter, encoding=encoding)

    if frame.empty:
        raise ValueError(f"El archivo no contiene observaciones: {source}")
    if frame.columns.duplicated().any():
        duplicated = frame.columns[frame.columns.duplicated()].tolist()
        raise ValueError(f"Hay columnas duplicadas en {source}: {duplicated}")
    if DATETIME_COLUMN not in frame.columns:
        raise ValueError(
            f"Falta la columna temporal '{DATETIME_COLUMN}' en {source}; "
            f"columnas encontradas: {frame.columns.tolist()}"
        )

    parsed_dates = pd.to_datetime(
        frame[DATETIME_COLUMN], format="%Y-%m-%d %H:%M:%S", errors="coerce"
    )
    invalid_dates = parsed_dates.isna() & frame[DATETIME_COLUMN].notna()
    if invalid_dates.any():
        examples = frame.loc[invalid_dates, DATETIME_COLUMN].head(3).tolist()
        raise ValueError(f"Fechas inválidas en {source}: {examples}")
    frame[DATETIME_COLUMN] = parsed_dates

    station_columns = [column for column in frame.columns if column != DATETIME_COLUMN]
    if not station_columns:
        raise ValueError(f"No se encontraron columnas de estaciones en {source}")

    for column in station_columns:
        original = frame[column]
        numeric = pd.to_numeric(original, errors="coerce")
        invalid = numeric.isna() & original.notna()
        if invalid.any():
            examples = original.loc[invalid].head(3).tolist()
            raise ValueError(
                f"Valores no numéricos en la estación '{column}' de {source}: "
                f"{examples}"
            )
        frame[column] = numeric

    if add_source_file:
        frame["source_file"] = source.name
    return frame


def load_pm25_files(
    paths: str | Path | Iterable[str | Path],
    *,
    pattern: str = "Estaciones_PM2.5_*.tab",
    strict_schema: bool = False,
    add_source_file: bool = True,
) -> pd.DataFrame:
    """Carga múltiples meses, informa su origen y valida cambios de schema.

    Si ``paths`` es un directorio se buscan archivos con ``pattern``. Con
    ``strict_schema=True`` se exige exactamente el mismo conjunto y orden de
    columnas en todos los meses; en modo flexible, pandas conserva la unión de
    estaciones y representa ausencias con ``NaN``.
    """
    if isinstance(paths, (str, Path)):
        candidate = Path(paths)
        files = sorted(candidate.glob(pattern)) if candidate.is_dir() else [candidate]
    else:
        files = sorted(Path(path) for path in paths)

    if not files:
        raise FileNotFoundError("No se encontraron archivos mensuales de PM2.5")

    frames: list[pd.DataFrame] = []
    reference_schema: list[str] | None = None
    for file in files:
        frame = read_pm25_file(file, add_source_file=add_source_file)
        schema = [column for column in frame.columns if column != "source_file"]
        if reference_schema is None:
            reference_schema = schema
        elif strict_schema and schema != reference_schema:
            raise ValueError(
                f"Schema incompatible en {file.name}. "
                f"Esperado: {reference_schema}; encontrado: {schema}"
            )
        frames.append(frame)

    combined = pd.concat(frames, ignore_index=True, sort=False)
    return combined.sort_values(DATETIME_COLUMN, kind="stable").reset_index(drop=True)
