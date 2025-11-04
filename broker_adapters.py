"""
Broker Adapters for Order Execution

This module provides abstract base classes and concrete implementations for
executing trades through various brokers. It serves as an integration point
for future live trading implementations.

Current Status: PLACEHOLDER - No live order execution implemented
Future Implementation: Add concrete adapters for real broker APIs
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Dict, Optional
from datetime import datetime
import _order_management as om


class OrderStatus(Enum):
    """Order status enumeration."""
    PENDING = "pending"
    SUBMITTED = "submitted"
    PARTIALLY_FILLED = "partially_filled"
    FILLED = "filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"
    EXPIRED = "expired"


class BrokerAdapter(ABC):
    """
    Abstract base class for broker connections.

    All broker adapters should inherit from this class and implement
    the required methods for order submission and management.
    """

    @abstractmethod
    def connect(self) -> bool:
        """
        Establish connection to the broker.

        Returns:
            bool: True if connection successful, False otherwise
        """
        pass

    @abstractmethod
    def disconnect(self) -> bool:
        """
        Close connection to the broker.

        Returns:
            bool: True if disconnection successful, False otherwise
        """
        pass

    @abstractmethod
    def submit_order(self, order: om.Order) -> str:
        """
        Submit an order to the broker.

        Args:
            order: Order object (LimitOrder, MarketOrder, or IOCOrder)

        Returns:
            str: Broker's order ID

        Raises:
            ConnectionError: If not connected to broker
            ValueError: If order is invalid
        """
        pass

    @abstractmethod
    def cancel_order(self, order_id: str) -> bool:
        """
        Cancel an existing order.

        Args:
            order_id: Broker's order ID

        Returns:
            bool: True if cancellation successful, False otherwise
        """
        pass

    @abstractmethod
    def modify_order(self, order_id: str, new_quantity: int) -> bool:
        """
        Modify an existing order's quantity.

        Args:
            order_id: Broker's order ID
            new_quantity: New order quantity (must be smaller than original)

        Returns:
            bool: True if modification successful, False otherwise
        """
        pass

    @abstractmethod
    def get_order_status(self, order_id: str) -> Dict:
        """
        Get status of an order.

        Args:
            order_id: Broker's order ID

        Returns:
            dict: Order status with keys: status, filled_qty, remaining_qty,
                  avg_fill_price, timestamps
        """
        pass

    @abstractmethod
    def get_open_orders(self) -> List[Dict]:
        """
        Get all open orders.

        Returns:
            list: List of open orders with their details
        """
        pass

    @abstractmethod
    def get_positions(self) -> Dict[str, int]:
        """
        Get current positions.

        Returns:
            dict: Dictionary mapping symbol to position size (negative for short)
        """
        pass

    @abstractmethod
    def get_account_info(self) -> Dict:
        """
        Get account information.

        Returns:
            dict: Account info with keys: buying_power, cash, portfolio_value,
                  margin_used, etc.
        """
        pass


# =============================================================================
# CONCRETE IMPLEMENTATIONS (COMMENTED OUT - FOR FUTURE USE)
# =============================================================================

"""
# Example: Alpaca Broker Adapter
# Uncomment and install alpaca-trade-api to use: pip install alpaca-trade-api

