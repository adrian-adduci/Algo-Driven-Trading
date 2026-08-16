"""Tests for the statistical rigor of the model-selection pipeline.

Two properties matter here and neither is visible in an accuracy number:

1. Hyperparameter search on time-ordered data must not validate on rows that
   precede the rows it trained on.
2. Scale-sensitive estimators must be scaled, and the scaler must be fit
   inside each fold rather than across the whole window.
"""

import numpy as np
import pytest
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import TimeSeriesSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

from _trade_management import Model_Selection, needs_scaling


@pytest.fixture
def wide_scale_frame(ml_training_frame):
    """Same frame, but with feature magnitudes spread across many orders."""
    frame = ml_training_frame.copy()
    for i, col in enumerate(c for c in frame.columns if c != "0"):
        frame[col] = frame[col] * (10 ** (i % 6))
    return frame


class TestTimeAwareCrossValidation:
    def test_grid_search_uses_time_series_split(self, ml_training_frame):
        """Regression: GridSearchCV used default K-fold on time-ordered rows."""
        models = {"rf": RandomForestClassifier(random_state=0, n_estimators=5)}
        grids = {"rf": {"max_depth": [2]}}
        selector = Model_Selection(models, grids, [ml_training_frame], 30, 10, 1)

        selector.pipeline()

        cv = selector.grid["rf"].cv
        assert isinstance(cv, TimeSeriesSplit), f"expected TimeSeriesSplit, got {cv!r}"

    def test_validation_folds_never_precede_their_training_rows(self, ml_training_frame):
        """The defining property of a time-aware split."""
        models = {"rf": RandomForestClassifier(random_state=0, n_estimators=5)}
        grids = {"rf": {"max_depth": [2]}}
        selector = Model_Selection(models, grids, [ml_training_frame], 30, 10, 1)
        selector.pipeline()

        cv = selector.grid["rf"].cv
        for train_idx, test_idx in cv.split(np.zeros((30, 1))):
            assert train_idx.max() < test_idx.min(), (
                "a validation row precedes a training row: lookahead in tuning"
            )

    def test_split_count_follows_the_requested_cv(self, ml_training_frame):
        models = {"rf": RandomForestClassifier(random_state=0, n_estimators=5)}
        grids = {"rf": {"max_depth": [2]}}
        selector = Model_Selection(models, grids, [ml_training_frame], 30, 10, 1)
        selector.cv = 3

        selector.pipeline()

        assert selector.grid["rf"].cv.get_n_splits() == 3


class TestScaleSensitiveEstimators:
    def test_needs_scaling_flags_distance_based_models(self):
        assert needs_scaling(SVC()) is True

    def test_needs_scaling_exempts_tree_ensembles(self):
        assert needs_scaling(RandomForestClassifier()) is False

    def test_svc_is_wrapped_in_a_scaling_pipeline(self, ml_training_frame):
        models = {"svc": SVC(random_state=0)}
        grids = {"svc": {"C": [1.0]}}
        selector = Model_Selection(models, grids, [ml_training_frame], 30, 10, 1)

        selector.pipeline()

        estimator = selector.grid["svc"].estimator
        assert isinstance(estimator, Pipeline)
        assert isinstance(estimator.named_steps["scaler"], StandardScaler)

    def test_tree_models_are_not_wrapped(self, ml_training_frame):
        """Scaling a tree ensemble is pure overhead; it must be skipped."""
        models = {"rf": RandomForestClassifier(random_state=0, n_estimators=5)}
        grids = {"rf": {"max_depth": [2]}}
        selector = Model_Selection(models, grids, [ml_training_frame], 30, 10, 1)

        selector.pipeline()

        assert not isinstance(selector.grid["rf"].estimator, Pipeline)

    def test_caller_grids_need_no_pipeline_prefix(self, ml_training_frame):
        """The wrapping is internal: callers still pass plain parameter names."""
        models = {"svc": SVC(random_state=0)}
        grids = {"svc": {"C": [0.5, 1.0]}}
        selector = Model_Selection(models, grids, [ml_training_frame], 30, 10, 1)

        selector.pipeline()

        # Translated internally to the pipeline's namespace.
        assert "model__C" in selector.grid["svc"].param_grid
        assert selector.grid["svc"].best_params_["model__C"] in (0.5, 1.0)

    def test_scaling_lifts_svc_on_badly_scaled_features(self, wide_scale_frame):
        """The point of the change: an unscaled RBF SVC is crippled here."""
        models = {"svc": SVC(random_state=0)}
        grids = {"svc": {"C": [1.0]}}

        scaled = Model_Selection(models, grids, [wide_scale_frame], 30, 10, 1)
        scaled.pipeline()

        unscaled = Model_Selection(
            {"svc": SVC(random_state=0)}, {"svc": {"C": [1.0]}},
            [wide_scale_frame], 30, 10, 1,
        )
        unscaled.scale_features = False
        unscaled.pipeline()

        scaled_acc = sum(scaled.acc["svc"]) / len(scaled.acc["svc"])
        unscaled_acc = sum(unscaled.acc["svc"]) / len(unscaled.acc["svc"])
        assert scaled_acc >= unscaled_acc


class TestNoScalerLeakage:
    def test_scaler_is_fit_inside_the_estimator_not_on_the_window(self, ml_training_frame):
        """A scaler fit outside the pipeline would see validation rows.

        Wrapping the scaler in the estimator means GridSearchCV refits it on
        each fold's training rows only. This asserts the scaler is a pipeline
        step rather than something applied to X_train beforehand.
        """
        models = {"svc": SVC(random_state=0)}
        grids = {"svc": {"C": [1.0]}}
        selector = Model_Selection(models, grids, [ml_training_frame], 30, 10, 1)

        selector.pipeline()

        best = selector.grid["svc"].best_estimator_
        assert isinstance(best, Pipeline)
        assert isinstance(best.named_steps["scaler"], StandardScaler)

    def test_feature_importance_still_resolves_through_the_pipeline(
        self, ml_training_frame
    ):
        """Wrapping must not hide feature_importances_ / coef_."""
        models = {"svc": SVC(random_state=0, kernel="linear")}
        grids = {"svc": {"C": [1.0]}}
        selector = Model_Selection(models, grids, [ml_training_frame], 30, 10, 1)

        selector.pipeline()

        top = selector.feature_importance["svc"][0]
        assert len(top) == 5
        feature_columns = set(ml_training_frame.columns) - {"0"}
        for name, _score in top:
            assert name in feature_columns
