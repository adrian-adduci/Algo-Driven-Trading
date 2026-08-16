"""Tests for the rolling-window model selection pipeline."""

import pytest
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

from _trade_management import Model_Selection, run_pipeline

SUMMARY_COLUMNS = [
    "Estimator",
    "Accuracy_mean",
    "Accuracy_std",
    "Accuracy_max",
    "Accuracy_min",
    "F_score",
]


@pytest.fixture
def models():
    return {
        "RandomForestClassifier": RandomForestClassifier(random_state=0),
        "AdaBoostClassifier": AdaBoostClassifier(
            estimator=DecisionTreeClassifier(), n_estimators=5, random_state=0
        ),
    }


@pytest.fixture
def grids():
    return {
        "RandomForestClassifier": {"n_estimators": [5], "max_depth": [3]},
        "AdaBoostClassifier": {"estimator__max_depth": [1, 2]},
    }


@pytest.fixture
def selector(models, grids, ml_training_frame):
    return Model_Selection(models, grids, [ml_training_frame], 30, 10, 1)


class TestModernSklearnCompatibility:
    def test_adaboost_accepts_the_estimator_keyword(self):
        """`base_estimator` was removed in scikit-learn 1.4."""
        clf = AdaBoostClassifier(estimator=DecisionTreeClassifier(), n_estimators=5)

        assert clf.estimator is not None


class TestInitialState:
    def test_starts_with_no_fitted_grids(self, selector):
        assert selector.grid == {}

    def test_starts_with_no_per_day_results(self, selector):
        assert selector.true_values_day == {}


class TestPipeline:
    def test_produces_one_summary_per_day(self, selector):
        selector.pipeline()

        assert len(selector.summary_day) == 1

    def test_summary_has_the_documented_columns(self, selector):
        selector.pipeline()

        assert list(selector.summary_day[0].columns) == SUMMARY_COLUMNS

    def test_summary_covers_every_model(self, selector, models):
        selector.pipeline()

        assert set(selector.summary_day[0]["Estimator"]) == set(models)

    def test_summary_is_sorted_by_the_requested_column(self, selector):
        selector.pipeline()
        summary = selector.summary_day[0]

        assert list(summary["Accuracy_mean"]) == sorted(summary["Accuracy_mean"], reverse=True)

    def test_accuracies_are_valid_probabilities(self, selector):
        selector.pipeline()

        for key in selector.acc:
            assert all(0.0 <= a <= 1.0 for a in selector.acc[key])

    def test_records_a_prediction_set_per_rolling_window(self, selector):
        selector.pipeline()

        for key in selector.predict_values:
            assert len(selector.predict_values[key]) == len(selector.acc[key])

    def test_uses_all_available_rolling_windows(self, selector, ml_training_frame):
        """Regression: the window loop was hardcoded to `range(0, 20, pred_sec)`,
        so it ignored everything past row 20 regardless of dataset size."""
        selector.pipeline()

        expected = len(range(0, len(ml_training_frame) - 30 - 10 + 1, 10))
        assert len(selector.acc["RandomForestClassifier"]) == expected


class TestFeatureImportance:
    def test_feature_importance_is_retained(self, selector):
        """Regression: importances were computed into a local and discarded,
        while the README advertised reading them back."""
        selector.pipeline()

        assert selector.feature_importance, "no feature importances were stored"
        assert "RandomForestClassifier" in selector.feature_importance

    def test_reports_the_top_five_features(self, selector):
        selector.pipeline()

        top = selector.feature_importance["RandomForestClassifier"][0]
        assert len(top) == 5

    def test_importances_are_sorted_descending(self, selector):
        selector.pipeline()

        top = selector.feature_importance["RandomForestClassifier"][0]
        scores = [score for _, score in top]
        assert scores == sorted(scores, reverse=True)

    def test_reported_features_are_real_feature_columns(self, selector, ml_training_frame):
        selector.pipeline()

        feature_columns = set(ml_training_frame.columns) - {"0"}
        for _key, importances in selector.feature_importance.items():
            for window in importances:
                for name, _score in window:
                    assert name in feature_columns


class TestSingleWindowStability:
    def test_summary_survives_a_single_rolling_window(self, models, grids, ml_training_frame):
        """Regression: `statistics.stdev` raises StatisticsError on one sample."""
        short = ml_training_frame.iloc[:40]
        selector = Model_Selection(models, grids, [short], 30, 10, 1)

        selector.pipeline()
        summary = selector.summary_day[0]

        assert len(selector.acc["RandomForestClassifier"]) == 1
        assert summary["Accuracy_std"].notna().all()
        assert (summary["Accuracy_std"] == 0).all()


class TestRunPipelineHelper:
    def test_returns_a_populated_selector(self, models, grids, ml_training_frame):
        selector = run_pipeline(
            models, grids, [ml_training_frame], latest_sec=30, pred_sec=10, day=1
        )

        assert list(selector.summary_day[0].columns) == SUMMARY_COLUMNS
