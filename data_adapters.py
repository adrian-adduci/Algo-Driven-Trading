"""
Data Adapters for Market Data Integration

This module provides abstract base classes and concrete implementations for
fetching market data from various sources. It serves as an integration point
for future live trading implementations.

Current Status: PLACEHOLDER - No live data integration implemented
Future Implementation: Add concrete adapters for real-time market data APIs
"""

from abc import ABC, abstractmethod
import pandas as pd
from typing import List, Dict, Optional
from datetime import datetime


class MarketDataAdapter(ABC):
    """
    Abstract base class for market data providers.

    All market data adapters should inherit from this class and implement
    the required methods for fetching stock and options data.
    """

    @abstractmethod
    def connect(self) -> bool:
        """
        Establish connection to the data provider.

        Returns:
            bool: True if connection successful, False otherwise
        """
        pass

    @abstractmethod
    def disconnect(self) -> bool:
        """
        Close connection to the data provider.

        Returns:
            bool: True if disconnection successful, False otherwise
        """
        pass

    @abstractmethod
    def get_stock_quote(self, symbol: str) -> Dict:
        """
        Get real-time stock quote.

        Args:
            symbol: Stock ticker symbol

        Returns:
            dict: Quote data with keys: bid_price, bid_volume, ask_price,
                  ask_volume, last_price, timestamp
        """
        pass

    @abstractmethod
    def get_options_chain(self, symbol: str, expiration_date: str) -> pd.DataFrame:
        """
        Get options chain for a given stock and expiration date.

        Args:
            symbol: Underlying stock ticker symbol
            expiration_date: Option expiration date (YYYY-MM-DD)

        Returns:
            pd.DataFrame: Options chain with columns for strike, call_bid,
                         call_ask, put_bid, put_ask, etc.
        """
        pass

    @abstractmethod
    def get_historical_data(self, symbol: str, start_date: str, end_date: str,
                           timeframe: str = '1Min') -> pd.DataFrame:
        """
        Get historical market data.

        Args:
            symbol: Ticker symbol
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            timeframe: Data frequency ('1Min', '5Min', '1H', '1D')

        Returns:
            pd.DataFrame: Historical data with OHLCV columns
        """
        pass

    @abstractmethod
    def subscribe_realtime(self, symbols: List[str], callback) -> bool:
        """
        Subscribe to real-time data stream.

        Args:
            symbols: List of ticker symbols to subscribe to
            callback: Function to call when new data arrives

        Returns:
            bool: True if subscription successful
        """
        pass


# =============================================================================
# CONCRETE IMPLEMENTATIONS (COMMENTED OUT - FOR FUTURE USE)
# =============================================================================

"""
# Example: Alpaca Market Data Adapter
# Uncomment and install alpaca-trade-api to use: pip install alpaca-trade-api

class AlpacaDataAdapter(MarketDataAdapter):
    def __init__(self, api_key: str, secret_key: str, base_url: str):
        import alpaca_trade_api as tradeapi
        self.api = tradeapi.REST(api_key, secret_key, base_url)
        self.connected = False

    def connect(self) -> bool:
        try:
            # Test connection
            self.api.get_account()
            self.connected = True
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False

    def disconnect(self) -> bool:
        self.connected = False
        return True

    def get_stock_quote(self, symbol: str) -> Dict:
        quote = self.api.get_latest_quote(symbol)
        return {
            'bid_price': quote.bp,
            'bid_volume': quote.bs,
            'ask_price': quote.ap,
            'ask_volume': quote.as_,
            'timestamp': quote.t
        }

    def get_options_chain(self, symbol: str, expiration_date: str) -> pd.DataFrame:
        # Note: Alpaca does not currently support options trading
        raise NotImplementedError("Alpaca does not support options data")

    def get_historical_data(self, symbol: str, start_date: str, end_date: str,
                           timeframe: str = '1Min') -> pd.DataFrame:
        barset = self.api.get_bars(symbol, timeframe, start=start_date, end=end_date)
        df = barset.df
        return df

    def subscribe_realtime(self, symbols: List[str], callback) -> bool:
        # Implement using Alpaca's streaming API
        pass
"""

