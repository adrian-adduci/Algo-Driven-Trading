# Crypto Trading Platform - Complete User Guide

> **⚠️ This describes a product that does not exist.**
>
> There is no web interface, no crypto integration, no bot runner, and no user
> accounts in this repository. This is a **design document** — written as a
> user guide for a proposed platform — and is the companion to
> [CRYPTO_FRONTEND_PLAN.md](CRYPTO_FRONTEND_PLAN.md).
>
> Every screen, button, and workflow below is aspirational. Read it as a
> product specification, not as instructions you can follow.
>
> For what the code actually does today, see [README.md](../../README.md):
> an order matching engine, a Black-Scholes options arbitrage strategy, and a
> rolling-window ML pipeline — all Python libraries with no UI, operating on
> equities and options rather than crypto.

**Version:** 1.0 (design draft)
**Date:** January 9, 2026
**Status:** Not implemented

---

## Table of Contents

1. [System Overview](#system-overview)
2. [User Personas & Use Cases](#user-personas--use-cases)
3. [Getting Started](#getting-started)
4. [Trading Control Features](#trading-control-features)
5. [Research & Analysis Features](#research--analysis-features)
6. [Automated Trading (Bots)](#automated-trading-bots)
7. [Complete User Workflows](#complete-user-workflows)
8. [Interface Walkthrough](#interface-walkthrough)

---

## System Overview

### What This System Does

This platform provides **BOTH** trading control and research capabilities:

✅ **Trading Control:**
- Manual trade execution (buy/sell)
- Automated trading bots
- Portfolio management
- Risk management
- Order management (create, modify, cancel)

✅ **Research & Analysis:**
- Real-time market data analysis
- Historical price charts
- ML model predictions
- Performance analytics
- Backtesting strategies
- Market screening & discovery

### Dual-Mode Operation

The system operates in **two complementary modes**:

1. **Active Trading Mode:** Execute trades manually or via bots
2. **Research Mode:** Analyze markets, backtest strategies, review performance (read-only)

Users can seamlessly switch between modes or use both simultaneously.

---

## User Personas & Use Cases

### 👨‍💼 Persona 1: The Active Trader

**Goal:** Execute trades quickly based on market opportunities

**Uses the system to:**
- Monitor multiple crypto pairs in real-time
- Place market and limit orders rapidly
- Track open positions and P&L
- Set stop-losses and take-profits
- Receive price alerts

**Primary Features:**
- Trading interface
- Real-time charts
- Order book
- Quick trade buttons

---

### 📊 Persona 2: The Algorithm Developer

**Goal:** Research and develop profitable trading strategies

**Uses the system to:**
- Backtest ML models on historical data
- Analyze feature importance
- Compare strategy performance
- Optimize parameters
- Paper trade before going live

**Primary Features:**
- Analytics dashboard
- Backtesting engine
- ML model insights
- Performance metrics

---

### 🤖 Persona 3: The Bot Operator

**Goal:** Run automated strategies while monitoring performance

**Uses the system to:**
- Configure and launch trading bots
- Monitor bot performance
- Adjust parameters dynamically
- Review bot trade history
- Set risk limits

**Primary Features:**
- Bot management interface
- Strategy templates
- Performance tracking
- Alert system

---

### 🔬 Persona 4: The Market Researcher

**Goal:** Understand market dynamics and discover opportunities

**Uses the system to:**
- Screen coins by volume, volatility, momentum
- Analyze correlations between assets
- Study order book depth
- Identify arbitrage opportunities
- Export data for external analysis

**Primary Features:**
- Market overview
- Advanced charting
- Data export tools
- Correlation matrices

---

## Getting Started

### Step 1: Account Setup

```
1. Navigate to https://your-platform.com
2. Click "Sign Up"
3. Enter email and create password
4. Verify email address
5. Log in to dashboard
```

### Step 2: Connect Exchange (Optional)

**For Paper Trading (Research Only):**
- No API keys needed
- System uses simulated broker
- Can practice with $100,000 virtual balance

**For Live Trading:**
```
1. Go to Settings → Exchange Connections
2. Click "Add Exchange"
3. Select exchange (Binance/Coinbase/Kraken)
4. Enter API Key and Secret
5. Set permissions (read-only for research, trade for live)
6. Test connection
7. Enable exchange
```

**API Key Security:**
- Keys are encrypted (AES-256)
- Can restrict to specific IP addresses
- Recommend trade-only permissions (NO withdrawal)
- Can be revoked anytime

### Step 3: Choose Your Mode

**Paper Trading (Safe):**
- Toggle "Paper Trading Mode" ON in settings
- All orders execute against simulated broker
- Perfect for testing strategies
- No real money at risk

**Live Trading:**
- Toggle "Paper Trading Mode" OFF
- Requires exchange API keys
- Real orders sent to exchange
- Real money at risk

---

## Trading Control Features

### 4.1 Manual Trading Interface

**Location:** Main Navigation → Trading

```
┌─────────────────────────────────────────────────────────────┐
│  🔍 Search Pair: BTC/USDT                                    │
│                                                              │
│  ┌──────────────────────┐  ┌──────────────────────────────┐ │
│  │   Price Chart        │  │   Order Book                 │ │
│  │                      │  │   ┌──────────────────────┐   │ │
│  │   📈 Candlesticks    │  │   │ ASKS (Sell Orders)   │   │ │
│  │                      │  │   │ 67,235.00  0.543 BTC │   │ │
│  │   [1m][5m][1h][1d]   │  │   │ 67,234.50  1.234 BTC │   │ │
│  │                      │  │   │──────────────────────│   │ │
│  │   Indicators:        │  │   │ BIDS (Buy Orders)    │   │ │
│  │   ☑ Volume           │  │   │ 67,233.00  0.891 BTC │   │ │
│  │   ☑ MA (20, 50)      │  │   │ 67,232.50  2.145 BTC │   │ │
│  │   ☐ RSI              │  │   └──────────────────────┘   │ │
│  │   ☐ MACD             │  │                              │ │
│  └──────────────────────┘  └──────────────────────────────┘ │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  ORDER ENTRY                                         │   │
│  │  [Buy] [Sell]  [Market] [Limit] [Stop-Limit]        │   │
│  │                                                      │   │
│  │  Amount: [________] BTC                             │   │
│  │  Price:  [________] USDT  ← (disabled for Market)  │   │
│  │  Total:  [________] USDT                            │   │
│  │                                                      │   │
│  │  Advanced Options:                                  │   │
│  │  ☐ Stop Loss: [________] USDT                      │   │
│  │  ☐ Take Profit: [________] USDT                    │   │
│  │                                                      │   │
│  │  [Preview Order]  [Place Order]                     │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  OPEN ORDERS (3)                                     │   │
│  │  BTC/USDT  Limit Buy   0.5 @ 66,000  [Cancel]       │   │
│  │  ETH/USDT  Limit Sell  2.0 @ 3,500   [Cancel]       │   │
│  │  SOL/USDT  Stop Loss   10  @ 95      [Cancel]       │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  POSITIONS (2)                      Total P&L: +$234 │   │
│  │  BTC/USDT  1.2 BTC  Entry: $65,000  P&L: +$3,456    │   │
│  │  ETH/USDT  5.0 ETH  Entry: $3,200   P&L: +$1,500    │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### How to Place a Trade

**Example: Buy 0.5 BTC with Limit Order**

```
1. Navigate to Trading page
2. Search for "BTC/USDT" in pair selector
3. Review current price on chart (e.g., $67,234)
4. Click "Buy" button
5. Select "Limit" order type
6. Enter Amount: 0.5 BTC
7. Enter Price: 66,000 USDT (below market to wait for dip)
8. System calculates Total: 33,000 USDT
9. Optional: Check "Stop Loss" and enter 64,000
10. Click "Preview Order" → Review details
11. Click "Place Order"
12. Order appears in "Open Orders" section
13. When market hits $66,000, order fills automatically
14. Position appears in "Positions" section
```

### Order Types Explained

**Market Order:**
- Executes immediately at current market price
- Guarantees execution, not price
- Use when: You need to enter/exit NOW

**Limit Order:**
- Executes only at specified price or better
- Guarantees price, not execution
- Use when: You want to wait for specific entry point

**Stop-Limit Order:**
- Triggers limit order when stop price reached
- Use when: Protecting profits or limiting losses

### Quick Trade Buttons

For fast execution, use 1-click trading:

```
┌─────────────────────────────────┐
│  Quick Trade: BTC/USDT          │
│                                 │
│  [Buy $100] [Buy $500] [Buy $1K]│
│  [Sell 25%] [Sell 50%] [Sell All]│
│                                 │
│  ⚠️ 1-Click Enabled (Market Orders)│
└─────────────────────────────────┘
```

**Warning:** 1-click trading executes instantly without confirmation!

### Portfolio Management

**Location:** Dashboard → Portfolio

```
┌──────────────────────────────────────────────────────┐
│  Total Portfolio Value: $125,432.67  (+12.3% 24h)   │
│                                                      │
│  ┌────────────────────────────────────────────┐     │
│  │  Allocation Pie Chart                      │     │
│  │  🟦 BTC: 45% ($56,444)                     │     │
│  │  🟩 ETH: 30% ($37,629)                     │     │
│  │  🟨 SOL: 15% ($18,814)                     │     │
│  │  🟧 Others: 10% ($12,544)                  │     │
│  └────────────────────────────────────────────┘     │
│                                                      │
│  Holdings Detail:                                   │
│  Asset   Amount      Value       P&L        %Change │
│  BTC     0.84       $56,444     +$4,231     +8.1%   │
│  ETH     11.2       $37,629     +$2,156     +6.1%   │
│  SOL     194.3      $18,814     +$1,023     +5.7%   │
│  USDT    12,544     $12,544     $0          0.0%    │
│                                                      │
│  [Rebalance Portfolio] [Export CSV]                 │
└──────────────────────────────────────────────────────┘
```

### Risk Management Controls

**Location:** Settings → Risk Management

```
Position Limits:
☑ Max position size per trade: 10% of portfolio
☑ Max total exposure: 90% (keep 10% cash)
☑ Max positions: 10 concurrent

Stop-Loss Defaults:
☑ Auto stop-loss: 5% below entry
☑ Trailing stop: 3% from peak

Order Limits:
☑ Max order size: $10,000 per order
☑ Require confirmation for orders > $1,000

Notifications:
☑ Email alerts for fills
☑ SMS alerts for stop-loss triggers
```

---

## Research & Analysis Features

### 5.1 Market Overview & Screening

**Location:** Main Navigation → Markets

```
┌─────────────────────────────────────────────────────────────┐
│  MARKET OVERVIEW                                            │
│                                                             │
│  Filter: [All] [Favorites] [Volume>$1M] [Gainers] [Losers] │
│  Sort by: [Volume ▼] [Price] [% Change] [Market Cap]       │
│                                                             │
│  Pair         Price      24h Change   24h Volume   Action  │
│  ⭐ BTC/USDT  $67,234    +2.3%       $2.4B         [Trade]  │
│  ⭐ ETH/USDT  $3,456     +1.8%       $1.1B         [Trade]  │
│     SOL/USDT  $98.45     +5.2%       $456M         [Trade]  │
│     ADA/USDT  $0.542     -1.2%       $234M         [Trade]  │
│     XRP/USDT  $0.678     +0.8%       $345M         [Trade]  │
│                                                             │
│  [Export Data] [Add to Watchlist] [Compare Assets]         │
└─────────────────────────────────────────────────────────────┘
```

**Screening Capabilities:**
- **Volume Filter:** Find high-liquidity pairs
- **Volatility Filter:** Identify volatile assets for day trading
- **Momentum Filter:** Assets with strong trends
- **Correlation Analysis:** Find uncorrelated assets for diversification

### 5.2 Advanced Charting

**Location:** Trading Page → Chart (Full Screen Mode)

**Available Indicators:**
- Moving Averages (SMA, EMA)
- Bollinger Bands
- RSI (Relative Strength Index)
- MACD (Moving Average Convergence Divergence)
- Volume Profile
- Fibonacci Retracements
- Support/Resistance Lines

**Drawing Tools:**
- Trend Lines
- Horizontal Lines
- Channels
- Rectangles
- Annotations

**Timeframes:**
- 1m, 5m, 15m, 30m (Intraday)
- 1h, 4h (Swing)
- 1d, 1w (Position)

**Chart Sharing:**
- Save chart layouts
- Export as image
- Share analysis via URL

### 5.3 ML Model Insights

**Location:** Analytics → ML Models

```
┌─────────────────────────────────────────────────────────────┐
│  MACHINE LEARNING MODEL PERFORMANCE                         │
│                                                             │
│  Active Models: 5                                           │
│                                                             │
│  Model            Accuracy  F1-Score  Predictions (24h)    │
│  Random Forest    78.4%     0.82      143  (89 wins)       │
│  Gradient Boost   76.2%     0.79      143  (84 wins)       │
│  Extra Trees      75.8%     0.78      143  (82 wins)       │
│  AdaBoost         72.1%     0.74      143  (76 wins)       │
│  SVC              69.3%     0.71      143  (71 wins)       │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Feature Importance (Random Forest)                 │   │
│  │  ████████████████████ Volume_MA_20        0.18      │   │
│  │  ██████████████ Price_Momentum            0.12      │   │
│  │  ████████████ RSI_14                      0.11      │   │
│  │  ██████████ MACD_Signal                   0.09      │   │
│  │  ████████ Volatility_Std                  0.08      │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  Current Prediction (BTC/USDT):                            │
│  🟢 BUY Signal (Confidence: 73%)                           │
│  Next 10 seconds predicted: +0.15% movement                │
│                                                             │
│  [Retrain Models] [View Detailed Report] [Backtest]       │
└─────────────────────────────────────────────────────────────┘
```

**How ML Insights Help Research:**

1. **Strategy Validation:** See which features matter most
2. **Model Comparison:** Identify best-performing algorithms
3. **Confidence Levels:** Understand prediction reliability
4. **Feature Engineering:** Discover new indicators to add

### 5.4 Backtesting Engine

**Location:** Analytics → Backtest

```
┌─────────────────────────────────────────────────────────────┐
│  STRATEGY BACKTESTING                                       │
│                                                             │
│  Strategy: ML Prediction Bot (Random Forest)               │
│  Asset: BTC/USDT                                           │
│  Period: 2025-01-01 to 2025-12-31 (1 year)                │
│  Initial Capital: $10,000                                  │
│                                                             │
│  RESULTS:                                                   │
│  ├─ Final Value: $13,456                                   │
│  ├─ Total Return: +34.56%                                  │
│  ├─ Sharpe Ratio: 1.82                                     │
│  ├─ Max Drawdown: -12.3%                                   │
│  ├─ Win Rate: 64.2%                                        │
│  ├─ Total Trades: 342                                      │
│  ├─ Avg Trade: +$10.11                                     │
│  └─ Best Trade: +$234.56                                   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Equity Curve                                       │   │
│  │  $14K ┤                                  ╭──        │   │
│  │  $12K ┤                         ╭────────╯          │   │
│  │  $10K ┼─────────────────────────╯                   │   │
│  │   $8K ┤                                             │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  [Adjust Parameters] [Compare Strategies] [Export Report]  │
└─────────────────────────────────────────────────────────────┘
```

**Backtesting Workflow:**

1. Select strategy type (ML, Grid, DCA, Custom)
2. Configure parameters (risk %, timeframes, etc.)
3. Choose historical period
4. Set initial capital
5. Run backtest
6. Analyze results
7. Optimize parameters
8. Re-run until satisfied
9. Deploy as live bot

### 5.5 Performance Analytics

**Location:** Analytics → Performance

```
┌─────────────────────────────────────────────────────────────┐
│  PORTFOLIO PERFORMANCE ANALYTICS                            │
│                                                             │
│  Time Period: [Last 30 Days ▼]                             │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Equity Curve (Last 30 Days)                        │   │
│  │  $130K ┤                                    ╭─      │   │
│  │  $125K ┤                          ╭─────────╯       │   │
│  │  $120K ┼──────────────────────────╯                 │   │
│  │  $115K ┤                                            │   │
│  │  $110K ┤                                            │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  Key Metrics:                                              │
│  ├─ Total Return: +18.2%                                   │
│  ├─ Sharpe Ratio: 2.34  (Excellent)                       │
│  ├─ Sortino Ratio: 3.12                                   │
│  ├─ Max Drawdown: -5.6%                                    │
│  ├─ Calmar Ratio: 3.25                                     │
│  ├─ Win Rate: 67.8%                                        │
│  └─ Profit Factor: 2.1                                     │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  P&L by Asset                                       │   │
│  │  BTC: +$4,231 ████████████████                     │   │
│  │  ETH: +$2,156 ████████                             │   │
│  │  SOL: +$1,023 ████                                  │   │
│  │  ADA: -$234   █                                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Trade Distribution (Heatmap)                       │   │
│  │  Hour  | Mon | Tue | Wed | Thu | Fri | Sat | Sun   │   │
│  │  00-04 | ░░░ | ░░░ | ░░░ | ░░░ | ░░░ | ░░░ | ░░░   │   │
│  │  04-08 | ░░░ | ██░ | ░░░ | ██░ | ░░░ | ░░░ | ░░░   │   │
│  │  08-12 | ███ | ███ | ███ | ███ | ███ | ░░░ | ░░░   │   │
│  │  12-16 | ███ | ███ | ███ | ███ | ███ | ██░ | ░░░   │   │
│  │  16-20 | ██░ | ███ | ██░ | ███ | ██░ | ░░░ | ░░░   │   │
│  │  20-24 | ░░░ | ░░░ | ░░░ | ░░░ | ░░░ | ░░░ | ░░░   │   │
│  │  (Darker = More Profitable Trades)                  │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  [Generate PDF Report] [Export CSV] [Share Analysis]       │
└─────────────────────────────────────────────────────────────┘
```

**Research Questions This Answers:**

- "Which assets are most profitable for me?"
- "What time of day do I trade best?"
- "Is my strategy improving over time?"
- "How does my performance compare to buy-and-hold?"
- "What's my risk-adjusted return?"

### 5.6 Market Correlation Analysis

**Location:** Analytics → Correlations

```
┌─────────────────────────────────────────────────────────────┐
│  ASSET CORRELATION MATRIX (30-Day)                          │
│                                                             │
│           BTC    ETH    SOL    ADA    XRP    DOGE           │
│  BTC      1.00   0.89   0.76   0.65   0.58   0.45          │
│  ETH      0.89   1.00   0.82   0.71   0.63   0.52          │
│  SOL      0.76   0.82   1.00   0.68   0.61   0.48          │
│  ADA      0.65   0.71   0.68   1.00   0.74   0.59          │
│  XRP      0.58   0.63   0.61   0.74   1.00   0.66          │
│  DOGE     0.45   0.52   0.48   0.59   0.66   1.00          │
│                                                             │
│  Color Key:  🟥 High (>0.8)  🟨 Medium (0.5-0.8)  🟩 Low (<0.5)│
│                                                             │
│  Insights:                                                  │
│  • BTC and ETH are highly correlated (0.89)                │
│  • DOGE shows lowest correlation with BTC (0.45)           │
│  • Consider DOGE for portfolio diversification             │
│                                                             │
│  [Update Period] [Add Assets] [Export Data]                │
└─────────────────────────────────────────────────────────────┘
```

**Use Cases:**
- **Diversification:** Find uncorrelated assets
- **Hedging:** Identify negative correlations
- **Pair Trading:** Spot correlation breakdowns

### 5.7 Data Export for External Research

**Location:** Any data view → Export button

**Export Formats:**
- CSV (for Excel, Python pandas)
- JSON (for APIs, programming)
- PDF (for reports, sharing)

**Exportable Data:**
- Historical OHLCV data
- Trade history
- Order book snapshots
- Performance metrics
- ML model predictions
- Custom queries via API

---

## Automated Trading (Bots)

### 6.1 Bot Management Interface

**Location:** Main Navigation → Bots

```
┌─────────────────────────────────────────────────────────────┐
│  MY TRADING BOTS                                            │
│                                                             │
│  [+ Create New Bot]                     Filter: [All ▼]     │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 🟢 ML Prediction Bot #1              RUNNING        │   │
│  │                                                      │   │
│  │ Strategy: Random Forest Predictions                 │   │
│  │ Pairs: BTC/USDT, ETH/USDT                          │   │
│  │ Started: 2026-01-01 10:00 (9 days ago)             │   │
│  │                                                      │   │
│  │ Performance:                                        │   │
│  │ ├─ Total P&L: +$1,234.56 (+12.3%)                  │   │
│  │ ├─ Win Rate: 68.4%                                  │   │
│  │ ├─ Trades: 87 (59 wins, 28 losses)                 │   │
│  │ └─ Avg Trade: +$14.19                              │   │
│  │                                                      │   │
│  │ [⏸ Pause] [⚙️ Settings] [📊 Details] [🗑️ Delete]   │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 🟡 Grid Trading Bot #2               PAUSED         │   │
│  │                                                      │   │
│  │ Strategy: Grid Trading (30 levels)                  │   │
│  │ Pairs: SOL/USDT                                     │   │
│  │ Started: 2026-01-05 08:00 (5 days ago)             │   │
│  │                                                      │   │
│  │ Performance:                                        │   │
│  │ ├─ Total P&L: +$234.12 (+4.7%)                     │   │
│  │ ├─ Win Rate: 100% (grid never loses)               │   │
│  │ ├─ Trades: 23 (23 wins, 0 losses)                  │   │
│  │ └─ Avg Trade: +$10.18                              │   │
│  │                                                      │   │
│  │ [▶️ Resume] [⚙️ Settings] [📊 Details] [🗑️ Delete] │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 🔴 DCA Bot #3                        STOPPED        │   │
│  │                                                      │   │
│  │ Strategy: Dollar Cost Averaging                     │   │
│  │ Pairs: BTC/USDT                                     │   │
│  │ Started: 2025-12-01 (40 days ago)                  │   │
│  │ Stopped: 2026-01-09 (today)                        │   │
│  │                                                      │   │
│  │ Performance:                                        │   │
│  │ ├─ Total P&L: +$456.78 (+9.1%)                     │   │
│  │ ├─ Win Rate: N/A (accumulation strategy)           │   │
│  │ ├─ Purchases: 40                                    │   │
│  │ └─ Avg Price: $63,234.56                           │   │
│  │                                                      │   │
│  │ [▶️ Start] [⚙️ Settings] [📊 Details] [🗑️ Delete]  │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### 6.2 Creating a Bot

**Wizard Flow: ML Prediction Bot Example**

**Step 1: Choose Strategy Template**
```
Select Bot Type:
○ ML Prediction Bot (Uses trained models)
○ Grid Trading Bot (Profit from volatility)
○ DCA Bot (Regular purchases)
○ Arbitrage Bot (Cross-exchange opportunities)
○ Custom Strategy (Write your own logic)

[Next]
```

**Step 2: Configure Parameters**
```
ML Prediction Bot Configuration:

Model Selection:
☑ Random Forest (78.4% accuracy)
☐ Gradient Boosting (76.2% accuracy)
☐ Extra Trees (75.8% accuracy)

Trading Pairs:
☑ BTC/USDT
☑ ETH/USDT
☐ SOL/USDT

Risk Settings:
Position Size: [5]% of portfolio per trade
Max Simultaneous Positions: [3]
Minimum Confidence: [70]%

Entry Rules:
Signal Type: [BUY signals only ▼]
Confirmation: [Require 2 consecutive predictions ▼]

Exit Rules:
Take Profit: [3]%
Stop Loss: [2]%
Max Hold Time: [24] hours

[Back] [Next]
```

**Step 3: Backtest Strategy**
```
Running backtest on historical data...

Period: Last 90 days
Initial Capital: $10,000 (simulated)

Results:
✅ Total Return: +23.4%
✅ Win Rate: 68.2%
✅ Max Drawdown: -5.1%
✅ Sharpe Ratio: 2.1

[View Detailed Report] [Adjust Settings] [Deploy Bot]
```

**Step 4: Deploy**
```
Ready to Deploy!

Bot Name: [ML Prediction Bot #1]

Mode:
○ Paper Trading (Simulated - Safe)
● Live Trading (Real Money - Requires API Key)

Initial Capital Allocation: [$5,000]

Confirmation:
☑ I understand this bot will execute real trades
☑ I have set appropriate stop-loss limits
☑ I will monitor bot performance regularly

[Cancel] [Deploy Bot]
```

### 6.3 Monitoring Bot Performance

**Location:** Bots → [Bot Name] → Details

```
┌─────────────────────────────────────────────────────────────┐
│  ML PREDICTION BOT #1 - DETAILED PERFORMANCE                │
│                                                             │
│  Status: 🟢 RUNNING          Uptime: 9 days 14 hours       │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Equity Curve                                       │   │
│  │  $6.2K ┤                                      ╭─    │   │
│  │  $6.0K ┤                              ╭───────╯     │   │
│  │  $5.8K ┤                      ╭───────╯             │   │
│  │  $5.6K ┤              ╭───────╯                     │   │
│  │  $5.4K ┤      ╭───────╯                             │   │
│  │  $5.2K ┤  ╭───╯                                     │   │
│  │  $5.0K ┼──╯                                         │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  Summary Statistics:                                       │
│  ├─ Starting Capital: $5,000.00                            │
│  ├─ Current Value: $6,234.56                              │
│  ├─ Total Return: +$1,234.56 (+24.7%)                     │
│  ├─ Daily Avg Return: +2.74%                              │
│  └─ Sharpe Ratio: 2.34                                    │
│                                                             │
│  Trade Statistics:                                         │
│  ├─ Total Trades: 87                                       │
│  ├─ Wins: 59 (67.8%)                                      │
│  ├─ Losses: 28 (32.2%)                                     │
│  ├─ Avg Win: +$32.45                                      │
│  ├─ Avg Loss: -$18.23                                     │
│  ├─ Largest Win: +$145.67                                 │
│  ├─ Largest Loss: -$67.89                                 │
│  └─ Profit Factor: 2.1                                     │
│                                                             │
│  Current Positions:                                        │
│  BTC/USDT  0.02 BTC  Entry: $66,000  P&L: +$24.68        │
│  ETH/USDT  0.50 ETH  Entry: $3,400   P&L: +$28.00        │
│                                                             │
│  Recent Trades:                                            │
│  2026-01-09 14:23  BTC/USDT  SELL  0.01  $67,234  +$12.34 │
│  2026-01-09 12:15  ETH/USDT  BUY   0.50  $3,400   (open)  │
│  2026-01-09 10:08  SOL/USDT  SELL  2.00  $98.45   +$8.90  │
│                                                             │
│  Model Performance:                                        │
│  ├─ Prediction Accuracy: 78.4%                            │
│  ├─ False Positives: 12 (13.8%)                           │
│  ├─ False Negatives: 7 (8.0%)                             │
│  └─ Avg Confidence: 76.2%                                 │
│                                                             │
│  [⏸ Pause Bot] [⚙️ Adjust Settings] [📥 Export Data]      │
└─────────────────────────────────────────────────────────────┘
```

### 6.4 Bot Alerts & Notifications

**Automatic Alerts Sent When:**
- Bot opens new position
- Bot closes position (profit/loss)
- Stop-loss triggered
- Bot paused due to error
- Daily performance summary
- Capital drawdown exceeds threshold

**Alert Channels:**
- Email
- Browser notification
- Webhook (for Slack, Discord, custom)
- SMS (optional, premium feature)

---

## Complete User Workflows

### Workflow 1: Research Before Trading

**Scenario:** You heard SOL is pumping. Should you buy?

```
Step 1: Market Overview
├─ Go to Markets page
├─ Search for "SOL/USDT"
├─ Check 24h change (+5.2%), volume ($456M)
└─ Add to watchlist

Step 2: Chart Analysis
├─ Open Trading page → Select SOL/USDT
├─ View 1-hour chart
├─ Add indicators: RSI, Volume, MA(20, 50)
├─ Observation: RSI at 78 (overbought!)
└─ Conclusion: Maybe wait for pullback

Step 3: Check ML Predictions
├─ Go to Analytics → ML Models
├─ View prediction for SOL/USDT
├─ Current signal: BUY (confidence 68%)
└─ Note: Moderate confidence, proceed cautiously

Step 4: Backtest Strategy
├─ Go to Analytics → Backtest
├─ Set up: "Buy on ML BUY signal, Sell at +3%"
├─ Run on 30-day history
├─ Results: Win rate 65%, but Sharpe ratio only 1.2
└─ Decision: Strategy works, but marginal

Step 5: Paper Trade First
├─ Enable Paper Trading Mode
├─ Place limit buy order: 10 SOL @ $97 (below market)
├─ Monitor for 24 hours
└─ See if strategy would have worked

Step 6: Execute (If Confident)
├─ Disable Paper Trading Mode
├─ Place real limit order
├─ Set stop-loss at $94 (-3%)
├─ Set take-profit at $103 (+6%)
└─ Monitor position in Portfolio

Total Time: 15-20 minutes of research before risking capital
```

### Workflow 2: Active Day Trading

**Scenario:** You're a day trader exploiting BTC volatility

```
Morning (8:00 AM):
├─ Log in to Dashboard
├─ Check overnight positions (none)
├─ Review market overview (BTC down 1.2% overnight)
├─ Check ML prediction: NEUTRAL (confidence 52% - not actionable)
└─ Decide to wait for setup

Mid-Morning (10:30 AM):
├─ BTC bounces off $66,000 support (identified on chart)
├─ RSI crosses above 30 (oversold)
├─ Volume spike confirms reversal
├─ ML prediction updates: BUY (confidence 74%)
├─ ACTION: Click "Quick Buy $1000" (Market order)
└─ Position opened: 0.015 BTC @ $66,500

Monitoring (10:30 - 2:00 PM):
├─ Set price alert: $68,000 (target)
├─ Set stop-loss order: $65,850 (-1%)
├─ Continue working, check phone occasionally
└─ Alert received at 1:45 PM: Price hit $68,000!

Afternoon (1:50 PM):
├─ Review position: +$22.50 profit (+2.25%)
├─ Check chart: Resistance at $68,200
├─ ML prediction: NEUTRAL (confidence dropping to 58%)
├─ ACTION: Click "Sell All" (Market order)
├─ Position closed: 0.015 BTC @ $68,000
└─ Profit: +$22.50 (after fees: +$20.25)

End of Day (5:00 PM):
├─ Review Analytics → Performance
├─ Today's P&L: +$20.25 (1 trade, 100% win rate)
├─ Update trading journal (notes in bot settings)
└─ Log out

Next Day: Analyze yesterday's trade to improve strategy
```

### Workflow 3: Long-Term Automated Strategy

**Scenario:** Set up a bot and check it weekly

```
Initial Setup (Week 0):
├─ Go to Bots → Create New Bot
├─ Select "DCA Bot" (Dollar Cost Averaging)
├─ Configure:
│   ├─ Asset: BTC/USDT
│   ├─ Investment: $100 per week
│   ├─ Schedule: Every Monday 9:00 AM
│   └─ Duration: 1 year (52 weeks = $5,200 total)
├─ Backtest on past year: +18% vs lump sum
├─ Deploy bot in LIVE mode
└─ Set alert: Weekly email summary

Week 1-4 (Passive Monitoring):
├─ Receive email each Monday: "DCA Bot purchased $100 BTC"
├─ Check dashboard briefly: Portfolio growing
└─ No action needed

Week 5 (Monthly Review):
├─ Go to Bots → DCA Bot #3 → Details
├─ Review performance:
│   ├─ Invested: $500
│   ├─ Current value: $534.67
│   ├─ Unrealized gain: +$34.67 (+6.9%)
│   └─ Avg entry price: $65,123
├─ Compare to market:
│   ├─ BTC current price: $67,234
│   └─ If bought lump sum Week 1: +$412 (better)
│   └─ But we avoided timing risk and volatility
├─ Decision: Continue strategy
└─ Export CSV for tax records

Week 52 (End of Year):
├─ Review annual performance
├─ Decide: Continue for another year or cash out?
├─ If continuing: Bot keeps running automatically
├─ If cashing out: Pause bot, manually sell positions
└─ Export full trade history for tax filing

Total Active Time: ~1 hour over entire year
```

### Workflow 4: ML Strategy Optimization

**Scenario:** You're a quant improving ML models

```
Step 1: Baseline Performance
├─ Go to Analytics → ML Models
├─ Review current model performance:
│   └─ Random Forest: 78.4% accuracy, 0.82 F1-score
├─ Export feature importance data
└─ Hypothesis: Can we improve by adding new features?

Step 2: Feature Analysis
├─ Go to Analytics → Backtest
├─ Run backtests with different feature combinations:
│   ├─ Test 1: Original 64 features → 78.4% accuracy
│   ├─ Test 2: Add order book imbalance → 79.1% accuracy ✅
│   ├─ Test 3: Add Twitter sentiment → 77.8% accuracy ❌
│   └─ Test 4: Add funding rates → 79.8% accuracy ✅
└─ Best combination: Original + order book + funding rates

Step 3: Parameter Tuning
├─ Adjust GridSearchCV parameters in bot settings
├─ Increase CV folds from 2 to 5 (better validation)
├─ Run backtests again on 90-day period
├─ New accuracy: 81.2% (improvement!)
└─ Sharpe ratio improves from 2.1 to 2.6

Step 4: Paper Trading Validation
├─ Create new bot: "ML Prediction Bot v2"
├─ Enable Paper Trading Mode
├─ Run for 7 days alongside current bot
├─ Results:
│   ├─ v1 (current): +$123 (78% win rate)
│   ├─ v2 (new): +$156 (82% win rate) ✅
└─ Conclusion: v2 performs better!

Step 5: Deploy Improved Model
├─ Pause v1 bot
├─ Switch v2 bot to LIVE mode
├─ Monitor for 14 days
├─ If performance holds: Retire v1 permanently
└─ Document improvements in notes

Step 6: Continuous Monitoring
├─ Weekly: Check if accuracy degrades (model drift)
├─ Monthly: Retrain on recent data
├─ Quarterly: Major feature engineering review
└─ Yearly: Complete strategy overhaul

This iterative process leads to continuous improvement!
```

---

## Interface Walkthrough

### Main Navigation Bar

```
┌─────────────────────────────────────────────────────────────┐
│ 🏠 Dashboard | 📊 Markets | 💹 Trading | 🤖 Bots | 📈 Analytics│
│                                                             │
│                              👤 John Doe  🔔 [3]  ⚙️ Settings│
└─────────────────────────────────────────────────────────────┘
```

**Always Visible:**
- Quick access to all major sections
- Notification bell (order fills, alerts)
- User profile dropdown
- Settings access

### Sidebar (Collapsible)

```
┌────────────────┐
│ 🏠 Dashboard   │
│                │
│ 📊 Markets     │
│ ├─ Overview    │
│ ├─ Screener    │
│ └─ Watchlist   │
│                │
│ 💹 Trading     │
│ ├─ Spot        │
│ └─ Positions   │
│                │
│ 🤖 Bots        │
│ ├─ My Bots     │
│ ├─ Create      │
│ └─ Templates   │
│                │
│ 📈 Analytics   │
│ ├─ Performance │
│ ├─ ML Models   │
│ ├─ Backtest    │
│ └─ Reports     │
│                │
│ ⚙️ Settings    │
│ ├─ Profile     │
│ ├─ Exchanges   │
│ ├─ Risk Mgmt   │
│ └─ API Keys    │
└────────────────┘
```

### Real-Time Status Bar

```
┌─────────────────────────────────────────────────────────────┐
│ Mode: 📄 PAPER TRADING  |  BTC: $67,234 (+2.3%)  |         │
│ Portfolio: $125,432 (+12.3%)  |  Open Orders: 3  |          │
│ Active Bots: 2  |  System Status: 🟢 All Systems Operational │
└─────────────────────────────────────────────────────────────┘
```

**Always Visible at Bottom:**
- Current trading mode (Paper/Live)
- BTC price (market pulse)
- Portfolio value snapshot
- Quick stats
- System health

### Keyboard Shortcuts

```
? - Show keyboard shortcuts
D - Dashboard
M - Markets
T - Trading page
B - Bots
A - Analytics
S - Settings
/ - Search (symbols, features)
ESC - Close dialogs
F - Toggle fullscreen chart
```

---

## Summary: Trading Control vs. Research

### Trading Control Features ✅

| Feature | Purpose | Access Level |
|---------|---------|--------------|
| Manual Order Entry | Execute trades | Requires API keys |
| Quick Trade Buttons | Fast execution | Requires API keys |
| Stop-Loss/Take-Profit | Risk management | Requires API keys |
| Position Management | Track holdings | Requires API keys |
| Bot Deployment | Automated trading | Requires API keys |
| Portfolio Rebalancing | Asset allocation | Requires API keys |

### Research & Analysis Features 📊

| Feature | Purpose | Access Level |
|---------|---------|--------------|
| Market Screener | Discover opportunities | No API keys needed |
| Advanced Charting | Technical analysis | No API keys needed |
| ML Model Insights | Strategy validation | No API keys needed |
| Backtesting | Historical testing | No API keys needed |
| Performance Analytics | Track results | View own data only |
| Data Export | External analysis | No API keys needed |
| Correlation Analysis | Diversification | No API keys needed |

### The System Provides BOTH 💡

**Research Mode (Safe):**
- No API keys required
- No real money at risk
- Full access to analysis tools
- Learn before you earn

**Trading Mode (Active):**
- API keys required
- Real money at risk
- Full control over execution
- Manual or automated

**Best Practice:**
1. Start in Paper Trading Mode (research + practice)
2. Develop and backtest strategies
3. Run paper trading for 30 days
4. Switch to Live Trading with small capital
5. Scale up as confidence grows

---

## Conclusion

This platform is designed as a **complete trading and research ecosystem**:

✅ **For Researchers:** Explore markets, test theories, analyze data without risking capital

✅ **For Traders:** Execute strategies manually with professional-grade tools

✅ **For Developers:** Build, backtest, and deploy algorithmic strategies

✅ **For All Users:** Learn, practice, refine, then trade with confidence

The frontend provides **full visibility and control** over every aspect of the trading process, from idea generation to execution to performance analysis.
