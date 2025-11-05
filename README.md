# Algorithmic Trading System

A modular Python-based algorithmic trading system featuring order matching simulation, Black-Scholes options pricing, and machine learning-based trade prediction.

## DISCLAIMER

**This system is for EDUCATIONAL and RESEARCH purposes only.**

- This software does NOT connect to real brokers or execute real trades
- No warranty is provided - use at your own risk
- Always test thoroughly with paper trading before considering live trading
- Trading involves substantial risk of loss
- Past performance does not guarantee future results

## Features

### 1. **Order Matching Engine** (`_order_management.py`)
- Simulates exchange-style order book with price-time priority
- Supports multiple order types:
  - **Limit Orders**: Execute at specified price or better
  - **Market Orders**: Execute immediately at best available price
  - **IOC Orders**: Immediate-or-cancel execution
- Full order lifecycle management (submit, amend, cancel)
- Maintains separate bid/ask books with automatic matching

### 2. **Options Arbitrage Trading** (`_trade_data_management.py`)
- Black-Scholes option pricing model implementation
- Greeks calculation (Delta, Vega)
- Statistical arbitrage strategy:
  - Identifies mispricing between market and theoretical prices
  - Generates delta-neutral positions
  - Automatic hedging with underlying stock
- Configurable arbitrage threshold ($0.10 default)

### 3. **Machine Learning Trade Prediction** (`_trade_management.py`)
- Multiple ML models with automated hyperparameter tuning:
  - Random Forest
  - Extra Trees
  - AdaBoost
  - Gradient Boosting
  - Support Vector Classifier (SVC)
- Rolling window training (30-second windows)
- GridSearchCV for parameter optimization
- Performance metrics: Accuracy, F1-score
- Feature importance analysis

### 4. **Integration Framework** (New)
- **Data Adapters** (`data_adapters.py`): Abstract interfaces for market data
- **Broker Adapters** (`broker_adapters.py`): Abstract interfaces for order execution
- **Configuration Management** (`config.yaml`): Centralized parameter control
- **Environment Variables** (`.env.example`): Secure credential management

## Project Structure

```
Algo-Driven-Trading/
├── _order_management.py          # Order matching engine
├── _trade_data_management.py     # Options pricing & arbitrage
├── _trade_management.py          # ML trade prediction
├── unit_test.py                  # Comprehensive unit tests
├── data_adapters.py              # Market data integration (NEW)
├── broker_adapters.py            # Broker integration (NEW)
├── config.yaml                   # System configuration (NEW)
├── .env.example                  # API credentials template (NEW)
├── requirements.txt              # Python dependencies (NEW)
├── README.md                     # This file (NEW)
└── CHANGELOG.md                  # Version history (NEW)
```

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Git (optional, for cloning)

### Step 1: Clone or Download

```bash
# Using Git
git clone <repository-url>
cd Algo-Driven-Trading

# Or download and extract the ZIP file
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configuration (Optional)

```bash
# Copy example configuration
cp .env.example .env

# Edit .env with your API keys (if planning to add live data)
# Note: Current implementation uses CSV files, not live APIs
```

## Usage

### 1. Order Matching Engine

```python
import time
from _order_management import (
    MatchingEngine, LimitOrder, MarketOrder, IOCOrder,
    OrderSide
)

# Create matching engine
engine = MatchingEngine()

# Submit a buy limit order
buy_order = LimitOrder(
    id=1,
    symbol="AAPL",
    quantity=100,
    price=150.50,
    side=OrderSide.BUY,
    time=time.time()
)

filled_orders = engine.handle_limit_order(buy_order)
print(f"Filled {len(filled_orders)} orders")

# Submit a sell limit order (will match if price crosses)
sell_order = LimitOrder(
    id=2,
    symbol="AAPL",
    quantity=50,
    price=150.00,
    side=OrderSide.SELL,
    time=time.time()
)

filled_orders = engine.handle_limit_order(sell_order)

# Submit market order
market_order = MarketOrder(
    id=3,
    symbol="AAPL",
    quantity=25,
    side=OrderSide.BUY,
    time=time.time()
)

