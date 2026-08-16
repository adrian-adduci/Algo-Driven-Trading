# Algorithmic Trading System

A Python implementation of three building blocks of an equity/options trading stack:
an exchange-style **order matching engine**, a **Black-Scholes options arbitrage**
strategy, and a **rolling-window ML pipeline** for short-horizon trade prediction.

Built as a portfolio/educational project. Every code sample below is executed
against the real API before being committed.

## Disclaimer

**Educational and research use only.**

- Does not connect to real brokers and does not execute real trades.
- No warranty. Trading involves substantial risk of loss.
- Past performance does not guarantee future results.

---

## Install

Requires Python 3.10+.

```bash
git clone https://github.com/adrian-adduci/Algo-Driven-Trading
cd Algo-Driven-Trading

python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -e ".[dev]"
```

Installing in editable mode puts the modules on your path, so the examples and
tests work from any directory.

## Run the tests

```bash
pytest
```

```
76 passed
```

Lint with `ruff check .`. CI runs both across Python 3.10–3.13 on every push.

## Run the examples

```bash
python examples/example_order_matching.py
python examples/example_simulated_broker.py
```

---

## 1. Order matching engine (`_order_management.py`)

Exchange-style limit order book with price-time priority. Supports limit,
market, and IOC orders, plus amend and cancel.

```python
import time
from _order_management import MatchingEngine, LimitOrder, MarketOrder, OrderSide

engine = MatchingEngine()

engine.handle_limit_order(LimitOrder(1, "AAPL", 100, 150.00, OrderSide.BUY, time.time()))
engine.handle_limit_order(LimitOrder(2, "AAPL", 50, 150.50, OrderSide.BUY, time.time()))

filled = engine.handle_market_order(MarketOrder(3, "AAPL", 60, OrderSide.SELL, time.time()))

for fill in filled:
    print(f"order {fill.id}: {fill.quantity} @ {fill.price}")

print(f"bid book depth: {len(engine.bid_book)}")

engine.amend_quantity(1, 40)     # reductions only
engine.cancel_order(1)
```

```
order 2: 50 @ 150.5
order 3: 10 @ 150.0
order 1: 10 @ 150.0
bid book depth: 1
```

**Reading the fill list.** `filled` records *both* sides of each trade — the
resting orders and the aggressor. The aggressor appears once, on the level that
fully consumes it, not once per level swept. To compute traded volume, filter by
order id or side rather than summing the whole list.

`handle_order(order)` dispatches to the right handler by order type and returns
the same fill list.

## 2. Options arbitrage (`_trade_data_management.py`)

Prices calls and puts with Black-Scholes, compares theoretical to quoted prices,
and builds delta-neutral positions hedged with the underlying.

```python
import _trade_data_management as tdm

time_to_expiry, market_data = tdm.read_data("tests/data/sample_market_data.csv")
option_names = tdm.get_list_of_all_instruments(market_data)
timestamp = market_data.index

market_data = tdm.set_tte_to_market_data(market_data, time_to_expiry)
option_values, option_deltas = tdm.create_df_to_store_options_values_delta(
    market_data, option_names
)
market_data = tdm.add_blacksholes_data_to_market_data(
    market_data, option_names, option_values, option_deltas
)

short_opps, long_opps = tdm.option_opportunities("C80", market_data)
print(f"C80: {len(short_opps)} short, {len(long_opps)} long opportunities")

positions = tdm.create_positions(market_data, option_names, timestamp)
trades, final_positions = tdm.create_orders(positions)
```

```
C80: 0 short, 0 long opportunities
```

**The bundled sample data contains no arbitrage.** It was generated under the
same Black-Scholes assumptions the strategy uses, so quoted and theoretical
prices agree and the strategy correctly does nothing. To see the strategy
trade, perturb an instrument's quotes — `tests/conftest.py` does exactly this
via the `mispriced_market_data_path` fixture.

Strategy parameters live at the top of the module:

| Constant | Default | Meaning |
|---|---|---|
| `ARBITRAGE_THRESHOLD` | `0.10` | Minimum edge in dollars before trading |
| `RISK_FREE_RATE` | `0.0` | Discount rate (flat) |
| `VOLATILITY` | `0.20` | Volatility assumption (flat) |

## 3. ML trade prediction (`_trade_management.py`)

Walk-forward model selection: for each rolling window, grid-search every
candidate model on the trailing `latest_sec` rows and score it on the next
`pred_sec` rows. Models never see their own test window during fitting.

```python
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from _trade_management import run_pipeline

models = {
    "RandomForestClassifier": RandomForestClassifier(random_state=0),
    "AdaBoostClassifier": AdaBoostClassifier(
        estimator=DecisionTreeClassifier(), n_estimators=10, random_state=0
    ),
}
grids = {
    "RandomForestClassifier": {"n_estimators": [10, 25], "max_depth": [3, 5]},
    "AdaBoostClassifier": {"estimator__max_depth": [1, 2]},
}

# `frame`: column '0' is the binary label, columns '1'..'64' are features.
selector = run_pipeline(models, grids, [frame], latest_sec=30, pred_sec=10, day=1)

print(selector.summary_day[0].to_string(index=False))

best = selector.summary_day[0].iloc[0]
print(f"best model: {best['Estimator']} (accuracy {best['Accuracy_mean']:.3f})")

top = selector.feature_importance["RandomForestClassifier"][0]
print("top features:", [name for name, _score in top])
```

```
             Estimator  Accuracy_mean  Accuracy_std  Accuracy_max  Accuracy_min  F_score
    AdaBoostClassifier            1.0      0.000000           1.0           1.0  1.00000
RandomForestClassifier            0.7      0.173205           0.8           0.5  0.62037

best model: AdaBoostClassifier (accuracy 1.000)
top features: ['1', '64', '11', '38', '42']
```

