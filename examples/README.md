# Examples Directory

This directory contains example scripts demonstrating how to use the algorithmic trading system.

## Available Examples

### 1. `example_order_matching.py`

Demonstrates the order matching engine functionality:
- Building order books with limit orders
- Executing market orders
- Handling IOC (Immediate-or-Cancel) orders
- Order amendment and cancellation
- Price-time priority matching

**To run:**
```bash
cd examples
python example_order_matching.py
```

**What you'll learn:**
- How to create different order types
- How the matching engine works
- Price-time priority algorithm
- Order lifecycle management

---

### 2. `example_simulated_broker.py`

Demonstrates the simulated broker adapter for paper trading:
- Connecting to the simulated broker
- Submitting orders and checking status
- Managing positions
- Modifying and cancelling orders
- Account information tracking

**To run:**
```bash
cd examples
python example_simulated_broker.py
```

**What you'll learn:**
- How to use broker adapters
- Paper trading workflow
- Position and account management
- Order status tracking

---

## Ideas for further examples

These are **not implemented** — they are a backlog, listed so the gaps are
visible. Nothing below exists in this directory.

### 3. `example_options_arbitrage.py` (not written)

Will demonstrate:
- Loading options market data from CSV
- Calculating Black-Scholes prices
- Finding arbitrage opportunities
- Generating delta-neutral positions
- Converting positions to orders

### 4. `example_ml_prediction.py` (not written)

Will demonstrate:
- Preparing ML training data
- Training multiple models
- Hyperparameter tuning with GridSearchCV
- Model evaluation and comparison
- Feature importance analysis

### 5. `example_live_data_adapter.py` (not written)

Will demonstrate (when live APIs are implemented):
- Connecting to market data providers
- Fetching real-time quotes
- Subscribing to data streams
- Historical data retrieval

### 6. `example_end_to_end_strategy.py` (not written)

Will demonstrate a complete trading workflow:
- Data ingestion
- Signal generation
- Risk management
- Order execution
- Position monitoring
- Performance tracking

---

## Running Examples

### Prerequisites

From the repository root:

```bash
pip install -e ".[dev]"
```

### Running

Both examples resolve the project root from their own file location, so they
run from any working directory:

```bash
python examples/example_order_matching.py      # from the repo root
```

```bash
cd examples && python example_order_matching.py   # or from in here
```

---

## Creating Your Own Examples

Here's a template:

```python
"""
Example: Your Example Name

Brief description of what this example demonstrates.
"""

import sys
from pathlib import Path

# Resolve the project root from this file's location. Do NOT use
# sys.path.append('..') -- that is relative to the *working directory*, so it
# only works when you happen to run the script from inside examples/.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from _order_management import MatchingEngine  # noqa: E402


def main():
    print("=" * 70)
    print("YOUR EXAMPLE NAME")
    print("=" * 70)
    print()

    # Your example code here

    print("Example complete!")
    print()


if __name__ == "__main__":
    main()
```

If you installed with `pip install -e .`, the `sys.path` block is unnecessary —
plain `from _order_management import ...` works. It is kept in the shipped
examples so they also run from a bare checkout.

---

## Notes

- All examples are self-contained and can be run independently
- Examples use simulated/demo data - no real trading occurs
- Examples are educational - adapt for your own use cases
- Check the main README.md for detailed API documentation

---

## Questions or Issues?

- Review the main [README.md](../README.md) for detailed documentation
- Check the [CHANGELOG.md](../CHANGELOG.md) for recent changes
- Run the test suite from the repository root: `pytest`
- Consult inline code documentation (docstrings)
