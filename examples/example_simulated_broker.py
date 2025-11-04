"""
Example: Simulated Broker Usage

This script demonstrates how to use the simulated broker adapter for
paper trading and testing strategies without risking real money.
"""

import time
import sys
sys.path.append('..')  # Add parent directory to path

from _order_management import LimitOrder, MarketOrder, OrderSide
from broker_adapters import create_broker_adapter


def main():
    print("=" * 70)
    print("SIMULATED BROKER EXAMPLE")
    print("=" * 70)
    print()

    # Create and connect to simulated broker
    print("--- Connecting to Simulated Broker ---")
    broker = create_broker_adapter('simulated')
    broker.connect()
    print()

    # Check initial account info
    print("--- Initial Account Information ---")
    account = broker.get_account_info()
    print(f"Cash: ${account['cash']:,.2f}")
    print(f"Portfolio Value: ${account['portfolio_value']:,.2f}")
    print(f"Buying Power: ${account['buying_power']:,.2f}")
    print()

    # Submit some orders
    print("--- Submitting Orders ---")
    print()

    orders = []

    # Order 1: Buy limit order
    order1 = LimitOrder(1, "AAPL", 100, 150.00, OrderSide.BUY, time.time())
    order_id1 = broker.submit_order(order1)
    orders.append(order_id1)
    print(f"Order 1: {order_id1}")

    # Order 2: Another buy limit order at different price
    order2 = LimitOrder(2, "AAPL", 50, 149.50, OrderSide.BUY, time.time())
    order_id2 = broker.submit_order(order2)
    orders.append(order_id2)
    print(f"Order 2: {order_id2}")

    # Order 3: Sell limit order (will match if crossed)
    order3 = LimitOrder(3, "AAPL", 75, 150.50, OrderSide.SELL, time.time())
    order_id3 = broker.submit_order(order3)
    orders.append(order_id3)
    print(f"Order 3: {order_id3}")
    print()

    # Check order statuses
    print("--- Order Statuses ---")
    for order_id in orders:
        status = broker.get_order_status(order_id)
        print(f"{order_id}: {status['status'].upper()}")
        if status['filled_qty'] > 0:
            print(f"  Filled: {status['filled_qty']} @ ${status['avg_fill_price']:.2f}")
    print()

    # Submit a market order that will execute
    print("--- Market Order Execution ---")
    market_order = MarketOrder(4, "AAPL", 30, OrderSide.SELL, time.time())
    order_id4 = broker.submit_order(market_order)
    print(f"Order 4 (Market): {order_id4}")
    print()

    status = broker.get_order_status(order_id4)
    print(f"Status: {status['status'].upper()}")
    if status['filled_qty'] > 0:
        print(f"Filled: {status['filled_qty']} shares @ ${status['avg_fill_price']:.2f}")
    print()

    # Check positions
    print("--- Current Positions ---")
    positions = broker.get_positions()
    if positions:
        for symbol, qty in positions.items():
            position_type = "LONG" if qty > 0 else "SHORT"
            print(f"{symbol}: {abs(qty)} shares ({position_type})")
    else:
        print("No positions")
    print()

    # View open orders
    print("--- Open Orders ---")
    open_orders = broker.get_open_orders()
    if open_orders:
        for order in open_orders:
            print(f"Order {order['order_id']}: {order['symbol']} "
                  f"{order['side']} {order['qty']} @ {order['price']}")
    else:
        print("No open orders")
    print()

    # Modify an order
    print("--- Modifying Order ---")
    if open_orders:
        first_order = open_orders[0]
        order_id = first_order['order_id']
        original_qty = first_order['qty']
        new_qty = original_qty // 2

        print(f"Modifying {order_id}: {original_qty} → {new_qty} shares")
        success = broker.modify_order(order_id, new_qty)

        if success:
            print("✓ Order modified successfully")
        else:
            print("✗ Modification failed")
    print()

    # Cancel an order
    print("--- Cancelling Order ---")
    if open_orders:
        last_order = open_orders[-1]
        order_id = last_order['order_id']

        print(f"Cancelling {order_id}")
        success = broker.cancel_order(order_id)

        if success:
            print("✓ Order cancelled successfully")
        else:
            print("✗ Cancellation failed")
    print()

    # Final account summary
    print("=" * 70)
    print("FINAL ACCOUNT SUMMARY")
    print("=" * 70)
    account = broker.get_account_info()
    print(f"Cash: ${account['cash']:,.2f}")
    print(f"Portfolio Value: ${account['portfolio_value']:,.2f}")
    print(f"Orders Submitted: {account['orders_submitted']}")
    print(f"Fills: {account['fills_count']}")
    print()

    positions = broker.get_positions()
    if positions:
        print("Positions:")
        for symbol, qty in positions.items():
            position_type = "LONG" if qty > 0 else "SHORT"
            print(f"  {symbol}: {abs(qty)} shares ({position_type})")
    else:
        print("No positions held")

    print()

    # Disconnect
    broker.disconnect()
    print("Disconnected from simulated broker")
    print()
    print("Example complete!")
    print()


if __name__ == "__main__":
    main()