"""
# Example: Interactive Brokers Data Adapter
# Uncomment and install ib_insync to use: pip install ib_insync

class InteractiveBrokersDataAdapter(MarketDataAdapter):
    def __init__(self, host: str = '127.0.0.1', port: int = 7497, client_id: int = 1):
        from ib_insync import IB, Stock, Option
        self.ib = IB()
        self.host = host
        self.port = port
        self.client_id = client_id
        self.connected = False

    def connect(self) -> bool:
        try:
            self.ib.connect(self.host, self.port, clientId=self.client_id)
            self.connected = True
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False

    def disconnect(self) -> bool:
        if self.connected:
            self.ib.disconnect()
            self.connected = False
        return True

    def get_stock_quote(self, symbol: str) -> Dict:
        from ib_insync import Stock
        stock = Stock(symbol, 'SMART', 'USD')
        self.ib.qualifyContracts(stock)
        ticker = self.ib.reqMktData(stock)
        self.ib.sleep(1)  # Wait for data

        return {
            'bid_price': ticker.bid,
            'bid_volume': ticker.bidSize,
            'ask_price': ticker.ask,
            'ask_volume': ticker.askSize,
            'last_price': ticker.last,
            'timestamp': datetime.now()
        }

    def get_options_chain(self, symbol: str, expiration_date: str) -> pd.DataFrame:
        from ib_insync import Stock
        stock = Stock(symbol, 'SMART', 'USD')
        self.ib.qualifyContracts(stock)
        chains = self.ib.reqSecDefOptParams(stock.symbol, '', stock.secType, stock.conId)

        # Process chains and return DataFrame
        # Implementation details depend on your specific requirements
        pass

    def get_historical_data(self, symbol: str, start_date: str, end_date: str,
                           timeframe: str = '1Min') -> pd.DataFrame:
        from ib_insync import Stock
        stock = Stock(symbol, 'SMART', 'USD')
        self.ib.qualifyContracts(stock)

        bars = self.ib.reqHistoricalData(
            stock,
            endDateTime=end_date,
            durationStr='1 D',
            barSizeSetting=timeframe,
            whatToShow='TRADES',
            useRTH=True
        )

        df = pd.DataFrame(bars)
        return df

    def subscribe_realtime(self, symbols: List[str], callback) -> bool:
        # Implement using IB's streaming ticker data
        pass
"""

"""
# Example: Polygon.io Data Adapter
# Uncomment and install polygon to use: pip install polygon-api-client

class PolygonDataAdapter(MarketDataAdapter):
    def __init__(self, api_key: str):
        from polygon import RESTClient
        self.client = RESTClient(api_key)
        self.connected = True  # REST API doesn't require explicit connection

    def connect(self) -> bool:
        return True

    def disconnect(self) -> bool:
        return True

    def get_stock_quote(self, symbol: str) -> Dict:
        quote = self.client.get_last_quote(symbol)
        return {
            'bid_price': quote.bid_price,
            'bid_volume': quote.bid_size,
            'ask_price': quote.ask_price,
            'ask_volume': quote.ask_size,
            'timestamp': quote.sip_timestamp
        }

    def get_options_chain(self, symbol: str, expiration_date: str) -> pd.DataFrame:
        # Use Polygon's options API
        contracts = self.client.list_options_contracts(
            underlying_ticker=symbol,
            expiration_date=expiration_date
        )
        # Process and return as DataFrame
        pass

    def get_historical_data(self, symbol: str, start_date: str, end_date: str,
                           timeframe: str = '1Min') -> pd.DataFrame:
        bars = self.client.get_aggs(
            symbol,
            1,
            'minute' if 'Min' in timeframe else 'day',
            start_date,
            end_date
        )
        df = pd.DataFrame(bars)
        return df

    def subscribe_realtime(self, symbols: List[str], callback) -> bool:
        # Use Polygon's WebSocket API for streaming
        pass
"""