filled_orders = engine.handle_market_order(market_order)

# Amend order quantity (reduce only)
engine.amend_quantity(order_id=1, quantity=50)

# Cancel order
engine.cancel_order(order_id=1)

# Check order books
print(f"Bid book depth: {len(engine.bid_book)}")
print(f"Ask book depth: {len(engine.ask_book)}")
```

### 2. Options Arbitrage Trading

```python
import _trade_data_management as tdm

# Step 1: Read market data from CSV
time_to_expiry, market_data = tdm.read_data('data/market_data.csv')

# CSV format required:
# Time, TimeToExpiry, BidPrice-Stock, BidVolume-Stock, AskPrice-Stock,
# AskVolume-Stock, BidPrice-P60, BidVolume-P60, AskPrice-P60, ...

# Step 2: Get option names
option_names = tdm.get_list_of_all_instruments(market_data)
print(f"Options found: {option_names}")  # e.g., ['P60', 'P70', 'C60', 'C70']

# Step 3: Add time-to-expiry to market data
market_data = tdm.set_tte_to_market_data(market_data, time_to_expiry)

# Step 4: Calculate Black-Scholes theoretical values
option_values, option_deltas = tdm.create_df_to_store_options_values_delta(
    market_data, option_names
)

# Step 5: Merge theoretical values into market data
market_data = tdm.add_blacksholes_data_to_market_data(
    market_data, option_names, option_values, option_deltas
)

# Step 6: Find arbitrage opportunities
short_opps, long_opps = tdm.option_opportunities('C60', market_data)
print(f"Found {len(short_opps)} short opportunities")
print(f"Found {len(long_opps)} long opportunities")

# Step 7: Generate delta-neutral positions
timestamp = market_data.index
positions = tdm.create_positions(market_data, option_names, timestamp)

# Step 8: Convert positions to executable orders
trades, final_positions = tdm.create_orders(positions)

print(f"Generated {len(trades)} trade signals")
print(f"\nFinal positions:")
print(final_positions)
```

### 3. Machine Learning Trade Prediction

```python
import pandas as pd
from _trade_management import Model_Selection

# Prepare data
# Format: Column 0 = label (0 or 1), Columns 1-64 = features
df = pd.read_csv('data/training_data.csv')

# Initialize model selection with multiple algorithms
ms = Model_Selection(df)

# Run full pipeline: train, tune, and evaluate all models
ms.pipeline(latest_sec=30, pred_sec=10, cv=2)

# Get performance summary
summary = ms.score_summary()

print("\nModel Performance Ranking:")
print(summary)

# Best model details
best_model = summary.iloc[0]
print(f"\nBest Model: {best_model['Model']}")
print(f"Test Accuracy: {best_model['Test Accuracy Mean']:.4f} ± {best_model['Test Accuracy Std']:.4f}")
print(f"F1 Score: {best_model['Test F1 Mean']:.4f}")

# Feature importance (for tree-based models)
if 'Feature Importance' in best_model:
    print(f"\nTop Features: {best_model['Feature Importance']}")
```

### 4. Using Data and Broker Adapters (New)

```python
from data_adapters import create_data_adapter, CSVDataAdapter
from broker_adapters import create_broker_adapter, SimulatedBrokerAdapter

# Create CSV data adapter
data_adapter = create_data_adapter('csv', filename='data/market_data.csv')
data_adapter.connect()

# Get stock quote
quote = data_adapter.get_stock_quote('Stock')
print(f"Bid: ${quote['bid_price']} Ask: ${quote['ask_price']}")

# Get options chain
options = data_adapter.get_options_chain('Stock', '2024-01-15')

data_adapter.disconnect()

# Create simulated broker
broker = create_broker_adapter('simulated')
broker.connect()

# Submit orders
from _order_management import LimitOrder, OrderSide
import time

order = LimitOrder(1, "AAPL", 100, 150.00, OrderSide.BUY, time.time())
order_id = broker.submit_order(order)
print(f"Order submitted: {order_id}")