class AlpacaBrokerAdapter(BrokerAdapter):
    def __init__(self, api_key: str, secret_key: str, base_url: str):
        import alpaca_trade_api as tradeapi
        self.api = tradeapi.REST(api_key, secret_key, base_url)
        self.connected = False

    def connect(self) -> bool:
        try:
            self.api.get_account()
            self.connected = True
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False

    def disconnect(self) -> bool:
        self.connected = False
        return True

    def submit_order(self, order: om.Order) -> str:
        if not self.connected:
            raise ConnectionError("Not connected to broker")

        # Map internal order types to Alpaca types
        if isinstance(order, om.MarketOrder):
            alpaca_order = self.api.submit_order(
                symbol=order.symbol,
                qty=order.quantity,
                side='buy' if order.side == om.OrderSide.BUY else 'sell',
                type='market',
                time_in_force='day'
            )
        elif isinstance(order, om.LimitOrder):
            alpaca_order = self.api.submit_order(
                symbol=order.symbol,
                qty=order.quantity,
                side='buy' if order.side == om.OrderSide.BUY else 'sell',
                type='limit',
                limit_price=order.price,
                time_in_force='day'
            )
        elif isinstance(order, om.IOCOrder):
            alpaca_order = self.api.submit_order(
                symbol=order.symbol,
                qty=order.quantity,
                side='buy' if order.side == om.OrderSide.BUY else 'sell',
                type='limit',
                limit_price=order.price,
                time_in_force='ioc'
            )
        else:
            raise ValueError(f"Unsupported order type: {type(order)}")

        return alpaca_order.id

    def cancel_order(self, order_id: str) -> bool:
        try:
            self.api.cancel_order(order_id)
            return True
        except Exception as e:
            print(f"Cancel failed: {e}")
            return False

    def modify_order(self, order_id: str, new_quantity: int) -> bool:
        try:
            self.api.replace_order(order_id, qty=new_quantity)
            return True
        except Exception as e:
            print(f"Modify failed: {e}")
            return False

    def get_order_status(self, order_id: str) -> Dict:
        order = self.api.get_order(order_id)
        return {
            'status': order.status,
            'filled_qty': int(order.filled_qty),
            'remaining_qty': int(order.qty) - int(order.filled_qty),
            'avg_fill_price': float(order.filled_avg_price) if order.filled_avg_price else None,
            'submitted_at': order.submitted_at,
            'filled_at': order.filled_at
        }

    def get_open_orders(self) -> List[Dict]:
        orders = self.api.list_orders(status='open')
        return [{'order_id': o.id, 'symbol': o.symbol, 'qty': o.qty,
                 'side': o.side, 'type': o.type} for o in orders]

    def get_positions(self) -> Dict[str, int]:
        positions = self.api.list_positions()
        return {p.symbol: int(p.qty) for p in positions}

    def get_account_info(self) -> Dict:
        account = self.api.get_account()
        return {
            'buying_power': float(account.buying_power),
            'cash': float(account.cash),
            'portfolio_value': float(account.portfolio_value),
            'equity': float(account.equity)
        }
"""

"""
# Example: Interactive Brokers Broker Adapter
# Uncomment and install ib_insync to use: pip install ib_insync

class InteractiveBrokersBrokerAdapter(BrokerAdapter):
    def __init__(self, host: str = '127.0.0.1', port: int = 7497, client_id: int = 1):
        from ib_insync import IB
        self.ib = IB()
        self.host = host
        self.port = port
        self.client_id = client_id
        self.connected = False
        self.orders = {}  # Track submitted orders

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

    def submit_order(self, order: om.Order) -> str:
        from ib_insync import Stock, Order as IBOrder

        if not self.connected:
            raise ConnectionError("Not connected to broker")

        # Create IB contract
        contract = Stock(order.symbol, 'SMART', 'USD')
        self.ib.qualifyContracts(contract)

        # Map internal order to IB order
        action = 'BUY' if order.side == om.OrderSide.BUY else 'SELL'

        if isinstance(order, om.MarketOrder):
            ib_order = IBOrder(action, order.quantity, 'MKT')
        elif isinstance(order, om.LimitOrder):
            ib_order = IBOrder(action, order.quantity, 'LMT', lmtPrice=order.price)
        elif isinstance(order, om.IOCOrder):
            ib_order = IBOrder(action, order.quantity, 'LMT', lmtPrice=order.price)
            ib_order.tif = 'IOC'
        else:
            raise ValueError(f"Unsupported order type: {type(order)}")

        # Submit order
        trade = self.ib.placeOrder(contract, ib_order)
        self.orders[trade.order.orderId] = trade

        return str(trade.order.orderId)

    def cancel_order(self, order_id: str) -> bool:
        try:
            trade = self.orders.get(int(order_id))
            if trade:
                self.ib.cancelOrder(trade.order)
                return True
            return False
        except Exception as e:
            print(f"Cancel failed: {e}")
            return False

    def modify_order(self, order_id: str, new_quantity: int) -> bool:
        try:
            trade = self.orders.get(int(order_id))
            if trade:
                trade.order.totalQuantity = new_quantity
                self.ib.placeOrder(trade.contract, trade.order)
                return True
            return False
        except Exception as e:
            print(f"Modify failed: {e}")
            return False

    def get_order_status(self, order_id: str) -> Dict:
        trade = self.orders.get(int(order_id))
        if not trade:
            return {'status': 'not_found'}

        return {
            'status': trade.orderStatus.status,
            'filled_qty': trade.orderStatus.filled,
            'remaining_qty': trade.orderStatus.remaining,
            'avg_fill_price': trade.orderStatus.avgFillPrice
        }

    def get_open_orders(self) -> List[Dict]:
        trades = self.ib.openTrades()
        return [{'order_id': str(t.order.orderId), 'symbol': t.contract.symbol,
                 'qty': t.order.totalQuantity, 'action': t.order.action}
                for t in trades]

    def get_positions(self) -> Dict[str, int]:
        positions = self.ib.positions()
        return {p.contract.symbol: int(p.position) for p in positions}

    def get_account_info(self) -> Dict:
        account_values = self.ib.accountValues()
        info = {}
        for av in account_values:
            if av.tag == 'BuyingPower':
                info['buying_power'] = float(av.value)
            elif av.tag == 'TotalCashValue':
                info['cash'] = float(av.value)
            elif av.tag == 'NetLiquidation':
                info['portfolio_value'] = float(av.value)
        return info