class CSVDataAdapter(MarketDataAdapter):
    """
    CSV file-based data adapter for backtesting and development.

    This is the current implementation used by the system. It reads
    market data from CSV files instead of live API sources.
    """

    def __init__(self, filename: str):
        """
        Initialize CSV data adapter.

        Args:
            filename: Path to CSV file containing market data
        """
        self.filename = filename
        self.data = None
        self.connected = False

    def connect(self) -> bool:
        """Load data from CSV file."""
        try:
            self.data = pd.read_csv(self.filename, index_col=0)
            self.connected = True
            return True
        except Exception as e:
            print(f"Failed to load CSV file: {e}")
            return False

    def disconnect(self) -> bool:
        """Clear loaded data."""
        self.data = None
        self.connected = False
        return True

    def get_stock_quote(self, symbol: str) -> Dict:
        """
        Get stock quote from CSV data (returns first row).

        Note: This is a simplified implementation for backtesting.
        """
        if self.data is None or not self.connected:
            raise ConnectionError("Not connected. Call connect() first.")

        # Extract stock columns
        stock_cols = [col for col in self.data.columns if 'Stock' in col]
        first_row = self.data[stock_cols].iloc[0]

        return {
            'bid_price': first_row.get('BidPrice-Stock', 0),
            'bid_volume': first_row.get('BidVolume-Stock', 0),
            'ask_price': first_row.get('AskPrice-Stock', 0),
            'ask_volume': first_row.get('AskVolume-Stock', 0),
            'timestamp': self.data.index[0]
        }

    def get_options_chain(self, symbol: str, expiration_date: str) -> pd.DataFrame:
        """
        Get options chain from CSV data.

        Note: This returns all options data from the CSV file.
        """
        if self.data is None or not self.connected:
            raise ConnectionError("Not connected. Call connect() first.")

        # Extract option columns
        option_cols = [col for col in self.data.columns
                      if '-P' in col or '-C' in col]
        return self.data[option_cols]

    def get_historical_data(self, symbol: str, start_date: str, end_date: str,
                           timeframe: str = '1Min') -> pd.DataFrame:
        """
        Get historical data from CSV file.

        Returns all data from the CSV file (date filtering not implemented).
        """
        if self.data is None or not self.connected:
            raise ConnectionError("Not connected. Call connect() first.")

        return self.data.copy()

    def subscribe_realtime(self, symbols: List[str], callback) -> bool:
        """
        Not supported for CSV adapter.

        Raises:
            NotImplementedError: CSV files don't support real-time streaming
        """
        raise NotImplementedError(
            "CSV adapter does not support real-time data streaming. "
            "Use a live data adapter (Alpaca, IB, Polygon, etc.) for real-time data."
        )


# =============================================================================
# FACTORY FUNCTION
# =============================================================================

def create_data_adapter(adapter_type: str, **kwargs) -> MarketDataAdapter:
    """
    Factory function to create appropriate data adapter.

    Args:
        adapter_type: Type of adapter ('csv', 'alpaca', 'ib', 'polygon')
        **kwargs: Configuration parameters for the adapter

    Returns:
        MarketDataAdapter: Configured data adapter instance

    Example:
        >>> adapter = create_data_adapter('csv', filename='data/market_data.csv')
        >>> adapter.connect()
    """
    if adapter_type.lower() == 'csv':
        return CSVDataAdapter(kwargs.get('filename', 'data/market_data.csv'))

    # Uncomment when implementing live adapters
    # elif adapter_type.lower() == 'alpaca':
    #     return AlpacaDataAdapter(
    #         api_key=kwargs['api_key'],
    #         secret_key=kwargs['secret_key'],
    #         base_url=kwargs.get('base_url', 'https://paper-api.alpaca.markets')
    #     )
    # elif adapter_type.lower() == 'ib':
    #     return InteractiveBrokersDataAdapter(
    #         host=kwargs.get('host', '127.0.0.1'),
    #         port=kwargs.get('port', 7497),
    #         client_id=kwargs.get('client_id', 1)
    #     )
    # elif adapter_type.lower() == 'polygon':
    #     return PolygonDataAdapter(api_key=kwargs['api_key'])

    else:
        raise ValueError(
            f"Unknown adapter type: {adapter_type}. "
            f"Supported types: 'csv' (currently), 'alpaca', 'ib', 'polygon' (future)"
        )
