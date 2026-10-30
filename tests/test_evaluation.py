import unittest

import numpy as np
import pandas as pd

from src.models import regression_metrics, rolling_origin_predictions, threshold_for_budget, warning_metrics


class TestEvaluation(unittest.TestCase):
    def test_rolling_origin_trains_only_on_previous_years(self) -> None:
        data = pd.DataFrame({"year": [2019, 2019, 2020, 2020, 2021], "y": [1.0, 2.0, 3.0, 4.0, 5.0]})
        seen = {}

        def fit_predict(train: pd.DataFrame, test: pd.DataFrame) -> np.ndarray:
            seen[int(test["year"].iloc[0])] = sorted(train["year"].unique())
            return np.full(len(test), train["y"].mean())

        predictions = rolling_origin_predictions(data, [2020, 2021], fit_predict)
        self.assertEqual(seen, {2020: [2019], 2021: [2019, 2020]})
        self.assertEqual(predictions.loc[2], 1.5)
        self.assertEqual(predictions.loc[4], 2.5)

    def test_threshold_for_budget_matches_number_of_events(self) -> None:
        y_true = pd.Series([10, 40, 50, 20, 39])
        y_pred = pd.Series([30, 36, 45, 25, 34])
        threshold = threshold_for_budget(y_true, y_pred)
        self.assertEqual(threshold, 34)
        self.assertEqual(int((y_pred >= threshold).sum()), int((y_true >= 38).sum()))

    def test_warning_metrics_and_starts(self) -> None:
        y_true = pd.Series([40.0, 40.0, 10.0, 39.0])
        y_pred = pd.Series([39.0, 20.0, 38.0, 38.5])
        starts = pd.Series([True, False, False, False])
        result = warning_metrics(y_true, y_pred, starts, alert_threshold=38)
        self.assertEqual(result["eventos"], 3)
        self.assertEqual(result["avisos"], 3)
        self.assertAlmostEqual(result["precision"], 2 / 3)
        self.assertAlmostEqual(result["recall"], 2 / 3)
        self.assertEqual(result["inicios_avisados"], 1)

    def test_regression_metrics(self) -> None:
        result = regression_metrics(pd.Series([1.0, 2.0, 3.0]), pd.Series([1.0, 2.0, 5.0]))
        self.assertAlmostEqual(result["MAE"], 2 / 3)
        self.assertAlmostEqual(result["R2"], 1 - 4 / 2)


if __name__ == "__main__":
    unittest.main()
