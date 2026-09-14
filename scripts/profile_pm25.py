"""Imprime un perfil reproducible de todos los archivos locales de PM2.5."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import sys

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data" / "raw" / "pm25"
sys.path.insert(0, str(PROJECT_ROOT))

from src.data import read_pm25_file  # noqa: E402


def main() -> None:
    files = sorted(DATA_DIR.glob("Estaciones_PM2.5_*.tab"))
    if not files:
        raise FileNotFoundError(f"No hay archivos en {DATA_DIR}")

    frames: list[pd.DataFrame] = []
    schemas: Counter[tuple[str, ...]] = Counter()
    monthly_rows: list[int] = []
    for file in files:
        frame = read_pm25_file(file, add_source_file=True)
        stations = tuple(
            column
            for column in frame.columns
            if column not in {"fecha_hora", "source_file"}
        )
        schemas[stations] += 1
        monthly_rows.append(len(frame))
        frames.append(frame)

    combined = pd.concat(frames, ignore_index=True, sort=False)
    stations = sorted(
        column
        for column in combined.columns
        if column not in {"fecha_hora", "source_file"}
    )
    values = combined[stations]
    timestamps = combined["fecha_hora"]
    expected_hours = pd.date_range(timestamps.min(), timestamps.max(), freq="h")

    print(f"files={len(files)}")
    print(f"schema_variants={len(schemas)}")
    print(f"rows={len(combined)}")
    print(f"station_columns={len(stations)}")
    print(f"measurements_non_null={int(values.notna().sum().sum())}")
    print(f"measurements_missing={int(values.isna().sum().sum())}")
    print(f"range_start={timestamps.min()}")
    print(f"range_end={timestamps.max()}")
    print(f"duplicate_rows={int(combined.duplicated().sum())}")
    print(f"duplicate_timestamps={int(timestamps.duplicated().sum())}")
    print(f"missing_global_hours={len(expected_hours.difference(timestamps))}")
    print(f"rows_all_stations_missing={int(values.isna().all(axis=1).sum())}")
    print(f"negative_measurements={int(values.lt(0).sum().sum())}")
    print(f"zero_measurements={int(values.eq(0).sum().sum())}")
    print(f"monthly_rows_min={min(monthly_rows)}")
    print(f"monthly_rows_max={max(monthly_rows)}")
    print("\nstation_coverage")
    first_measurement = {
        station: timestamps[combined[station].notna()].min() for station in stations
    }
    last_measurement = {
        station: timestamps[combined[station].notna()].max() for station in stations
    }
    active_hours = {
        station: int(
            (last_measurement[station] - first_measurement[station])
            / pd.Timedelta(hours=1)
        )
        + 1
        for station in stations
    }
    non_null = values.notna().sum()
    coverage = pd.DataFrame(
        {
            "non_null": non_null,
            "coverage_pct_active_period": {
                station: 100 * int(non_null[station]) / active_hours[station]
                for station in stations
            },
            "first_measurement": first_measurement,
            "last_measurement": last_measurement,
        }
    ).sort_values("non_null", ascending=False)
    print(coverage.to_string(float_format=lambda value: f"{value:.2f}"))
    print("\nschema_variants")
    for schema, count in schemas.most_common():
        print(f"{count:3d} files: {list(schema)}")


if __name__ == "__main__":
    main()
