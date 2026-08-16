"""Rolling-window model selection for short-horizon trade prediction.

The pipeline walks forward through time: for each window it tunes every
candidate model on the most recent `latest_sec` rows, then scores it on the
next `pred_sec` rows. Models never see their own test window during fitting.

Input data is a list of DataFrames, one per trading day. In each DataFrame
column ``'0'`` is the binary label and the remaining columns are features.
"""

import statistics

import pandas as pd
from sklearn import metrics
from sklearn.base import clone
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

LABEL_COLUMN = "0"

#: Name of the estimator step inside a scaling pipeline. Caller-supplied grid
#: keys are rewritten into this namespace, so callers never see it.
MODEL_STEP = "model"
SCALER_STEP = "scaler"

SUMMARY_COLUMNS = [
    "Estimator",
    "Accuracy_mean",
    "Accuracy_std",
    "Accuracy_max",
    "Accuracy_min",
    "F_score",
]


def needs_scaling(estimator):
    """Whether an estimator's results depend on feature magnitude.

    Tree ensembles split on thresholds within a single feature at a time, so
    rescaling cannot change which split is chosen -- scaling them is pure
    overhead. Distance- and margin-based methods (SVMs, k-NN, and any linear
    model with a regularisation penalty) are dominated by whichever feature
    happens to carry the largest units unless the features are standardised.

    Detection is by defining module rather than by capability, because the
    capability checks that would seem natural do not work on an *unfitted*
    estimator: ``feature_importances_`` is a property that raises
    NotFittedError, so ``hasattr`` reports False for a tree ensemble that has
    not been fit yet.

    Anything already wrapped in a Pipeline is left alone -- the caller has
    taken responsibility for preprocessing.
    """
    if isinstance(estimator, Pipeline):
        return False
    module = type(estimator).__module__
    return module.startswith(("sklearn.svm", "sklearn.neighbors", "sklearn.linear_model"))


