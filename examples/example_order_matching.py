"""
Example: Order Matching Engine Usage

This script demonstrates how to use the order matching engine to simulate
order book dynamics and trade execution.
"""

import time
import sys
sys.path.append('..')  # Add parent directory to path

from _order_management import (
    MatchingEngine,
    LimitOrder,
    MarketOrder,
    IOCOrder,
    OrderSide
)


def main():
    print("=" * 70)
    print("ORDER MATCHING ENGINE EXAMPLE")
    print("=" * 70)
    print()

    # Create matching engine
    engine = MatchingEngine()
    print("✓ Created matching engine")
    print()

    # Example 1: Submit buy limit orders
    print("--- Example 1: Building the order book ---")
    print()

    buy_orders = [
        LimitOrder(1, "AAPL", 100, 150.50, OrderSide.BUY, time.time()),
        LimitOrder(2, "AAPL", 200, 150.25, OrderSide.BUY, time.time()),
        LimitOrder(3, "AAPL", 150, 150.00, OrderSide.BUY, time.time()),
    ]

    for order in buy_orders:
        engine.handle_limit_order(order)
        print(f"✓ Added BUY order: ID={order.id}, Price=${order.price:.2f}, "
              f"Qty={order.quantity}")

    print()
    print(f"Bid book depth: {len(engine.bid_book)} orders")
    print()

    # Example 2: Submit sell limit orders (no crossing)
    print("--- Example 2: Adding sell orders (no match) ---")
    print()

    sell_orders = [
        LimitOrder(4, "AAPL", 100, 151.00, OrderSide.SELL, time.time()),
        LimitOrder(5, "AAPL", 150, 151.25, OrderSide.SELL, time.time()),
        LimitOrder(6, "AAPL", 200, 151.50, OrderSide.SELL, time.time()),
    ]

    for order in sell_orders:
        engine.handle_limit_order(order)
        print(f"✓ Added SELL order: ID={order.id}, Price=${order.price:.2f}, "
              f"Qty={order.quantity}")

    print()
    print(f"Ask book depth: {len(engine.ask_book)} orders")
    print()

    # Display current order books
    print("--- Current Order Books ---")
    print()
    print("BID BOOK (sorted by price desc, time asc):")
    for i, order in enumerate(engine.bid_book[:5], 1):
        print(f"  {i}. ID={order.id}, Price=${order.price:.2f}, "
              f"Qty={order.quantity}, Side={order.side.name}")

    print()
    print("ASK BOOK (sorted by price asc, time desc):")
    for i, order in enumerate(engine.ask_book[:5], 1):
        print(f"  {i}. ID={order.id}, Price=${order.price:.2f}, "
              f"Qty={order.quantity}, Side={order.side.name}")
    print()

    # Example 3: Market order execution
    print("--- Example 3: Market order (matches immediately) ---")
    print()

    market_order = MarketOrder(7, "AAPL", 50, OrderSide.BUY, time.time())
    print(f"Submitting market BUY order: Qty={market_order.quantity}")

    filled_orders = engine.handle_market_order(market_order)

    print(f"✓ Market order executed, {len(filled_orders)} fills")
    for fill in filled_orders:
        print(f"  - Filled {fill.quantity} @ ${fill.price:.2f}")

    print()
    print(f"Ask book depth after market order: {len(engine.ask_book)} orders")
    print()

    # Example 4: Limit order that crosses (partial fill)
    print("--- Example 4: Limit order with crossing (partial fill) ---")
    print()

    crossing_order = LimitOrder(8, "AAPL", 300, 151.20, OrderSide.BUY, time.time())
    print(f"Submitting BUY limit order: Price=${crossing_order.price:.2f}, "
          f"Qty={crossing_order.quantity}")
    print(f"This will match with ask orders <= ${crossing_order.price:.2f}")
    print()

    filled_orders = engine.handle_limit_order(crossing_order)

    if filled_orders:
        print(f"✓ Order partially filled, {len(filled_orders)} executions")
        total_filled = sum(f.quantity for f in filled_orders if f.id == crossing_order.id)
        print(f"  Total filled: {total_filled} shares")
        print(f"  Remaining: {crossing_order.quantity} shares (now in bid book)")
    else:
        print("✓ Order added to book (no immediate match)")

    print()

    # Example 5: IOC order (Immediate-or-Cancel)
    print("--- Example 5: IOC order (fills what it can, cancels rest) ---")
    print()

    ioc_order = IOCOrder(9, "AAPL", 500, 152.00, OrderSide.BUY, time.time())
    print(f"Submitting IOC BUY order: Price=${ioc_order.price:.2f}, "
          f"Qty={ioc_order.quantity}")
    print(f"Will fill what's available, cancel remainder")
    print()

    filled_orders = engine.handle_ioc_order(ioc_order)

    if filled_orders:
        total_filled = sum(f.quantity for f in filled_orders if f.id == ioc_order.id)
        print(f"✓ IOC order filled: {total_filled} shares")
        print(f"  Cancelled: {ioc_order.quantity} shares")
    else:
        print("✓ IOC order fully cancelled (no matches)")

    print()

    # Example 6: Order amendment
    print("--- Example 6: Amend order quantity ---")
    print()

    # Find an order in the book
    if engine.bid_book:
        order_to_amend = engine.bid_book[0]
        original_qty = order_to_amend.quantity
        new_qty = original_qty // 2

        print(f"Amending order ID={order_to_amend.id}")
        print(f"  Original quantity: {original_qty}")
        print(f"  New quantity: {new_qty}")

        engine.amend_quantity(order_to_amend.id, new_qty)

        print(f"✓ Order amended successfully")
        print(f"  Current quantity: {order_to_amend.quantity}")
    else:
        print("No orders available to amend")

    print()

    # Example 7: Order cancellation
    print("--- Example 7: Cancel order ---")
    print()

    if engine.ask_book:
        order_to_cancel = engine.ask_book[0]
        print(f"Cancelling order ID={order_to_cancel.id}")

        success = engine.cancel_order(order_to_cancel.id)

        if success:
            print(f"✓ Order cancelled successfully")
            print(f"  Ask book depth: {len(engine.ask_book)} orders")
        else:
            print("✗ Order not found")
    else:
        print("No orders available to cancel")

    print()

    # Final summary
    print("=" * 70)
    print("FINAL STATE")
    print("=" * 70)
    print(f"Bid book: {len(engine.bid_book)} orders")
    print(f"Ask book: {len(engine.ask_book)} orders")
    print()
    print("Example complete!")
    print()


if __name__ == "__main__":
    main()
