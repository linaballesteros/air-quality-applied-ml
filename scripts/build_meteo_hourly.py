"""Agrega los archivos meteorológicos minutales a una tabla horaria por estación.

Lee ``data/raw/meteo/<código>/``, aplica la bandera ``calidad`` y escribe
``data/interim/meteo_hourly.csv`` junto con un resumen de cobertura válida
por estación y variable dentro de la ventana analítica.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.data.load_meteo import METEO_VARIABLES, load_meteo_station  # noqa: E402
from src.data.stations import ANALYSIS_END, ANALYSIS_START, required_meteo_stations  # noqa: E402

RAW_DIR = PROJECT_ROOT / "data" / "raw" / "meteo"
OUTPUT = PROJECT_ROOT / "data" / "interim" / "meteo_hourly.csv"
COVERAGE_OUTPUT = PROJECT_ROOT / "data" / "interim" / "meteo_hourly_coverage.csv"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stations", help="códigos separados por coma; por defecto las asignadas")
    parser.add_argument("--min-minutes", type=int, default=45, help="minutos válidos por hora")
    parser.add_argument("--no-quality", action="store_true", help="ignorar la bandera calidad")
    return parser.parse_args()


def coverage_table(hourly: pd.DataFrame) -> pd.DataFrame:
    """Porcentaje de horas de la ventana con valor válido, por estación y variable."""
    start = pd.Timestamp(ANALYSIS_START + "-01")
    end = pd.Timestamp(ANALYSIS_END + "-01") + pd.offsets.MonthEnd(0) + pd.Timedelta(hours=23)
    expected_hours = int((end - start) / pd.Timedelta(hours=1)) + 1
    window = hourly[hourly["fecha_hora"].between(start, end)]
    rows = []
    for code, group in window.groupby("codigo"):
        row = {"codigo": code, "horas_con_registro": len(group)}
        for column in METEO_VARIABLES:
            if column in group:
                row[column] = round(100 * group[column].notna().sum() / expected_hours, 2)
        rows.append(row)
    return pd.DataFrame(rows).set_index("codigo")


def main() -> None:
    args = parse_args()
    stations = (
        [int(code) for code in args.stations.split(",")]
        if args.stations
        else required_meteo_stations()
    )
    frames = []
    for code in stations:
        folder = RAW_DIR / str(code)
        if not folder.is_dir():
            raise FileNotFoundError(f"No existe {folder}; ejecute scripts/download_meteo_dataset.py")
        hourly = load_meteo_station(
            folder, apply_quality=not args.no_quality, min_minutes=args.min_minutes
        )
        print(f"Estación {code}: {len(hourly)} horas")
        frames.append(hourly)

    table = pd.concat(frames, ignore_index=True)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(OUTPUT, index=False)
    coverage = coverage_table(table)
    coverage.to_csv(COVERAGE_OUTPUT)
    print(f"\nEscrito {OUTPUT.relative_to(PROJECT_ROOT)} con {len(table)} filas.")
    print(f"Cobertura válida (% de horas de {ANALYSIS_START} a {ANALYSIS_END}):")
    print(coverage.to_string())


if __name__ == "__main__":
    main()