# Check order status
status = broker.get_order_status(order_id)
print(f"Order status: {status}")

# Get positions
positions = broker.get_positions()
print(f"Current positions: {positions}")

# Get account info
account = broker.get_account_info()
print(f"Cash: ${account['cash']:.2f}")
print(f"Portfolio value: ${account['portfolio_value']:.2f}")

broker.disconnect()
```

## Running Tests

```bash
# Run all unit tests
python unit_test.py

# Expected output: OK (6 tests for each module)
```

The test suite covers:
- Order insertion and matching logic
- Market and IOC order handling
- Order amendments and cancellations
- Options data processing
- Black-Scholes calculations
- Arbitrage opportunity detection
- Position and order generation

## Configuration

### System Parameters (`config.yaml`)

```yaml
options:
  risk_free_rate: 0.0        # Currently hardcoded in code
  volatility: 0.20            # 20% volatility assumption
  arbitrage_threshold: 0.10   # $0.10 minimum price deviation

ml_trading:
  training_window_seconds: 30
  prediction_window_seconds: 10
  cv_folds: 2
  random_state: 42

order_management:
  min_order_quantity: 1
  price_tick_size: 0.01
  max_book_depth: 1000
```

Edit `config.yaml` to adjust system behavior. Note that some parameters are currently hardcoded in the source and will require code changes.

## Data Formats

### Market Data CSV Format (Options Trading)

```csv
Time,TimeToExpiry,BidPrice-Stock,BidVolume-Stock,AskPrice-Stock,AskVolume-Stock,BidPrice-P60,BidVolume-P60,AskPrice-P60,AskVolume-P60,...
1623456789,0.0833,70.25,100,70.30,150,0.50,50,0.55,75,...
```

**Required columns:**
- `Time`: Unix timestamp or datetime
- `TimeToExpiry`: Time to option expiration (years)
- `BidPrice-Stock`, `BidVolume-Stock`: Stock bid data
- `AskPrice-Stock`, `AskVolume-Stock`: Stock ask data
- `BidPrice-{Option}`, `BidVolume-{Option}`: Option bid data (e.g., P60, C70)
- `AskPrice-{Option}`, `AskVolume-{Option}`: Option ask data

**Option naming convention:**
- `P##`: Put option with strike price ## (e.g., P60 = Put $60 strike)
- `C##`: Call option with strike price ## (e.g., C70 = Call $70 strike)

### ML Training Data Format

```csv
Label,Feature1,Feature2,...,Feature64
0,0.512,1.234,...,0.892
1,-0.234,0.567,...,1.123
```

**Format:**
- First column: Binary label (0 or 1)
- Columns 1-64: Numeric features
- No header row required (or will be treated as data)

## Troubleshooting

### Common Issues

**1. ImportError: No module named 'scipy' / 'pandas' / 'sklearn'**
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**2. Order matching not working**
- **Fixed in this version**: The original code had a critical bug in `handle_order()` using `!=` instead of `==`
- Ensure you're using the updated `_order_management.py`

**3. cancel_order() not implemented**
- **Fixed in this version**: The method now properly removes orders from books

**4. Book sorting errors**
- **Fixed in this version**: Corrected book assignment bugs on lines 319 and 434

**5. "Risk-free rate is 0" warning**
- This is expected - risk-free rate is currently hardcoded to 0
- To change: Edit `_trade_data_management.py` line 289 (`r = 0`)

**6. "Volatility is fixed at 20%"**
- This is expected - volatility is currently hardcoded to 0.20
- To change: Edit `_trade_data_management.py` line 290 (`sigma = 0.20`)
- Future enhancement: Calculate historical volatility or use implied volatility

## Roadmap & Future Enhancements

### Priority 1: Core Improvements
- [ ] Externalize hardcoded parameters (risk-free rate, volatility) to `config.yaml`
- [ ] Add input validation and error handling
- [ ] Implement logging system
- [ ] Add data persistence (save/load order books)
- [ ] Calculate historical volatility from market data