class Model_Selection:
    """Grid-search several classifiers across rolling train/test windows."""

    def __init__(self, models, model_grid_params, data, latest_sec, pred_sec, day):
        self.models = models
        self.model_grid = model_grid_params
        self.data = data
        self.latest_sec = latest_sec
        self.pred_sec = pred_sec
        self.day = day
        self.keys = models.keys()
        self.best_score = {}
        self.grid = {}
        self.predict_values = {}
        self.cv_acc = {}
        self.acc = {}
        self.fscore = {}
        self.true_values = {}
        self.feature_importance = {}
        self.predict_values_day = {}
        self.cv_acc_day = {}
        self.acc_day = {}
        self.fscore_day = {}
        self.true_values_day = {}
        self.summary_day = []
        self.cv = 2
        #: Wrap scale-sensitive estimators in a StandardScaler pipeline.
        #: Set False to reproduce the previous unscaled behaviour.
        self.scale_features = True

    def Grid_fit(self, X_train, y_train, cv=2, scoring="accuracy"):
        """Tune hyperparameters for every model on the current training window.

        The search validates with TimeSeriesSplit. The rows in a window are
        sequential observations, and the default K-fold that GridSearchCV
        would otherwise use selects validation rows interleaved with training
        rows -- so a model could be tuned against data that precedes what it
        trained on.
        """
        self.cv = cv
        splitter = TimeSeriesSplit(n_splits=cv)

        for key in self.keys:
            estimator, param_grid = self._prepare(self.models[key], self.model_grid[key])
            grid = GridSearchCV(estimator, param_grid, cv=splitter, scoring=scoring)
            grid.fit(X_train, y_train)
            self.grid[key] = grid
            self.cv_acc[key].append(grid.best_score_)

    def _prepare(self, model, param_grid):
        """Return the estimator to search over, plus its grid.

        Scale-sensitive estimators are wrapped in a Pipeline with a
        StandardScaler. Wrapping (rather than scaling X_train up front) is
        what keeps the scaler honest: GridSearchCV refits every pipeline step
        on each fold's training rows, so the scaler never sees the fold's
        validation rows. Fitting a scaler on the whole window would leak its
        range into the validation scores.

        Caller grids stay in the estimator's own namespace; keys are rewritten
        into the pipeline's namespace here.
        """
        if not (self.scale_features and needs_scaling(model)):
            return model, param_grid

        pipeline = Pipeline(
            [(SCALER_STEP, StandardScaler()), (MODEL_STEP, clone(model))]
        )
        return pipeline, _prefix_grid(param_grid, MODEL_STEP)

    def model_fit(self, X_train, y_train, X_test, y_test):
        """Refit each model with its best parameters and score it on the test window."""
        for key in self.keys:
            # clone() so the search's own fitted estimator is left untouched
            # and each window starts from a fresh, unfitted model.
            model = clone(self.grid[key].estimator)
            model.set_params(**self.grid[key].best_params_)
            model.fit(X_train, y_train)
            predictions = model.predict(X_test)

            self.predict_values[key].append(predictions.tolist())
            self.true_values[key].append(y_test.tolist())
            self.acc[key].append(metrics.accuracy_score(y_test, predictions))
            self.fscore[key].append(metrics.f1_score(y_test, predictions, zero_division=0))

            top_features = self._top_features(model, X_train.columns)
            if top_features is not None:
                self.feature_importance.setdefault(key, []).append(top_features)

    @staticmethod
    def _top_features(model, feature_names, n=5):
        """Return the ``n`` highest-scoring features, or None if unavailable.

        Tree ensembles expose ``feature_importances_``; linear models expose
        ``coef_``. Kernel SVMs expose neither, so they are skipped rather than
        special-cased by estimator name.
        """
        # Unwrap the scaling pipeline so importances resolve on the estimator
        # itself. Scaling preserves feature order, so the names still line up.
        if isinstance(model, Pipeline):
            model = model.named_steps[MODEL_STEP]

        if hasattr(model, "feature_importances_"):
            scores = model.feature_importances_
        elif hasattr(model, "coef_"):
            scores = model.coef_[0]
        else:
            return None

        ranked = sorted(
            zip(feature_names, scores, strict=False), key=lambda pair: pair[1], reverse=True
        )
        return ranked[:n]

    def pipeline(self):
        """Run the full walk-forward evaluation across every day of data."""
        self.set_list_day()

        for day in range(0, self.day, 1):
            self.set_list()
            day_data = self.data[day]

            for i in self._window_starts(len(day_data)):
                data_train = day_data[i : i + self.latest_sec]
                X_train = data_train.drop([LABEL_COLUMN], axis=1)
                y_train = data_train[LABEL_COLUMN]

                data_test = day_data[
                    i + self.latest_sec : i + self.latest_sec + self.pred_sec
                ]
                X_test = data_test.drop([LABEL_COLUMN], axis=1)
                y_test = data_test[LABEL_COLUMN]

                self.Grid_fit(X_train, y_train, cv=self.cv, scoring="accuracy")
                self.model_fit(X_train, y_train, X_test, y_test)

            for key in self.keys:
                self.cv_acc_day[key].append(self.cv_acc[key])
                self.acc_day[key].append(self.acc[key])
                self.fscore_day[key].append(self.fscore[key])
                self.true_values_day[key].append(self.true_values[key])
                self.predict_values_day[key].append(self.predict_values[key])

            self.summary_day.append(self.score_summary(sort_by="Accuracy_mean"))

    def _window_starts(self, n_rows):
        """Start offsets for every complete train+test window that fits in the data.

        Derived from the data length rather than hardcoded, so the pipeline
        scales to datasets of any size.
        """
        last_start = n_rows - self.latest_sec - self.pred_sec
        if last_start < 0:
            raise ValueError(
                f"need at least {self.latest_sec + self.pred_sec} rows for one window, "
                f"got {n_rows}"
            )
        return range(0, last_start + 1, self.pred_sec)

    def set_list(self):
        """Reset the per-day statistic accumulators."""
        for key in self.keys:
            self.predict_values[key] = []
            self.cv_acc[key] = []
            self.acc[key] = []
            self.fscore[key] = []
            self.true_values[key] = []

    def set_list_day(self):
        """Reset the across-all-days statistic accumulators."""
        for key in self.keys:
            self.predict_values_day[key] = []
            self.cv_acc_day[key] = []
            self.acc_day[key] = []
            self.fscore_day[key] = []
            self.true_values_day[key] = []

    def score_summary(self, sort_by="Accuracy_mean"):
        """Rank the models by their accuracy across this day's rolling windows.

        Returns a DataFrame with one row per estimator, e.g.::

                             Estimator  Accuracy_mean  Accuracy_std  ...
            Ranking
            0   RandomForestClassifier           0.65          0.35
            1     ExtraTreesClassifier           0.65          0.35
        """
        rows = [
            {
                "Estimator": key,
                "Accuracy_mean": statistics.mean(self.acc[key]),
                "Accuracy_std": _stdev(self.acc[key]),
                "Accuracy_max": max(self.acc[key]),
                "Accuracy_min": min(self.acc[key]),
                "F_score": statistics.mean(self.fscore[key]),
            }
            for key in self.acc
        ]

        summary = pd.DataFrame(rows, columns=SUMMARY_COLUMNS)
        summary.index.rename("Ranking", inplace=True)
        return summary.sort_values(by=[sort_by], ascending=False)


def _prefix_grid(param_grid, step):
    """Rewrite grid keys into a pipeline step's namespace (``C`` -> ``model__C``).

    Accepts either a dict or a list of dicts, matching what GridSearchCV takes.
    Keys already addressing a pipeline step are left alone.
    """
    prefix = f"{step}__"

    def rewrite(grid):
        return {
            key if key.startswith(prefix) else prefix + key: value
            for key, value in grid.items()
        }

    if isinstance(param_grid, (list, tuple)):
        return [rewrite(grid) for grid in param_grid]
    return rewrite(param_grid)


def _stdev(values):
    """Sample standard deviation, defined as 0.0 for a single observation.

    `statistics.stdev` raises StatisticsError on one sample, which would
    otherwise crash the summary whenever the data yields a single window.
    """
    return statistics.stdev(values) if len(values) > 1 else 0.0


def run_pipeline(models, model_grid_params, data, latest_sec=30, pred_sec=10, day=1):
    """Build a Model_Selection, run the pipeline, and return the fitted object."""
    selector = Model_Selection(models, model_grid_params, data, latest_sec, pred_sec, day)
    selector.pipeline()
    return selector