"""


class SimulatedBrokerAdapter(BrokerAdapter):
    """
    Simulated broker for paper trading and backtesting.

    This adapter uses the internal MatchingEngine to simulate order execution
    without connecting to a real broker. Useful for testing strategies.
    """

    def __init__(self):
        """Initialize simulated broker with internal matching engine."""
        self.engine = om.MatchingEngine()
        self.connected = False
        self.order_counter = 0
        self.submitted_orders = {}  # Map order_id to order object
        self.order_status = {}  # Map order_id to status
        self.positions = {}  # Map symbol to quantity
        self.cash = 100000.0  # Starting cash
        self.fills = []  # List of filled orders

    def connect(self) -> bool:
        """Connect to simulated broker (always succeeds)."""
        self.connected = True
        print("Connected to simulated broker")
        return True

    def disconnect(self) -> bool:
        """Disconnect from simulated broker."""
        self.connected = False
        print("Disconnected from simulated broker")
        return True

    def submit_order(self, order: om.Order) -> str:
        """
        Submit order to simulated matching engine.

        Args:
            order: Order object to submit

        Returns:
            str: Simulated order ID
        """
        if not self.connected:
            raise ConnectionError("Not connected to broker")

        # Generate order ID
        self.order_counter += 1
        order_id = f"SIM{self.order_counter:06d}"

        # Store order
        self.submitted_orders[order_id] = order
        self.order_status[order_id] = OrderStatus.SUBMITTED

        # Submit to matching engine
        try:
            filled_orders = self.engine.handle_order(order)

            # Process fills
            if filled_orders:
                self.order_status[order_id] = OrderStatus.FILLED
                self.fills.extend(filled_orders)

                # Update positions
                for fill in filled_orders:
                    qty_change = fill.quantity if fill.side == om.OrderSide.BUY else -fill.quantity
                    self.positions[fill.symbol] = self.positions.get(fill.symbol, 0) + qty_change

                    # Update cash (simplified, doesn't account for commissions)
                    cash_change = -fill.quantity * fill.price if fill.side == om.OrderSide.BUY else fill.quantity * fill.price
                    self.cash += cash_change
            else:
                # Check if order is resting in book or was rejected
                if isinstance(order, om.LimitOrder):
                    self.order_status[order_id] = OrderStatus.PENDING
                elif isinstance(order, om.IOCOrder):
                    self.order_status[order_id] = OrderStatus.CANCELLED

            print(f"Order {order_id} submitted: {order.symbol} {order.side.name} "
                  f"{order.quantity} @ {getattr(order, 'price', 'MARKET')}")

            return order_id

        except Exception as e:
            self.order_status[order_id] = OrderStatus.REJECTED
            print(f"Order {order_id} rejected: {e}")
            return order_id

    def cancel_order(self, order_id: str) -> bool:
        """Cancel an order in the simulated broker."""
        if order_id not in self.submitted_orders:
            return False

        order = self.submitted_orders[order_id]
        success = self.engine.cancel_order(order.id)

        if success:
            self.order_status[order_id] = OrderStatus.CANCELLED
            print(f"Order {order_id} cancelled")
            return True

        return False

    def modify_order(self, order_id: str, new_quantity: int) -> bool:
        """Modify an order in the simulated broker."""
        if order_id not in self.submitted_orders:
            return False

        order = self.submitted_orders[order_id]
        try:
            self.engine.amend_quantity(order.id, new_quantity)
            print(f"Order {order_id} modified to quantity {new_quantity}")
            return True
        except Exception as e:
            print(f"Modify failed: {e}")
            return False

    def get_order_status(self, order_id: str) -> Dict:
        """Get order status from simulated broker."""
        if order_id not in self.submitted_orders:
            return {'status': OrderStatus.REJECTED.value, 'error': 'Order not found'}

        order = self.submitted_orders[order_id]
        status = self.order_status.get(order_id, OrderStatus.PENDING)

        # Calculate filled quantity (simplified)
        filled_qty = order.quantity if status == OrderStatus.FILLED else 0

        return {
            'status': status.value,
            'filled_qty': filled_qty,
            'remaining_qty': order.quantity - filled_qty,
            'avg_fill_price': getattr(order, 'price', None),
            'submitted_at': datetime.fromtimestamp(order.time)
        }

    def get_open_orders(self) -> List[Dict]:
        """Get all open orders in simulated broker."""
        open_orders = []
        for order_id, status in self.order_status.items():
            if status in [OrderStatus.PENDING, OrderStatus.SUBMITTED, OrderStatus.PARTIALLY_FILLED]:
                order = self.submitted_orders[order_id]
                open_orders.append({
                    'order_id': order_id,
                    'symbol': order.symbol,
                    'qty': order.quantity,
                    'side': order.side.name,
                    'type': order.type.name,
                    'price': getattr(order, 'price', None)
                })
        return open_orders

    def get_positions(self) -> Dict[str, int]:
        """Get current positions in simulated broker."""
        return self.positions.copy()

    def get_account_info(self) -> Dict:
        """Get account information from simulated broker."""
        # Calculate portfolio value (simplified)
        portfolio_value = self.cash
        # In a real implementation, would need current market prices to value positions

        return {
            'buying_power': self.cash,
            'cash': self.cash,
            'portfolio_value': portfolio_value,
            'positions_count': len(self.positions),
            'orders_submitted': self.order_counter,
            'fills_count': len(self.fills)
        }


# =============================================================================
# FACTORY FUNCTION
# =============================================================================

def create_broker_adapter(adapter_type: str, **kwargs) -> BrokerAdapter:
    """
    Factory function to create appropriate broker adapter.

    Args:
        adapter_type: Type of adapter ('simulated', 'alpaca', 'ib')
        **kwargs: Configuration parameters for the adapter

    Returns:
        BrokerAdapter: Configured broker adapter instance

    Example:
        >>> broker = create_broker_adapter('simulated')
        >>> broker.connect()
    """
    if adapter_type.lower() == 'simulated':
        return SimulatedBrokerAdapter()

    # Uncomment when implementing live brokers
    # elif adapter_type.lower() == 'alpaca':
    #     return AlpacaBrokerAdapter(
    #         api_key=kwargs['api_key'],
    #         secret_key=kwargs['secret_key'],
    #         base_url=kwargs.get('base_url', 'https://paper-api.alpaca.markets')
    #     )
    # elif adapter_type.lower() == 'ib':
    #     return InteractiveBrokersBrokerAdapter(
    #         host=kwargs.get('host', '127.0.0.1'),
    #         port=kwargs.get('port', 7497),
    #         client_id=kwargs.get('client_id', 1)
    #     )

    else:
        raise ValueError(
            f"Unknown adapter type: {adapter_type}. "
            f"Supported types: 'simulated' (currently), 'alpaca', 'ib' (future)"
        )
