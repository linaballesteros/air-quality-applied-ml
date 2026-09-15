from pathlib import Path
import unittest

import numpy as np
import pandas as pd

from src.data.load_meteo import (
    ALL_DOUBTFUL,
    aggregate_hourly,
    decode_quality,
    mask_doubtful,
    read_meteo_file,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SAMPLE = PROJECT_ROOT / "data" / "raw" / "meteo" / "202" / "Estacion_meteorologica_202_2018_01.tab"


class TestDecodeQuality(unittest.TestCase):
    def test_reliable_flags(self) -> None:
        self.assertEqual(decode_quality("1"), frozenset())
        self.assertEqual(decode_quality("2"), frozenset())

    def test_documented_flags(self) -> None:
        self.assertEqual(decode_quality("151"), ALL_DOUBTFUL)
        self.assertEqual(decode_quality("251"), ALL_DOUBTFUL)
        self.assertEqual(decode_quality("1511"), {"p"})
        self.assertEqual(decode_quality("153"), {"t"})
        self.assertEqual(decode_quality("154"), {"h"})
        self.assertEqual(decode_quality("155"), {"pr"})
        self.assertEqual(decode_quality("156"), {"vv", "vv_max"})
        self.assertEqual(decode_quality("1561"), {"vv"})
        self.assertEqual(decode_quality("1562"), {"vv_max"})
        self.assertEqual(decode_quality("157"), {"dv", "dv_max"})
        self.assertEqual(decode_quality("1571"), {"dv"})
        self.assertEqual(decode_quality("1572"), {"dv_max"})

    def test_combined_flags_observed_in_data(self) -> None:
        self.assertEqual(decode_quality("1534"), {"t", "h"})
        self.assertEqual(decode_quality("1515"), {"p", "pr"})
        self.assertEqual(decode_quality("1567"), {"vv", "vv_max", "dv", "dv_max"})
        self.assertEqual(decode_quality("156272"), {"vv_max", "dv_max"})
        self.assertEqual(decode_quality("1556272"), {"pr", "vv_max", "dv_max"})
        self.assertEqual(decode_quality("15361"), {"t", "vv"})
        self.assertEqual(decode_quality("25345"), {"t", "h", "pr"})
        self.assertEqual(decode_quality("15146272"), {"p", "h", "vv_max", "dv_max"})

    def test_unknown_flag_is_conservative(self) -> None:
        self.assertEqual(decode_quality("1345"), ALL_DOUBTFUL)
        self.assertEqual(decode_quality("159"), ALL_DOUBTFUL)
        self.assertEqual(decode_quality(""), ALL_DOUBTFUL)


def _minute_frame(minutes: int, *, calidad: str = "1") -> pd.DataFrame:
    stamps = pd.date_range("2020-03-01 05:00:00", periods=minutes, freq="min")
    return pd.DataFrame(
        {
            "codigo": 202,
            "fecha_hora": stamps,
            "h": 80.0,
            "t": 20.0,
            "pr": 850.0,
            "vv": 2.0,
            "vv_max": np.linspace(1.0, 3.0, minutes),
            "dv": 90.0,
            "dv_max": 95.0,
            "p": 0.1,
            "calidad": calidad,
        }
    )


class TestAggregation(unittest.TestCase):
    def test_full_hour_aggregates_each_variable(self) -> None:
        hourly = aggregate_hourly(_minute_frame(60))

        self.assertEqual(len(hourly), 1)
        row = hourly.iloc[0]
        self.assertEqual(row["fecha_hora"], pd.Timestamp("2020-03-01 05:00:00"))
        self.assertAlmostEqual(row["t"], 20.0)
        self.assertAlmostEqual(row["vv_max"], 3.0)
        self.assertAlmostEqual(row["p"], 6.0)
        self.assertAlmostEqual(row["dv"], 90.0, places=6)
        self.assertEqual(row["n_t"], 60)

    def test_hour_below_min_minutes_is_nan_but_counted(self) -> None:
        hourly = aggregate_hourly(_minute_frame(30))

        self.assertTrue(np.isnan(hourly.iloc[0]["t"]))
        self.assertEqual(hourly.iloc[0]["n_t"], 30)

    def test_mask_doubtful_only_affects_flagged_variables(self) -> None:
        frame = _minute_frame(60, calidad="1534")
        masked = mask_doubtful(frame)

        self.assertTrue(masked["t"].isna().all())
        self.assertTrue(masked["h"].isna().all())
        self.assertTrue(masked["pr"].notna().all())
        self.assertTrue(frame["t"].notna().all())

    def test_wind_direction_is_vector_mean(self) -> None:
        frame = _minute_frame(60)
        frame.loc[:29, "dv"] = 350.0
        frame.loc[30:, "dv"] = 10.0
        hourly = aggregate_hourly(frame)

        self.assertAlmostEqual(hourly.iloc[0]["dv"], 0.0, places=6)


@unittest.skipUnless(SAMPLE.exists(), "los datos meteorológicos se descargan por separado")
class TestRealFile(unittest.TestCase):
    def test_reads_sample_month(self) -> None:
        frame = read_meteo_file(SAMPLE)

        self.assertEqual(len(frame), 31 * 24 * 60)
        self.assertEqual(frame["codigo"].unique().tolist(), [202])
        self.assertFalse((frame[["t", "h", "pr", "p"]] <= -999).any().any())

        hourly = aggregate_hourly(mask_doubtful(frame))
        self.assertEqual(len(hourly), 31 * 24)
