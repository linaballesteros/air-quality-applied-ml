"""Descarga archivos originales de PM2.5 usando la API oficial de SIATA."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

PERSISTENT_ID = "doi:10.83041/AUWZWT"
METADATA_URL = (
    "https://datos.siata.gov.co/api/datasets/:persistentId/"
    f"?persistentId={PERSISTENT_ID}"
)
ACCESS_URL = "https://datos.siata.gov.co/api/access/datafile/{file_id}?format=original"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DESTINATION = PROJECT_ROOT / "data" / "raw" / "pm25"


def md5(path: Path) -> str:
    digest = hashlib.md5(usedforsecurity=False)
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fetch_manifest() -> tuple[dict, list[dict]]:
    with urllib.request.urlopen(METADATA_URL, timeout=120) as response:
        payload = json.load(response)
    if payload.get("status") != "OK":
        raise RuntimeError(f"SIATA respondió con estado inesperado: {payload.get('status')}")
    version = payload["data"]["latestVersion"]
    files = [entry["dataFile"] for entry in version["files"]]
    return version, files


def download_one(file_metadata: dict, attempts: int = 3) -> str:
    destination = DESTINATION / file_metadata["filename"]
    expected_md5 = file_metadata["checksum"]["value"].lower()
    if destination.exists() and md5(destination) == expected_md5:
        return f"verificado {destination.name}"

    temporary = destination.with_suffix(destination.suffix + ".part")
    for attempt in range(1, attempts + 1):
        try:
            request = urllib.request.Request(
                ACCESS_URL.format(file_id=file_metadata["id"]),
                headers={"User-Agent": "air-quality-applied-ml/1.0"},
            )
            with urllib.request.urlopen(request, timeout=120) as response:
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
            return f"descargado {destination.name}"
        except Exception:
            temporary.unlink(missing_ok=True)
            if attempt == attempts:
                raise
            time.sleep(attempt * 2)
    raise RuntimeError("Estado de descarga inalcanzable")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--all", action="store_true", help="descarga todos los meses")
    selection.add_argument("--year", help="descarga solo un año, por ejemplo 2013")
    parser.add_argument("--workers", type=int, default=6, help="descargas concurrentes")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    version, manifest = fetch_manifest()
    selected = manifest if args.all else [
        item for item in manifest if f"_{args.year}_" in item["filename"]
    ]
    if not selected:
        raise ValueError("La selección no contiene archivos")

    DESTINATION.mkdir(parents=True, exist_ok=True)
    print(
        f"Dataset versión {version['versionNumber']}.{version['versionMinorNumber']}; "
        f"{len(selected)} de {len(manifest)} archivos seleccionados."
    )
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as executor:
        futures = {executor.submit(download_one, item): item for item in selected}
        for future in as_completed(futures):
            print(future.result())


if __name__ == "__main__":
    main()
