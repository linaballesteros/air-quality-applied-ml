import unittest

import numpy as np
import pandas as pd

from src.features import PM25_FEATURES, TARGET, build_features

START, END = "2020-01-01", "2020-01-10"


def synthetic_pm25(days: int = 10) -> pd.DataFrame:
    """Una estación cuyo PM2.5 horario es constante e igual al número de día."""
    hours = pd.date_range(START, periods=24 * days, freq="h")
    return pd.DataFrame({"station_id": "AAA", "fecha_hora": hours, "pm25": (hours.day).astype(float)})


def synthetic_meteo(days: int = 10) -> pd.DataFrame:
    hours = pd.date_range(START, periods=24 * days, freq="h")
    return pd.DataFrame(
        {
            "codigo": 1,
            "fecha_hora": hours,
            "t": 20.0,
            "h": 70.0,
            "pr": 840.0,
            "vv": 1.5,
            "vv_max": 4.0,
            "p": 0.1,
        }
    )


def build(pm25: pd.DataFrame, meteo: pd.DataFrame) -> pd.DataFrame:
    return build_features(pm25, meteo, {"AAA": 1}, START, END).set_index("date")


class TestBuildFeatures(unittest.TestCase):
    def test_lags_rolling_and_target(self) -> None:
        table = build(synthetic_pm25(), synthetic_meteo())
        day = table.loc["2020-01-05"]
        self.assertEqual(day["pm25_mean"], 5)
        self.assertEqual(day["pm25_lag1"], 4)
        self.assertEqual(day["pm25_lag4"], 1)
        self.assertTrue(np.isnan(day["pm25_lag5"]))
        self.assertEqual(day["pm25_roll3_mean"], 4)
        self.assertEqual(day["pm25_diff1"], 1)
        self.assertEqual(day[TARGET], 6)
        self.assertEqual(day["target_day_of_week"], pd.Timestamp("2020-01-06").dayofweek)
        self.assertTrue(np.isnan(table.loc[END, TARGET]))

    def test_day_with_few_hours_has_no_mean(self) -> None:
        pm25 = synthetic_pm25()
        pm25.loc[pm25["fecha_hora"].between("2020-01-03 00:00", "2020-01-03 06:00"), "pm25"] = np.nan
        table = build(pm25, synthetic_meteo())
        self.assertTrue(np.isnan(table.loc["2020-01-03", "pm25_mean"]))
        self.assertTrue(np.isnan(table.loc["2020-01-02", TARGET]))
        self.assertTrue(np.isnan(table.loc["2020-01-04", "pm25_lag1"]))

    def test_no_information_from_the_target_day(self) -> None:
        """Cambiar todo lo observado el día d + 1 solo puede cambiar el target de d."""
        pm25, meteo = synthetic_pm25(), synthetic_meteo()
        base = build(pm25, meteo)
        next_day = pm25["fecha_hora"].dt.floor("D") == pd.Timestamp("2020-01-06")
        pm25.loc[next_day, "pm25"] = 99.0
        meteo.loc[meteo["fecha_hora"].dt.floor("D") == pd.Timestamp("2020-01-06"), ["t", "p"]] = [35.0, 9.0]
        changed = build(pm25, meteo)
        features = [c for c in base.columns if c != TARGET]
        pd.testing.assert_series_equal(base.loc["2020-01-05", features], changed.loc["2020-01-05", features])
        self.assertEqual(changed.loc["2020-01-05", TARGET], 99.0)

    def test_zero_pressure_and_three_day_rain(self) -> None:
        meteo = synthetic_meteo()
        meteo.loc[meteo["fecha_hora"].dt.floor("D") == pd.Timestamp("2020-01-04"), "pr"] = 0.0
        table = build(synthetic_pm25(), meteo)
        self.assertTrue(np.isnan(table.loc["2020-01-04", "pr"]))
        self.assertTrue(np.isnan(table.loc["2020-01-02", "p_sum3"]))
        self.assertAlmostEqual(table.loc["2020-01-03", "p_sum3"], 3 * 24 * 0.1)

    def test_feature_list_matches_columns(self) -> None:
        table = build(synthetic_pm25(), synthetic_meteo())
        self.assertTrue(set(PM25_FEATURES) <= set(table.columns))


if __name__ == "__main__":
    unittest.main()