(That run uses synthetic data whose label is a direct function of feature `1`,
which is why AdaBoost scores 1.0. Do not read it as a performance claim.)

`feature_importance[model]` holds one ranked top-5 list per rolling window,
taken from `feature_importances_` for tree ensembles or `coef_` for linear
models. Estimators exposing neither (e.g. RBF-kernel SVC) are skipped.

## 4. Data and broker adapters

Abstract interfaces separating strategy code from data sources and execution
venues. Only the CSV data adapter and the simulated broker are implemented; the
rest are scaffolding for future work.

```python
from data_adapters import create_data_adapter
from broker_adapters import create_broker_adapter

data = create_data_adapter("csv", filename="tests/data/sample_market_data.csv")
data.connect()
quote = data.get_stock_quote("Stock")
print(f"stock bid {quote['bid_price']} / ask {quote['ask_price']}")
data.disconnect()

broker = create_broker_adapter("simulated")
broker.connect()
order_id = broker.submit_order(LimitOrder(1, "AAPL", 100, 150.00, OrderSide.BUY, time.time()))
print(broker.get_account_info()["cash"])
broker.disconnect()
```

```
stock bid 70.7 / ask 70.9
100000.0
```

---

## Data formats

### Options market data

```csv
Time,BidPrice-Stock,BidVolume-Stock,AskPrice-Stock,AskVolume-Stock,TimeToExpiry,BidPrice-P60,...
2018-01-01 00:05:00,70.7,120.0,70.9,120.0,0.9116,1.3,...
```

- `Time` — timestamp index
- `TimeToExpiry` — years to expiration
- `{Bid,Ask}{Price,Volume}-Stock` — underlying quotes
- `{Bid,Ask}{Price,Volume}-{Option}` — option quotes, where `{Option}` is
  `P##` (put, strike ##) or `C##` (call, strike ##)

A working 76-row example is at `tests/data/sample_market_data.csv`.

### ML training data

A DataFrame per trading day. Column `'0'` is the binary label; remaining columns
are numeric features. Needs at least `latest_sec + pred_sec` rows for one window.

---

## Project structure

```
Algo-Driven-Trading/
├── _order_management.py        # Matching engine, order types
├── _trade_data_management.py   # Black-Scholes, arbitrage, positions
├── _trade_management.py        # Rolling-window model selection
├── data_adapters.py            # Market data interfaces (CSV implemented)
├── broker_adapters.py          # Execution interfaces (simulated implemented)
├── config.yaml                 # Reference parameter values (NOT loaded at runtime)
├── .env.example                # Credential placeholders (NOT read at runtime)
├── pyproject.toml              # Dependencies, pytest and ruff config
├── examples/                   # Runnable demonstrations
├── tests/                      # pytest suite + sample market data
├── .github/workflows/ci.yml    # Lint + test on Python 3.10-3.13
├── CHANGELOG.md                # Version history
└── docs/
    ├── proposals/              # Designs for unbuilt work (crypto frontend)
    └── archive/                # Superseded status documents
```

Everything under `docs/proposals/` describes a planned web interface that **is
not implemented**. It is kept for design context, not as a description of this
codebase. See [docs/README.md](docs/README.md).

## Configuration

There is no config loader yet. **`config.yaml` and `.env.example` are reference
documents — no code reads either one.** Editing them changes nothing.

To change behaviour today, edit the named constants in the source:

| Setting | Where |
|---|---|
| Risk-free rate | `RISK_FREE_RATE` in `_trade_data_management.py` |
| Volatility | `VOLATILITY` in `_trade_data_management.py` |
| Arbitrage threshold | `ARBITRAGE_THRESHOLD` in `_trade_data_management.py` |
| Training / prediction window | `latest_sec` / `pred_sec` args to `run_pipeline()` |

Neither working integration (the CSV data adapter and the simulated broker)
requires credentials.

## Known limitations

Honest accounting of what this does not do:

1. **No live data or execution** — CSV in, simulated fills out.
2. **Flat rate and volatility** — no yield curve, no implied or historical vol.
3. **No transaction costs, slippage, or margin** — fills are frictionless.
4. **`create_orders` drops the opening row** (`positions.diff()[1:]`), so a
   position established at the first timestamp is never emitted as an order.
5. **`create_positions` requires both calls and puts** — it unconditionally
   sums a `Call Delta` and a `Put Delta` block, so an instrument universe
   containing only one kind raises `KeyError`.
6. **Single underlying** — the options module assumes one stock.
7. **No persistence** — order books are in-memory only.

### Previously listed, now fixed

- *Inner CV was not time-aware.* `GridSearchCV` now validates with
  `TimeSeriesSplit`, so hyperparameters are never tuned against rows that
  precede the rows the model trained on.
- *No feature scaling.* Scale-sensitive estimators (SVM, k-NN, linear models)
  are wrapped in a `StandardScaler` pipeline, so the scaler is refit per fold
  and never sees its own validation rows. Tree ensembles are left unwrapped,
  since they are scale-invariant.
- *`create_positions` used module-level globals.* Position state is now a
  local dict, so the module namespace stays clean and concurrent calls no
  longer share counters.

## References

- [Black-Scholes model](https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model)
- [scikit-learn](https://scikit-learn.org/stable/)
- Broker APIs: [Alpaca](https://alpaca.markets/docs/),
  [Interactive Brokers](https://interactivebrokers.github.io/tws-api/),
  [Polygon.io](https://polygon.io/docs/)

## License

MIT — see [LICENSE](LICENSE).
