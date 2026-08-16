# Crypto Trading Frontend Implementation Plan

> **⚠️ Proposal only — none of this has been built.**
>
> No frontend, backend API, database, WebSocket layer, or crypto exchange
> integration exists in this repository. Nothing in the file tree, schema, or
> phase plan below has been implemented.
>
> For the code that does exist, see [README.md](../../README.md). The companion
> document [USER_GUIDE.md](USER_GUIDE.md) describes the same unbuilt platform
> from a user's perspective.

**Project:** Algorithmic Cryptocurrency Trading Platform
**Date:** January 6, 2026
**Status:** Planning phase — not started

---

## Executive Summary

This document outlines a comprehensive plan to build a modern web-based frontend for the existing algorithmic trading system, extending it to support cryptocurrency trading via public APIs. The solution will provide real-time market data visualization, trade execution controls, portfolio analytics, and algorithmic strategy management.

---

## Table of Contents

1. [Current System Analysis](#1-current-system-analysis)
2. [Architecture Overview](#2-architecture-overview)
3. [Technology Stack](#3-technology-stack)
4. [Cryptocurrency API Integration](#4-cryptocurrency-api-integration)
5. [Frontend Components](#5-frontend-components)
6. [Backend API Layer](#6-backend-api-layer)
7. [Real-Time Data Handling](#7-real-time-data-handling)
8. [Security Considerations](#8-security-considerations)
9. [Implementation Phases](#9-implementation-phases)
10. [File Structure](#10-file-structure)
11. [Database Schema](#11-database-schema)
12. [Testing Strategy](#12-testing-strategy)
13. [Deployment Plan](#13-deployment-plan)

---

## 1. Current System Analysis

### Existing Components

**Backend (Python):**
- ✅ Order matching engine (742 LOC)
- ✅ Black-Scholes options pricing (606 LOC)
- ✅ ML-based trade prediction (244 LOC)
- ✅ Broker/Data adapter framework (1,011 LOC)
- ✅ Simulated broker for paper trading
- ❌ No live API connections
- ❌ No persistent database
- ❌ No REST API layer
- ❌ No frontend interface

### Key Gaps to Address

1. **Data Layer:** No real-time cryptocurrency market data
2. **API Layer:** No REST/WebSocket API for frontend communication
3. **Persistence:** No database for trades, positions, or user settings
4. **Frontend:** No user interface for monitoring and control
5. **Crypto Support:** System designed for stocks/options, not crypto pairs

---

## 2. Architecture Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND LAYER                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │  Dashboard   │  │   Trading    │  │     Analytics        │  │
│  │  - Live Data │  │   - Manual   │  │     - Performance    │  │
│  │  - Charts    │  │   - Bot Ctrl │  │     - ML Insights    │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │ REST API / WebSocket
┌────────────────────────────┴────────────────────────────────────┐
│                      BACKEND API LAYER (NEW)                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │   FastAPI    │  │  WebSocket   │  │   Authentication     │  │
│  │   Endpoints  │  │   Server     │  │   & Authorization    │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────┴────────────────────────────────────┐
│                   TRADING ENGINE LAYER (EXISTING)               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │    Order     │  │  ML Models   │  │   Crypto Data        │  │
│  │   Matching   │  │  Prediction  │  │   Adapters (NEW)     │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────┴────────────────────────────────────┐
│                    EXTERNAL SERVICES                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │   Binance    │  │   Coinbase   │  │      Kraken          │  │
│  │   REST/WS    │  │   REST/WS    │  │      REST/WS         │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                             │
┌────────────────────────────┴────────────────────────────────────┐
│                       DATA LAYER (NEW)                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  PostgreSQL: Trades, Positions, Users, Strategy Configs  │  │
│  │  Redis: Session Management, Real-time Cache, Rate Limits │  │
│  │  TimescaleDB Extension: Time-series market data storage  │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Technology Stack

### Frontend Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| **React** | 18.x | UI framework with hooks and context |
| **TypeScript** | 5.x | Type-safe development |
| **Vite** | 5.x | Build tool and dev server |
| **TailwindCSS** | 3.x | Utility-first styling |
| **shadcn/ui** | Latest | Pre-built accessible components |
| **TanStack Query** | 5.x | Server state management & caching |
| **Zustand** | 4.x | Client state management |
| **Recharts** | 2.x | Charting library |
| **TradingView Lightweight Charts** | 4.x | Advanced candlestick charts |
| **Socket.io-client** | 4.x | WebSocket communication |
| **Axios** | 1.x | HTTP client |
| **React Hook Form** | 7.x | Form management |
| **Zod** | 3.x | Schema validation |

### Backend Stack (NEW)

| Technology | Version | Purpose |
|------------|---------|---------|
| **FastAPI** | 0.109.x | Modern Python web framework |
| **Uvicorn** | 0.27.x | ASGI server |
| **SQLAlchemy** | 2.0.x | ORM for database operations |
| **Alembic** | 1.13.x | Database migrations |
| **PostgreSQL** | 15.x | Primary database |
| **TimescaleDB** | 2.13.x | Time-series extension |
| **Redis** | 7.2.x | Caching and session storage |
| **Celery** | 5.3.x | Async task queue |
| **python-socketio** | 5.10.x | WebSocket server |
| **CCXT** | 4.2.x | Unified crypto exchange library |
| **Pydantic** | 2.5.x | Data validation |
| **JWT** | Latest | Authentication tokens |
| **python-dotenv** | 1.0.x | Environment management |

### DevOps & Deployment

| Technology | Purpose |
|------------|---------|
| **Docker** | Containerization |
| **Docker Compose** | Local development orchestration |
| **Nginx** | Reverse proxy and static file serving |
| **GitHub Actions** | CI/CD pipeline |
| **pytest** | Backend testing |
| **Vitest** | Frontend testing |

---

## 4. Cryptocurrency API Integration

### Primary Exchange APIs

#### **Option 1: CCXT Library (RECOMMENDED)**

**Pros:**
- Unified interface for 100+ exchanges
- Active development and community
- Python native with excellent documentation
- Handles API differences automatically
- Built-in rate limiting and error handling

**Implementation:**
```python
import ccxt

# Unified interface across exchanges
binance = ccxt.binance({
    'apiKey': 'YOUR_API_KEY',
    'secret': 'YOUR_SECRET',
})

# Same methods work for all exchanges
markets = binance.load_markets()
ticker = binance.fetch_ticker('BTC/USDT')
orderbook = binance.fetch_order_book('BTC/USDT')
```

#### **Option 2: Individual Exchange APIs**

**Binance API:**
- **Endpoint:** https://api.binance.com
- **WebSocket:** wss://stream.binance.com:9443
- **Rate Limits:** 1200 requests/minute
- **Features:** Spot, Margin, Futures trading
- **Free Tier:** Yes (no trading fees on API access)
- **Python SDK:** `python-binance`

**Coinbase Advanced Trade API:**
- **Endpoint:** https://api.coinbase.com/api/v3
- **WebSocket:** wss://advanced-trade-ws.coinbase.com
- **Rate Limits:** Varies by endpoint
- **Features:** Spot trading, USD pairs
- **Free Tier:** Public market data free
- **Python SDK:** `coinbase-advanced-py`

**Kraken API:**
- **Endpoint:** https://api.kraken.com
- **WebSocket:** wss://ws.kraken.com
- **Rate Limits:** Counter-based system
- **Features:** Spot, Margin, Futures
- **Free Tier:** Public endpoints free
- **Python SDK:** `krakenex` or CCXT

### Crypto Data Adapter Architecture

```python
# File: crypto_adapters.py (NEW)

from abc import ABC, abstractmethod
import ccxt
from typing import Dict, List, Optional
import pandas as pd

class CryptoDataAdapter(ABC):
    """Base class for crypto exchange data adapters."""

    @abstractmethod
    def get_ticker(self, symbol: str) -> Dict:
        """Get current ticker data for a trading pair."""
        pass

    @abstractmethod
    def get_orderbook(self, symbol: str, limit: int = 100) -> Dict:
        """Get current order book."""
        pass

    @abstractmethod
    def get_ohlcv(self, symbol: str, timeframe: str, limit: int = 100) -> pd.DataFrame:
        """Get OHLCV candlestick data."""
        pass

    @abstractmethod
    def subscribe_ticker(self, symbols: List[str], callback):
        """Subscribe to real-time ticker updates via WebSocket."""
        pass

class BinanceAdapter(CryptoDataAdapter):
    """Binance exchange adapter using CCXT."""

    def __init__(self, api_key: Optional[str] = None, secret: Optional[str] = None):
        self.exchange = ccxt.binance({
            'apiKey': api_key,
            'secret': secret,
            'enableRateLimit': True,
        })

    def get_ticker(self, symbol: str) -> Dict:
        ticker = self.exchange.fetch_ticker(symbol)
        return {
            'symbol': ticker['symbol'],
            'bid': ticker['bid'],
            'ask': ticker['ask'],
            'last': ticker['last'],
            'volume': ticker['baseVolume'],
            'timestamp': ticker['timestamp']
        }

    # ... additional methods
```

### Supported Trading Pairs

**Initial Scope:**
- BTC/USDT - Bitcoin
- ETH/USDT - Ethereum
- BNB/USDT - Binance Coin
- SOL/USDT - Solana
- ADA/USDT - Cardano
- XRP/USDT - Ripple
- DOGE/USDT - Dogecoin
- MATIC/USDT - Polygon

**Extensible:** System will support any pair available on connected exchanges.

---

## 5. Frontend Components

### 5.1 Dashboard Overview

**File:** `frontend/src/pages/Dashboard.tsx`

**Features:**
- Portfolio value chart (24h, 7d, 30d, All)
- Current positions table with P&L
- Active orders summary
- Recent trades log
- Market overview (top gainers/losers)
- System status indicators

**Components:**
```tsx
<Dashboard>
  <PortfolioChart timeRange="24h" />
  <PositionsTable />
  <ActiveOrdersWidget />
  <RecentTradesLog />
  <MarketOverview />
  <SystemStatus />
</Dashboard>
```

### 5.2 Trading Interface

**File:** `frontend/src/pages/Trading.tsx`

**Features:**
- Trading pair selector with search
- Real-time price chart (TradingView style)
- Order book visualization (bid/ask spread)
- Order entry form (Market, Limit, Stop-Limit)
- Position management
- Quick trade buttons (1-click trading)

**Layout:**
```
┌─────────────────────────────────────────────────────────┐
│  Pair Selector: BTC/USDT ▼         $67,234.56  +2.3%   │
├────────────────────────┬────────────────────────────────┤
│                        │  Order Book                    │
│   Price Chart          │  Price     Amount    Total     │
│   (Candlesticks)       │  67235.00  0.543    36,508.61  │
│                        │  67234.50  1.234    82,963.35  │
│   [1m][5m][15m][1h]    │  ─────────────────────────────  │
│                        │  67233.00  0.891    59,896.50  │
│                        │  67232.50  2.145    144,213.71 │
├────────────────────────┴────────────────────────────────┤
│  Order Entry                                            │
│  [Buy] [Sell]  [Market] [Limit] [Stop-Limit]           │
│  Amount: [______] BTC   Price: [______] USDT            │
│  Total: [______] USDT         [Place Order]             │
├─────────────────────────────────────────────────────────┤
│  Open Orders (2)         Positions (3)                  │
└─────────────────────────────────────────────────────────┘
```

### 5.3 Bot Management

**File:** `frontend/src/pages/BotManagement.tsx`

**Features:**
- List of trading bots with status
- Create/Edit/Delete bot strategies
- Bot configuration (strategy type, pairs, parameters)
- Performance metrics per bot
- Start/Stop/Pause controls
- Backtesting interface

**Bot Types:**
- ML Prediction Bot (using existing `_trade_management.py`)
- Arbitrage Bot (using existing `_trade_data_management.py`)
- Grid Trading Bot (NEW)
- DCA (Dollar Cost Averaging) Bot (NEW)
- Custom Strategy Bot (NEW)

### 5.4 Analytics Dashboard

**File:** `frontend/src/pages/Analytics.tsx`

**Features:**
- Performance metrics (Sharpe ratio, max drawdown, win rate)
- Equity curve visualization
- Trade distribution heatmap
- P&L by trading pair
- Monthly/Weekly/Daily returns
- ML model performance tracking
- Feature importance visualization
- Risk metrics dashboard

### 5.5 Settings & Configuration

**File:** `frontend/src/pages/Settings.tsx`

**Sections:**
- **Exchange Connections:** API key management
- **Trading Preferences:** Default order types, confirmations
- **Risk Management:** Position limits, stop-loss defaults
- **Notifications:** Email, webhook, browser alerts
- **Display Settings:** Theme (dark/light), timezone, currency
- **Security:** 2FA, session timeout, API permissions

---

## 6. Backend API Layer

### 6.1 FastAPI Application Structure

**File:** `backend/main.py`

```python
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import socketio

# Lifespan context for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize DB, Redis, WebSocket handlers
    await startup_db_pool()
    await startup_redis()
    await startup_market_data_streams()
    yield
    # Shutdown: Close connections
    await shutdown_db_pool()
    await shutdown_redis()

app = FastAPI(
    title="Crypto Trading API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Socket.io for WebSocket
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
socket_app = socketio.ASGIApp(sio, app)

# Include routers
from routers import auth, trading, market_data, bots, analytics
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(trading.router, prefix="/api/trading", tags=["trading"])
app.include_router(market_data.router, prefix="/api/market", tags=["market"])
app.include_router(bots.router, prefix="/api/bots", tags=["bots"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])
```

### 6.2 API Endpoints

#### **Authentication Endpoints**

```
POST   /api/auth/register          - Create new user account
POST   /api/auth/login             - Login and receive JWT token
POST   /api/auth/refresh           - Refresh access token
POST   /api/auth/logout            - Invalidate token
GET    /api/auth/me                - Get current user info
PUT    /api/auth/profile           - Update user profile
POST   /api/auth/change-password   - Change password
```

#### **Market Data Endpoints**

```
GET    /api/market/pairs           - List available trading pairs
GET    /api/market/ticker/:symbol  - Get current ticker
GET    /api/market/orderbook/:symbol - Get order book
GET    /api/market/ohlcv/:symbol   - Get candlestick data
GET    /api/market/trades/:symbol  - Get recent trades
GET    /api/market/24h-stats       - Get 24h summary for all pairs
```

#### **Trading Endpoints**

```
POST   /api/trading/order          - Submit new order
GET    /api/trading/orders         - Get user's orders (open/closed)
GET    /api/trading/orders/:id     - Get order details
DELETE /api/trading/orders/:id     - Cancel order
PUT    /api/trading/orders/:id     - Modify order
GET    /api/trading/positions      - Get open positions
GET    /api/trading/trades         - Get trade history
GET    /api/trading/balance        - Get account balance
```

#### **Bot Management Endpoints**

```
GET    /api/bots                   - List user's bots
POST   /api/bots                   - Create new bot
GET    /api/bots/:id               - Get bot details
PUT    /api/bots/:id               - Update bot config
DELETE /api/bots/:id               - Delete bot
POST   /api/bots/:id/start         - Start bot
POST   /api/bots/:id/stop          - Stop bot
POST   /api/bots/:id/pause         - Pause bot
GET    /api/bots/:id/performance   - Get bot performance metrics
POST   /api/bots/:id/backtest      - Run backtest
```

#### **Analytics Endpoints**

```
GET    /api/analytics/portfolio    - Portfolio performance over time
GET    /api/analytics/pnl          - Profit & Loss summary
GET    /api/analytics/metrics      - Performance metrics (Sharpe, etc.)
GET    /api/analytics/trades       - Trade analytics
GET    /api/analytics/ml-models    - ML model performance data
```

### 6.3 WebSocket Events

**Client → Server:**
```javascript
socket.emit('subscribe_ticker', { symbols: ['BTC/USDT', 'ETH/USDT'] })
socket.emit('subscribe_orderbook', { symbol: 'BTC/USDT' })
socket.emit('unsubscribe_ticker', { symbols: ['BTC/USDT'] })
```

**Server → Client:**
```javascript
socket.on('ticker_update', (data) => {
  // { symbol: 'BTC/USDT', bid: 67234.5, ask: 67235.0, ... }
})

socket.on('orderbook_update', (data) => {
  // { symbol: 'BTC/USDT', bids: [...], asks: [...] }
})

socket.on('order_update', (data) => {
  // { order_id: 123, status: 'filled', ... }
})

socket.on('position_update', (data) => {
  // { symbol: 'BTC/USDT', size: 1.5, pnl: 1234.56, ... }
})
```

---

## 7. Real-Time Data Handling

### 7.1 Market Data Streaming

**Architecture:**
```
Exchange WebSocket → Python Handler → Redis PubSub → FastAPI WebSocket → React Client
```

**Implementation:**

```python
# File: backend/services/market_data_service.py

import asyncio
import ccxt.pro as ccxt
from redis import asyncio as aioredis
import json

class MarketDataService:
    def __init__(self):
        self.exchange = ccxt.binance()
        self.redis = None
        self.subscriptions = {}

    async def start(self):
        """Initialize connections and start streaming."""
        self.redis = await aioredis.from_url("redis://localhost")

    async def subscribe_ticker(self, symbol: str):
        """Subscribe to ticker updates from exchange."""
        if symbol in self.subscriptions:
            return

        async def ticker_loop():
            while True:
                try:
                    ticker = await self.exchange.watch_ticker(symbol)
                    await self.redis.publish(
                        f'ticker:{symbol}',
                        json.dumps(ticker)
                    )
                except Exception as e:
                    print(f"Error in ticker loop: {e}")
                    await asyncio.sleep(1)

        task = asyncio.create_task(ticker_loop())
        self.subscriptions[symbol] = task
```

### 7.2 Frontend Data Hooks

```typescript
// File: frontend/src/hooks/useMarketData.ts

import { useEffect, useState } from 'react'
import { socket } from '@/lib/socket'

export function useTicker(symbol: string) {
  const [ticker, setTicker] = useState(null)

  useEffect(() => {
    socket.emit('subscribe_ticker', { symbols: [symbol] })

    socket.on('ticker_update', (data) => {
      if (data.symbol === symbol) {
        setTicker(data)
      }
    })

    return () => {
      socket.emit('unsubscribe_ticker', { symbols: [symbol] })
      socket.off('ticker_update')
    }
  }, [symbol])

  return ticker
}
```

---

## 8. Security Considerations

### 8.1 Authentication & Authorization

**JWT Token Structure:**
```json
{
  "user_id": 123,
  "email": "user@example.com",
  "role": "trader",
  "permissions": ["trade", "view_analytics"],
  "exp": 1704672000
}
```

**Implementation:**
- Access tokens: 15-minute expiry
- Refresh tokens: 7-day expiry, stored in HTTP-only cookie
- Rate limiting: 100 requests/minute per user
- API key encryption: AES-256 for stored exchange keys

### 8.2 API Key Security

**Storage:**
- Exchange API keys encrypted in database
- Encryption key stored in environment variable (never in code)
- Keys decrypted only in memory when needed

**Permissions:**
- Read-only API keys for market data
- Trade-enabled keys with IP whitelist
- No withdrawal permissions required

### 8.3 Input Validation

**Order Validation:**
```python
from pydantic import BaseModel, validator

class OrderRequest(BaseModel):
    symbol: str
    side: str  # 'buy' or 'sell'
    type: str  # 'market', 'limit', 'stop_limit'
    amount: float
    price: Optional[float]

    @validator('amount')
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError('Amount must be positive')
        if v > 1000:  # Max order size
            raise ValueError('Amount exceeds maximum')
        return v
```

### 8.4 CORS & CSRF Protection

- CORS restricted to frontend domain
- CSRF tokens for state-changing requests
- SameSite cookie attribute
- Content Security Policy headers

### 8.5 Rate Limiting

**Implementation:**
```python
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

@app.post("/api/trading/order")
@limiter.limit("10/minute")  # Max 10 orders per minute
async def submit_order():
    pass
```

---

## 9. Implementation Phases

### **Phase 1: Foundation (Weeks 1-2)**

**Backend:**
- [ ] Set up FastAPI project structure
- [ ] Configure PostgreSQL + TimescaleDB
- [ ] Configure Redis
- [ ] Implement authentication system (JWT)
- [ ] Create database models and migrations
- [ ] Implement basic CRUD endpoints

**Frontend:**
- [ ] Initialize React + Vite + TypeScript project
- [ ] Configure TailwindCSS + shadcn/ui
- [ ] Set up routing (React Router)
- [ ] Implement authentication UI (login/register)
- [ ] Create layout components (header, sidebar, footer)
- [ ] Set up API client (Axios) with auth interceptors

**DevOps:**
- [ ] Create Docker Compose for local development
- [ ] Set up environment configuration (.env)

**Deliverable:** Basic authenticated web app with empty dashboard

---

### **Phase 2: Crypto Integration (Weeks 3-4)**

**Backend:**
- [ ] Implement CCXT crypto adapters (Binance, Coinbase, Kraken)
- [ ] Create market data endpoints (ticker, orderbook, OHLCV)
- [ ] Implement WebSocket server for real-time data
- [ ] Set up Redis pub/sub for market data streaming
- [ ] Create background tasks for data collection (Celery)
- [ ] Implement rate limiting and caching

**Frontend:**
- [ ] Build market data display components
- [ ] Implement WebSocket client and hooks
- [ ] Create trading pair selector
- [ ] Build real-time price chart (TradingView Lightweight Charts)
- [ ] Create order book visualization
- [ ] Implement ticker list with search/filter

**Deliverable:** Real-time crypto market data dashboard

---

### **Phase 3: Trading Engine (Weeks 5-6)**

**Backend:**
- [ ] Integrate existing order matching engine
- [ ] Implement trading endpoints (submit, cancel, modify orders)
- [ ] Create position tracking system
- [ ] Implement order status WebSocket updates
- [ ] Add trade history logging to database
- [ ] Create balance management system
- [ ] Implement paper trading mode

**Frontend:**
- [ ] Build order entry form (Market, Limit orders)
- [ ] Create open orders table with cancel functionality
- [ ] Implement positions display with P&L
- [ ] Build trade history view
- [ ] Add order confirmations and error handling
- [ ] Create quick trade buttons

**Deliverable:** Functional paper trading interface

---

### **Phase 4: Bot System (Weeks 7-8)**

**Backend:**
- [ ] Create bot management database schema
- [ ] Implement bot CRUD endpoints
- [ ] Integrate existing ML prediction system (`_trade_management.py`)
- [ ] Create Celery tasks for bot execution
- [ ] Implement bot lifecycle management (start/stop/pause)
- [ ] Add bot performance tracking
- [ ] Create backtesting system

**Frontend:**
- [ ] Build bot list page
- [ ] Create bot creation wizard
- [ ] Implement bot configuration forms
- [ ] Build bot performance dashboard
- [ ] Add bot control interface (start/stop/pause)
- [ ] Create strategy template library

**Supported Strategies:**
- ML Prediction Bot (using existing code)
- Grid Trading Bot
- DCA Bot
- Arbitrage Bot (using existing code)

**Deliverable:** Automated trading bot system

---

### **Phase 5: Analytics (Weeks 9-10)**

**Backend:**
- [ ] Implement analytics calculation service
- [ ] Create performance metrics endpoints (Sharpe, max drawdown)
- [ ] Build equity curve data aggregation
- [ ] Implement P&L calculations by pair/strategy
- [ ] Add ML model performance tracking
- [ ] Create report generation system

**Frontend:**
- [ ] Build portfolio performance chart
- [ ] Create metrics dashboard (Sharpe, win rate, etc.)
- [ ] Implement trade distribution visualizations
- [ ] Build P&L breakdown charts
- [ ] Create ML model insights page
- [ ] Add export functionality (PDF, CSV)

**Deliverable:** Comprehensive analytics dashboard

---

### **Phase 6: Advanced Features (Weeks 11-12)**

**Backend:**
- [ ] Implement advanced order types (Stop-Loss, Take-Profit, OCO)
- [ ] Add risk management system (position limits)
- [ ] Create notification system (email, webhooks)
- [ ] Implement trade alerts and triggers
- [ ] Add API key rotation
- [ ] Create audit logging system

**Frontend:**
- [ ] Build settings page
- [ ] Implement notification preferences
- [ ] Create risk management configuration
- [ ] Add advanced charting indicators
- [ ] Build watchlist functionality
- [ ] Implement theme customization

**Deliverable:** Production-ready trading platform

---

### **Phase 7: Testing & Optimization (Weeks 13-14)**

- [ ] Write comprehensive unit tests (backend)
- [ ] Write integration tests (API endpoints)
- [ ] Implement frontend component tests (Vitest)
- [ ] Perform load testing (WebSocket connections)
- [ ] Security audit (OWASP Top 10)
- [ ] Optimize database queries
- [ ] Implement caching strategies
- [ ] Performance profiling and optimization

**Deliverable:** Tested and optimized system

---

### **Phase 8: Deployment (Week 15)**

- [ ] Set up production infrastructure (cloud provider)
- [ ] Configure CI/CD pipeline (GitHub Actions)
- [ ] Implement monitoring (Prometheus, Grafana)
- [ ] Set up logging aggregation (ELK stack)
- [ ] Configure backup systems
- [ ] Write deployment documentation
- [ ] Perform final security review

**Deliverable:** Deployed production system

---

## 10. File Structure

```
Algo-Driven-Trading/
├── backend/                          # NEW: FastAPI backend
│   ├── main.py                       # FastAPI application entry point
│   ├── config.py                     # Configuration management
│   ├── dependencies.py               # Dependency injection
│   │
│   ├── routers/                      # API route handlers
│   │   ├── auth.py                   # Authentication endpoints
│   │   ├── trading.py                # Trading endpoints
│   │   ├── market_data.py            # Market data endpoints
│   │   ├── bots.py                   # Bot management endpoints
│   │   └── analytics.py              # Analytics endpoints
│   │
│   ├── models/                       # SQLAlchemy ORM models
│   │   ├── user.py                   # User model
│   │   ├── order.py                  # Order model
│   │   ├── trade.py                  # Trade model
│   │   ├── position.py               # Position model
│   │   ├── bot.py                    # Bot model
│   │   └── market_data.py            # Market data model
│   │
│   ├── schemas/                      # Pydantic schemas
│   │   ├── auth.py                   # Auth request/response schemas
│   │   ├── trading.py                # Trading schemas
│   │   ├── market_data.py            # Market data schemas
│   │   └── bot.py                    # Bot schemas
│   │
│   ├── services/                     # Business logic layer
│   │   ├── auth_service.py           # Authentication logic
│   │   ├── trading_service.py        # Trading logic
│   │   ├── market_data_service.py    # Market data streaming
│   │   ├── bot_service.py            # Bot execution logic
│   │   └── analytics_service.py      # Analytics calculations
│   │
│   ├── adapters/                     # External API adapters
│   │   ├── crypto_adapters.py        # CCXT-based crypto adapters
│   │   ├── binance_adapter.py        # Binance specific
│   │   ├── coinbase_adapter.py       # Coinbase specific
│   │   └── kraken_adapter.py         # Kraken specific
│   │
│   ├── core/                         # Core utilities
│   │   ├── security.py               # Password hashing, JWT
│   │   ├── database.py               # Database session management
│   │   ├── redis_client.py           # Redis connection
│   │   └── websocket.py              # WebSocket handler
│   │
│   ├── tasks/                        # Celery background tasks
│   │   ├── bot_executor.py           # Bot execution tasks
│   │   ├── data_collector.py         # Market data collection
│   │   └── analytics_calculator.py   # Analytics computation
│   │
│   ├── migrations/                   # Alembic database migrations
│   │   └── versions/
│   │
│   ├── tests/                        # Backend tests
│   │   ├── test_auth.py
│   │   ├── test_trading.py
│   │   └── test_bots.py
│   │
│   └── requirements.txt              # Python dependencies
│
├── frontend/                         # NEW: React frontend
│   ├── public/                       # Static assets
│   │   └── favicon.ico
│   │
│   ├── src/
│   │   ├── main.tsx                  # React entry point
│   │   ├── App.tsx                   # Root component
│   │   │
│   │   ├── components/               # Reusable components
│   │   │   ├── ui/                   # shadcn/ui components
│   │   │   │   ├── button.tsx
│   │   │   │   ├── card.tsx
│   │   │   │   ├── dialog.tsx
│   │   │   │   └── ...
│   │   │   │
│   │   │   ├── Layout/
│   │   │   │   ├── Header.tsx
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   └── Footer.tsx
│   │   │   │
│   │   │   ├── Trading/
│   │   │   │   ├── OrderForm.tsx
│   │   │   │   ├── OrderBook.tsx
│   │   │   │   ├── PriceChart.tsx
│   │   │   │   ├── PositionsTable.tsx
│   │   │   │   └── TradeHistory.tsx
│   │   │   │
│   │   │   ├── Dashboard/
│   │   │   │   ├── PortfolioChart.tsx
│   │   │   │   ├── MarketOverview.tsx
│   │   │   │   └── SystemStatus.tsx
│   │   │   │
│   │   │   ├── Bots/
│   │   │   │   ├── BotCard.tsx
│   │   │   │   ├── BotWizard.tsx
│   │   │   │   └── BotPerformance.tsx
│   │   │   │
│   │   │   └── Analytics/
│   │   │       ├── PerformanceMetrics.tsx
│   │   │       ├── EquityCurve.tsx
│   │   │       └── PnLBreakdown.tsx
│   │   │
│   │   ├── pages/                    # Page components
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Trading.tsx
│   │   │   ├── BotManagement.tsx
│   │   │   ├── Analytics.tsx
│   │   │   ├── Settings.tsx
│   │   │   └── Login.tsx
│   │   │
│   │   ├── hooks/                    # Custom React hooks
│   │   │   ├── useAuth.ts
│   │   │   ├── useMarketData.ts
│   │   │   ├── useWebSocket.ts
│   │   │   ├── useTradingForm.ts
│   │   │   └── useBots.ts
│   │   │
│   │   ├── lib/                      # Utilities
│   │   │   ├── api.ts                # Axios instance
│   │   │   ├── socket.ts             # Socket.io client
│   │   │   ├── utils.ts              # Helper functions
│   │   │   └── constants.ts
│   │   │
│   │   ├── store/                    # State management
│   │   │   ├── authStore.ts          # Auth state (Zustand)
│   │   │   ├── marketStore.ts        # Market data state
│   │   │   └── tradingStore.ts       # Trading state
│   │   │
│   │   ├── types/                    # TypeScript types
│   │   │   ├── api.ts
│   │   │   ├── market.ts
│   │   │   ├── trading.ts
│   │   │   └── bot.ts
│   │   │
│   │   └── styles/                   # Global styles
│   │       └── globals.css
│   │
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── tailwind.config.js
│
├── existing_code/                    # EXISTING: Python trading modules
│   ├── _order_management.py          # EXISTING
│   ├── _trade_data_management.py     # EXISTING
│   ├── _trade_management.py          # EXISTING
│   ├── broker_adapters.py            # EXISTING
│   ├── data_adapters.py              # EXISTING
│   └── unit_test.py                  # EXISTING
│
├── docker/                           # NEW: Docker configuration
│   ├── backend.Dockerfile
│   ├── frontend.Dockerfile
│   └── nginx.conf
│
├── docker-compose.yml                # NEW: Local development setup
├── .env.example                      # EXISTING (update)
├── config.yaml                       # EXISTING
└── README.md                         # UPDATE
```

---

## 11. Database Schema

### PostgreSQL Tables

#### **users**
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    is_superuser BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### **exchange_credentials**
```sql
CREATE TABLE exchange_credentials (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    exchange_name VARCHAR(50) NOT NULL,  -- 'binance', 'coinbase', 'kraken'
    api_key_encrypted TEXT NOT NULL,
    api_secret_encrypted TEXT NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, exchange_name)
);
```

#### **orders**
```sql
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    exchange VARCHAR(50) NOT NULL,
    symbol VARCHAR(20) NOT NULL,          -- 'BTC/USDT'
    order_type VARCHAR(20) NOT NULL,      -- 'market', 'limit', 'stop_limit'
    side VARCHAR(10) NOT NULL,            -- 'buy', 'sell'
    amount DECIMAL(20, 8) NOT NULL,
    price DECIMAL(20, 8),
    stop_price DECIMAL(20, 8),
    status VARCHAR(20) NOT NULL,          -- OrderStatus enum
    filled_amount DECIMAL(20, 8) DEFAULT 0,
    average_price DECIMAL(20, 8),
    exchange_order_id VARCHAR(100),
    bot_id INTEGER REFERENCES bots(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_orders_user_status ON orders(user_id, status);
CREATE INDEX idx_orders_symbol ON orders(symbol);
```

#### **trades**
```sql
CREATE TABLE trades (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    exchange VARCHAR(50) NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    side VARCHAR(10) NOT NULL,
    amount DECIMAL(20, 8) NOT NULL,
    price DECIMAL(20, 8) NOT NULL,
    fee DECIMAL(20, 8),
    fee_currency VARCHAR(10),
    exchange_trade_id VARCHAR(100),
    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_trades_user_symbol ON trades(user_id, symbol);
CREATE INDEX idx_trades_executed_at ON trades(executed_at DESC);
```

#### **positions**
```sql
CREATE TABLE positions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    exchange VARCHAR(50) NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    side VARCHAR(10) NOT NULL,            -- 'long', 'short'
    amount DECIMAL(20, 8) NOT NULL,
    entry_price DECIMAL(20, 8) NOT NULL,
    current_price DECIMAL(20, 8),
    unrealized_pnl DECIMAL(20, 8),
    realized_pnl DECIMAL(20, 8) DEFAULT 0,
    opened_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, exchange, symbol)
);
```

#### **bots**
```sql
CREATE TABLE bots (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    strategy_type VARCHAR(50) NOT NULL,   -- 'ml_prediction', 'grid', 'dca', 'arbitrage'
    config JSONB NOT NULL,                -- Strategy-specific configuration
    status VARCHAR(20) NOT NULL,          -- 'running', 'paused', 'stopped'
    exchange VARCHAR(50) NOT NULL,
    symbols TEXT[] NOT NULL,              -- Array of trading pairs
    total_pnl DECIMAL(20, 8) DEFAULT 0,
    trade_count INTEGER DEFAULT 0,
    win_rate DECIMAL(5, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    stopped_at TIMESTAMP
);
```

#### **bot_trades** (TimescaleDB Hypertable)
```sql
CREATE TABLE bot_trades (
    time TIMESTAMPTZ NOT NULL,
    bot_id INTEGER REFERENCES bots(id) ON DELETE CASCADE,
    symbol VARCHAR(20) NOT NULL,
    side VARCHAR(10) NOT NULL,
    amount DECIMAL(20, 8) NOT NULL,
    price DECIMAL(20, 8) NOT NULL,
    pnl DECIMAL(20, 8),
    PRIMARY KEY (time, bot_id)
);

SELECT create_hypertable('bot_trades', 'time');
```

#### **market_data_snapshots** (TimescaleDB Hypertable)
```sql
CREATE TABLE market_data_snapshots (
    time TIMESTAMPTZ NOT NULL,
    exchange VARCHAR(50) NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    bid DECIMAL(20, 8),
    ask DECIMAL(20, 8),
    last DECIMAL(20, 8),
    volume DECIMAL(20, 8),
    PRIMARY KEY (time, exchange, symbol)
);

SELECT create_hypertable('market_data_snapshots', 'time');
CREATE INDEX idx_market_data_symbol ON market_data_snapshots(symbol, time DESC);
```

---

## 12. Testing Strategy

### Backend Testing

**Unit Tests:**
```python
# tests/test_trading_service.py
import pytest
from services.trading_service import TradingService

@pytest.mark.asyncio
async def test_submit_market_order():
    service = TradingService()
    order = await service.submit_order(
        user_id=1,
        symbol='BTC/USDT',
        side='buy',
        amount=0.001,
        order_type='market'
    )
    assert order.status == 'submitted'
    assert order.symbol == 'BTC/USDT'
```

**Integration Tests:**
```python
# tests/test_api_endpoints.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_ticker():
    response = client.get('/api/market/ticker/BTC/USDT')
    assert response.status_code == 200
    assert 'bid' in response.json()
    assert 'ask' in response.json()
```

### Frontend Testing

**Component Tests:**
```typescript
// tests/OrderForm.test.tsx
import { render, screen, fireEvent } from '@testing-library/react'
import { OrderForm } from '@/components/Trading/OrderForm'

test('submits order with correct data', async () => {
  render(<OrderForm symbol="BTC/USDT" />)

  fireEvent.change(screen.getByLabelText('Amount'), { target: { value: '0.001' } })
  fireEvent.click(screen.getByText('Buy'))

  // Assert order submission
})
```

---

## 13. Deployment Plan

### Infrastructure

**Cloud Provider Options:**
- AWS (EC2, RDS, ElastiCache)
- DigitalOcean (Droplets, Managed Databases)
- Google Cloud Platform

**Services:**
- **Web Server:** EC2 t3.medium (2 vCPU, 4GB RAM)
- **Database:** RDS PostgreSQL (db.t3.small)
- **Cache:** ElastiCache Redis (cache.t3.micro)
- **Load Balancer:** Application Load Balancer
- **CDN:** CloudFront for frontend assets

### Docker Deployment

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  frontend:
    build:
      context: ./frontend
      dockerfile: ../docker/frontend.Dockerfile
    environment:
      - VITE_API_URL=https://api.yourdomain.com

  backend:
    build:
      context: .
      dockerfile: docker/backend.Dockerfile
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - JWT_SECRET=${JWT_SECRET}
    depends_on:
      - db
      - redis

  nginx:
    image: nginx:alpine
    volumes:
      - ./docker/nginx.conf:/etc/nginx/nginx.conf
      - ./frontend/dist:/usr/share/nginx/html
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - frontend
      - backend

  db:
    image: timescale/timescaledb:latest-pg15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_PASSWORD=${DB_PASSWORD}

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### CI/CD Pipeline (GitHub Actions)

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run backend tests
        run: |
          cd backend
          pip install -r requirements.txt
          pytest
      - name: Run frontend tests
        run: |
          cd frontend
          npm install
          npm run test

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: |
          # SSH into server and pull latest code
          # Run docker-compose up -d
```

---

## Summary

This plan provides a complete roadmap for building a production-ready cryptocurrency trading platform with:

✅ **Real-time market data** from Binance, Coinbase, Kraken
✅ **Manual trading interface** with advanced order types
✅ **Automated trading bots** using ML and algorithmic strategies
✅ **Comprehensive analytics** with performance tracking
✅ **Secure architecture** with JWT auth and encrypted API keys
✅ **Scalable infrastructure** using modern tech stack
✅ **15-week implementation timeline** with clear deliverables

**Next Steps:**
1. Review and approve this plan
2. Set up development environment
3. Begin Phase 1 implementation
4. Establish regular progress checkpoints

**Public Crypto APIs:**
- Binance API (Free, 1200 req/min)
- Coinbase Advanced Trade API (Free public data)
- Kraken API (Free public endpoints)
- CCXT library for unified access to 100+ exchanges

**Sources:**
- [Best Cryptocurrency APIs of 2026 | CoinGecko API](https://www.coingecko.com/learn/best-cryptocurrency-apis)
- [GitHub - ccxt/ccxt: A cryptocurrency trading API](https://github.com/ccxt/ccxt)
- [Best Crypto APIs for Trading, Exchange Data, & More – Apipheny](https://apipheny.io/best-cryptocurrency-api/)
- [Crypto Trading API | Crypto Exchange API | Kraken](https://www.kraken.com/features/trading-api)