### Priority 2: Live Trading Integration
- [ ] Implement Alpaca API adapter (stocks)
- [ ] Implement Interactive Brokers adapter (options)
- [ ] Add real-time data streaming
- [ ] Implement WebSocket connections
- [ ] Add paper trading mode

### Priority 3: Risk Management
- [ ] Position size limits
- [ ] Stop-loss orders
- [ ] Maximum drawdown monitoring
- [ ] Margin calculations
- [ ] Portfolio risk metrics (VaR, Sharpe ratio)

### Priority 4: Performance & Monitoring
- [ ] Database integration (PostgreSQL/TimescaleDB)
- [ ] Trade history tracking
- [ ] Performance analytics dashboard
- [ ] Backtesting framework
- [ ] Notification system (email, Slack)

### Priority 5: Advanced Features
- [ ] Additional option pricing models (Binomial, Monte Carlo)
- [ ] More Greeks (Gamma, Theta, Rho)
- [ ] Multi-leg option strategies (spreads, straddles)
- [ ] Order book visualization
- [ ] Deep learning models (LSTM, Transformers)

## Known Issues & Limitations

### Current Limitations

1. **No Live Data**: System only reads from CSV files
2. **No Order Execution**: No connection to real brokers
3. **Hardcoded Parameters**: Risk-free rate and volatility are fixed
4. **Simplified Risk Model**: No margin requirements or position limits
5. **No Persistence**: Order books cleared on restart
6. **Single Asset**: Options module designed for one underlying stock
7. **No Slippage Modeling**: Perfect execution assumed
8. **No Transaction Costs**: Commissions and fees not included

### Bugs Fixed in This Version

- ✅ Fixed critical order routing logic (lines 99-107 in `_order_management.py`)
- ✅ Implemented `cancel_order()` method
- ✅ Fixed book sorting bugs (lines 319, 434)
- ✅ Added comprehensive docstrings
- ✅ Created configuration framework
- ✅ Added API integration placeholders

## Additional Resources

### Learning Materials

- **Options Pricing**: [Black-Scholes Model](https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model)
- **Order Books**: [Understanding Market Microstructure](https://www.investopedia.com/terms/o/order-book.asp)
- **Machine Learning for Trading**: [scikit-learn documentation](https://scikit-learn.org/)

### API Documentation

- **Alpaca**: https://alpaca.markets/docs/
- **Interactive Brokers**: https://interactivebrokers.github.io/tws-api/
- **Polygon.io**: https://polygon.io/docs/
- **TD Ameritrade**: https://developer.tdameritrade.com/

### Python Libraries

- **pandas**: https://pandas.pydata.org/docs/
- **numpy**: https://numpy.org/doc/
- **scipy**: https://docs.scipy.org/doc/scipy/
- **scikit-learn**: https://scikit-learn.org/stable/

## Contributing

Contributions are welcome! Areas for improvement:

1. Bug fixes and code optimization
2. Additional ML models and features
3. Live broker integrations
4. Documentation improvements
5. Test coverage expansion
6. Performance benchmarking

## License

This project is provided as-is for educational purposes. Check the repository for specific license terms.

## Security Note

- **Never commit API keys or credentials** to version control
- Use `.env` file for sensitive data (included in `.gitignore`)
- Enable 2FA on all trading accounts
- Test thoroughly with paper trading before live trading
- Monitor positions and set appropriate risk limits

## Performance Tips

1. **Data Loading**: Cache CSV data to avoid repeated reads
2. **ML Training**: Use smaller `cv` parameter for faster GridSearch
3. **Order Matching**: Pre-sort order books only when needed
4. **Memory Usage**: Process data in chunks for large datasets
5. **Parallelization**: Run ML models in parallel using `n_jobs=-1`

## Support

For issues, questions, or suggestions:
- Check existing GitHub issues
- Review the troubleshooting section
- Consult the inline code documentation
- Test with the included unit tests

## Version

**Current Version**: 1.1.0 (See [CHANGELOG.md](CHANGELOG.md) for details)

---

**Remember**: This is a research and educational tool. Always practice responsible trading and risk management.
