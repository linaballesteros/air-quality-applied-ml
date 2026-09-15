"""Descarga archivos originales de la red meteorológica de SIATA.

Cada estación meteorológica es un dataset independiente en Dataverse con un
archivo por mes y resolución de un minuto. Por defecto se descargan las
estaciones asignadas en ``src.data.stations`` para la ventana analítica.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.data.stations import (  # noqa: E402
    ANALYSIS_END,
    ANALYSIS_START,
    METEO_DATASETS,
    NETWORK_DATASETS,
    required_meteo_stations,
)

METADATA_URL = "https://datos.siata.gov.co/api/datasets/:persistentId/?persistentId={pid}"
ACCESS_URL = "https://datos.siata.gov.co/api/access/datafile/{file_id}?format=original"
DESTINATION = PROJECT_ROOT / "data" / "raw" / "meteo"
NETWORK_DESTINATION = PROJECT_ROOT / "data" / "raw" / "network"
MONTH_PATTERN = re.compile(r"_(\d{4})_(\d{2})\.")


def md5(path: Path) -> str:
    digest = hashlib.md5(usedforsecurity=False)
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fetch_manifest(persistent_id: str) -> tuple[dict, list[dict]]:
    with urllib.request.urlopen(METADATA_URL.format(pid=persistent_id), timeout=120) as response:
        payload = json.load(response)
    if payload.get("status") != "OK":
        raise RuntimeError(f"SIATA respondió con estado inesperado: {payload.get('status')}")
    version = payload["data"]["latestVersion"]
    files = [entry["dataFile"] for entry in version["files"]]
    return version, files


def download_one(file_metadata: dict, folder: Path, attempts: int = 3) -> str:
    destination = folder / file_metadata["filename"]
    expected_md5 = file_metadata["checksum"]["value"].lower()
    if destination.exists() and md5(destination) == expected_md5:
        return f"verificado {folder.name}/{destination.name}"

    temporary = destination.with_suffix(destination.suffix + ".part")
    for attempt in range(1, attempts + 1):
        try:
            request = urllib.request.Request(
                ACCESS_URL.format(file_id=file_metadata["id"]),
                headers={"User-Agent": "air-quality-applied-ml/1.0"},
            )
            with urllib.request.urlopen(request, timeout=300) as response:
                with temporary.open("wb") as output:
                    while chunk := response.read(1024 * 1024):
                        output.write(chunk)
            actual_md5 = md5(temporary)
            if actual_md5 != expected_md5:
                raise ValueError(
                    f"MD5 inválido para {destination.name}: "
                    f"esperado {expected_md5}, recibido {actual_md5}"
                )
            temporary.replace(destination)
            return f"descargado {folder.name}/{destination.name}"
        except Exception:
            temporary.unlink(missing_ok=True)
            if attempt == attempts:
                raise
            time.sleep(attempt * 2)
    raise RuntimeError("Estado de descarga inalcanzable")


def month_key(filename: str) -> str | None:
    match = MONTH_PATTERN.search(filename)
    return f"{match.group(1)}-{match.group(2)}" if match else None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--stations",
        help="códigos separados por coma; por defecto las asignadas en src/data/stations.py",
    )
    parser.add_argument("--start", default=ANALYSIS_START, help="primer mes YYYY-MM")
    parser.add_argument("--end", default=ANALYSIS_END, help="último mes YYYY-MM")
    parser.add_argument("--workers", type=int, default=4, help="descargas concurrentes")
    parser.add_argument(
        "--skip-network",
        action="store_true",
        help="no descargar las tablas descriptivas de las redes",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    stations = (
        [int(code) for code in args.stations.split(",")]
        if args.stations
        else required_meteo_stations()
    )
    unknown = [code for code in stations if code not in METEO_DATASETS]
    if unknown:
        raise ValueError(f"Sin DOI registrado para las estaciones {unknown}")

    jobs: list[tuple[dict, Path]] = []
    if not args.skip_network:
        NETWORK_DESTINATION.mkdir(parents=True, exist_ok=True)
        for name, pid in NETWORK_DATASETS.items():
            _, files = fetch_manifest(pid)
            folder = NETWORK_DESTINATION / name
            folder.mkdir(exist_ok=True)
            jobs.extend((item, folder) for item in files)

    for code in stations:
        version, files = fetch_manifest(METEO_DATASETS[code])
        folder = DESTINATION / str(code)
        folder.mkdir(parents=True, exist_ok=True)
        selected = [
            item
            for item in files
            if (key := month_key(item["filename"])) and args.start <= key <= args.end
        ]
        print(
            f"Estación {code}: versión {version['versionNumber']}.{version['versionMinorNumber']}; "
            f"{len(selected)} de {len(files)} archivos entre {args.start} y {args.end}."
        )
        jobs.extend((item, folder) for item in selected)

    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as executor:
        futures = {executor.submit(download_one, item, folder): item for item, folder in jobs}
        for future in as_completed(futures):
            print(future.result())


if __name__ == "__main__":
    main()
