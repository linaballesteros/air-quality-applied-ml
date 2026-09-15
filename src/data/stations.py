"""Correspondencia verificada entre estaciones PM2.5 y meteorológicas de SIATA.

Las distancias se calcularon el 2026-09-14 con las coordenadas oficiales de
los datasets *Información de la Red de Calidad del Aire* (doi:10.83041/XTI3FH)
e *Información de la Red Meteorológica* (doi:10.83041/NXHIKW). La
justificación de cada asignación está en ``docs/station_matching.md``.
"""

from __future__ import annotations

# Ventana analítica vigente (ver context.md).
ANALYSIS_START = "2018-01"
ANALYSIS_END = "2025-12"

# Estaciones PM2.5 con cobertura >= 90 % en 2018-2025 -> código meteorológico.
PM25_TO_METEO: dict[str, int] = {
    "CEN-TRAF": 202,
    "ITA-CJUS": 252,
    "ITA-CONC": 206,
    "MED-ALTA": 197,
    "MED-BEME": 197,
    "EST-HOSP": 229,
    "BAR-TORR": 82,
    "COP-CVID": 73,
    "MED-VILL": 68,
    "MED-ARAN": 68,
    "MED-TESO": 59,
    "ENV-HOSP": 252,
    "CAL-JOAR": 105,
    "SAB-RAME": 229,
    "BEL-FEVE": 271,
    "MED-SCRI": 201,
}

# DOI del dataset Dataverse de cada estación meteorológica requerida.
METEO_DATASETS: dict[int, str] = {
    59: "doi:10.83041/6KPPNT",
    68: "doi:10.83041/LYQ8YR",
    73: "doi:10.83041/LRAEWS",
    82: "doi:10.83041/ANQUOJ",
    105: "doi:10.83041/ZPACRM",
    197: "doi:10.83041/RJPIBG",
    201: "doi:10.83041/9DJJ26",
    202: "doi:10.83041/A6AUIK",
    206: "doi:10.83041/OM9XPU",
    229: "doi:10.83041/LBFT8T",
    252: "doi:10.83041/1AHV46",
    271: "doi:10.83041/NEAMJ8",
}

# Datasets descriptivos de cada red (tablas de estaciones y PDF de generalidades).
NETWORK_DATASETS: dict[str, str] = {
    "calidad_aire": "doi:10.83041/XTI3FH",
    "meteorologica": "doi:10.83041/NXHIKW",
}


def required_meteo_stations() -> list[int]:
    """Códigos meteorológicos únicos que exige la correspondencia vigente."""
    return sorted(set(PM25_TO_METEO.values()))
