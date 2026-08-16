"""Shared pytest fixtures.

The market-data fixture replaces the ~78-line CSV string that used to be
embedded directly in the old ``unit_test.py``. Keeping it on disk means the
sample data is inspectable, diffable, and usable from the examples too.
"""

import sys
from pathlib import Path

import pandas as pd
import pytest

# Allow `pytest` to work from a clean clone without `pip install -e .` first.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

DATA_DIR = Path(__file__).parent / "data"


@pytest.fixture
def market_data_path():
    """Path to the sample options market-data CSV."""
    return DATA_DIR / "sample_market_data.csv"


@pytest.fixture
def raw_market_data(market_data_path):
    """The ``(time_to_expiry, market_data)`` pair straight out of ``read_data``."""
    import _trade_data_management as tdm

    return tdm.read_data(market_data_path)


@pytest.fixture
def option_names(raw_market_data):
    """Option instrument names present in the sample data, e.g. ``['P60', ...]``."""
    import _trade_data_management as tdm

    _, market_data = raw_market_data
    return tdm.get_list_of_all_instruments(market_data)


@pytest.fixture
def enriched_market_data(raw_market_data, option_names):
    """Market data re-indexed by time-to-expiry with Black-Scholes columns merged in.

    This is the six-step setup that the old test file copy-pasted into eight
    separate test methods.
    """
    import _trade_data_management as tdm

    time_to_expiry, market_data = raw_market_data
    market_data = tdm.set_tte_to_market_data(market_data, time_to_expiry)
    option_values, option_deltas = tdm.create_df_to_store_options_values_delta(
        market_data, option_names
    )
    return tdm.add_blacksholes_data_to_market_data(
        market_data, option_names, option_values, option_deltas
    )


@pytest.fixture
def mispriced_market_data_path(market_data_path, tmp_path):
    """Sample data with C80 quotes shifted well away from their theoretical value.

    The bundled sample was generated from the same Black-Scholes assumptions the
    strategy uses, so market and theoretical prices agree and *no* arbitrage is
    ever detected. Perturbing one instrument is what actually exercises the
    opportunity-detection and position-building code paths.
    """
    frame = pd.read_csv(market_data_path)
    frame["BidPrice-C80"] = frame["BidPrice-C80"] + 1.5
    frame["AskPrice-C80"] = frame["AskPrice-C80"] + 1.5

    out = tmp_path / "mispriced_market_data.csv"
    frame.to_csv(out, index=False)
    return out


@pytest.fixture
def ml_training_frame():
    """A deterministic label-plus-64-features frame shaped like the ML pipeline expects.

    Column ``'0'`` is the binary label; columns ``'1'``..``'64'`` are features.
    Row count covers two rolling windows (30 train + 10 predict, stepped by 10).
    """
    import numpy as np

    rng = np.random.default_rng(42)
    n_rows, n_features = 60, 64
    features = rng.normal(size=(n_rows, n_features))
    # Make the label weakly learnable rather than pure noise, so the models
    # produce meaningful (not degenerate) accuracy numbers.
    labels = (features[:, 0] + 0.5 * features[:, 1] > 0).astype(int)

    frame = pd.DataFrame(features, columns=[str(i) for i in range(1, n_features + 1)])
    frame.insert(0, "0", labels)
    return frame
