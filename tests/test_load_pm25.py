from pathlib import Path
import unittest

import pandas as pd

from src.data import load_pm25_files, read_pm25_file


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SAMPLE = PROJECT_ROOT / "data" / "raw" / "pm25" / "Estaciones_PM2.5_2013_01.tab"


@unittest.skipUnless(SAMPLE.exists(), "la muestra se descarga por separado")
class TestPm25Loader(unittest.TestCase):
    def test_reads_verified_sample(self) -> None:
        frame = read_pm25_file(SAMPLE)

        self.assertEqual(frame.shape, (744, 6))
        self.assertEqual(frame.columns[0], "fecha_hora")
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(frame["fecha_hora"]))
        self.assertEqual(frame["fecha_hora"].duplicated().sum(), 0)

    def test_adds_source_file_when_requested(self) -> None:
        frame = load_pm25_files([SAMPLE], add_source_file=True)

        self.assertIn("source_file", frame.columns)
        self.assertEqual(frame["source_file"].nunique(), 1)
        self.assertEqual(frame["source_file"].iat[0], SAMPLE.name)


if __name__ == "__main__":
    unittest.main()
