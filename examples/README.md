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

## Future Examples (Coming Soon)

### 3. `example_options_arbitrage.py` (TODO)

Will demonstrate:
- Loading options market data from CSV
- Calculating Black-Scholes prices
- Finding arbitrage opportunities
- Generating delta-neutral positions
- Converting positions to orders

### 4. `example_ml_prediction.py` (TODO)

Will demonstrate:
- Preparing ML training data
- Training multiple models
- Hyperparameter tuning with GridSearchCV
- Model evaluation and comparison
- Feature importance analysis

### 5. `example_live_data_adapter.py` (TODO)

Will demonstrate (when live APIs are implemented):
- Connecting to market data providers
- Fetching real-time quotes
- Subscribing to data streams
- Historical data retrieval

### 6. `example_end_to_end_strategy.py` (TODO)

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

Make sure you've installed the required dependencies:

```bash
cd ..  # Back to root directory
pip install -r requirements.txt
```

### Running from Examples Directory

```bash
cd examples
python example_order_matching.py
python example_simulated_broker.py
```

### Running from Root Directory

```bash
python examples/example_order_matching.py
python examples/example_simulated_broker.py
```

---

## Creating Your Own Examples

Feel free to create your own example scripts! Here's a template:

```python
"""
Example: Your Example Name

Brief description of what this example demonstrates.
"""

import sys
sys.path.append('..')  # Add parent directory to path

# Your imports here
from _order_management import MatchingEngine
# etc.


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
- Run the unit tests: `python ../unit_test.py`
- Consult inline code documentation (docstrings)

---

Happy Trading! 📈
