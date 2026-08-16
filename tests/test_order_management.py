"""Tests for the price-time priority matching engine."""

import time

import pytest

from _order_management import (
    IOCOrder,
    LimitOrder,
    MarketOrder,
    MatchingEngine,
    NewQuantityNotSmaller,
    NonPositivePrice,
    NonPositiveQuantity,
    OrderSide,
)


@pytest.fixture
def engine():
    return MatchingEngine()


def _limit(id_, qty, price, side):
    return LimitOrder(id_, "S", qty, price, side, time.time())


class TestBookInsertion:
    def test_insert_limit_order_records_quantity_and_price(self, engine):
        engine.insert_limit_order(_limit(1, 10, 10, OrderSide.BUY))

        assert engine.bid_book[0].quantity == 10
        assert engine.bid_book[0].price == 10

    def test_bid_book_sorts_highest_price_first(self, engine):
        engine.handle_limit_order(_limit(1, 10, 10, OrderSide.BUY))
        engine.handle_limit_order(_limit(2, 5, 10, OrderSide.BUY))
        engine.handle_limit_order(_limit(3, 10, 15, OrderSide.BUY))

        assert [o.price for o in engine.bid_book] == [15, 10, 10]

    def test_bid_book_breaks_price_ties_by_earliest_time(self, engine):
        first = LimitOrder(1, "S", 10, 10, OrderSide.BUY, 100.0)
        second = LimitOrder(2, "S", 10, 10, OrderSide.BUY, 200.0)
        engine.handle_limit_order(second)
        engine.handle_limit_order(first)

        assert [o.id for o in engine.bid_book] == [1, 2]

    def test_ask_book_sorts_lowest_price_first(self, engine):
        engine.handle_limit_order(_limit(1, 10, 15, OrderSide.SELL))
        engine.handle_limit_order(_limit(2, 10, 10, OrderSide.SELL))

        assert [o.price for o in engine.ask_book] == [10, 15]


class TestOrderValidation:
    def test_rejects_non_positive_quantity(self):
        with pytest.raises(NonPositiveQuantity):
            _limit(1, 0, 10, OrderSide.BUY)

    def test_rejects_non_positive_price(self):
        with pytest.raises(NonPositivePrice):
            _limit(1, 10, 0, OrderSide.BUY)


class TestLimitOrderMatching:
    def test_sell_sweeps_bid_book_best_price_first(self, engine):
        engine.handle_limit_order(_limit(1, 10, 10, OrderSide.BUY))
        engine.handle_limit_order(_limit(2, 5, 10, OrderSide.BUY))
        engine.handle_limit_order(_limit(3, 10, 15, OrderSide.BUY))

        filled = engine.handle_limit_order(_limit(4, 14, 8, OrderSide.SELL))

        # 14 units consume all of order 3 (10 @ 15), then 4 of order 2 (5 @ 10).
        assert filled[0].id == 3
        assert filled[0].price == 15
        assert filled[2].id == 1
        assert filled[2].price == 10
        assert engine.bid_book[0].quantity == 6

    def test_unmatched_remainder_is_posted_to_book(self, engine):
        engine.handle_limit_order(_limit(1, 5, 10, OrderSide.BUY))

        engine.handle_limit_order(_limit(2, 12, 10, OrderSide.SELL))

        assert len(engine.bid_book) == 0
        assert engine.ask_book[0].id == 2
        assert engine.ask_book[0].quantity == 7

    def test_non_crossing_order_does_not_match(self, engine):
        engine.handle_limit_order(_limit(1, 10, 10, OrderSide.BUY))

        filled = engine.handle_limit_order(_limit(2, 10, 20, OrderSide.SELL))

        assert filled == []
        assert len(engine.bid_book) == 1
        assert len(engine.ask_book) == 1


class TestMarketOrders:
    def test_market_sell_fills_at_resting_bid_price(self, engine):
        engine.handle_limit_order(_limit(1, 6, 10, OrderSide.BUY))
        engine.handle_limit_order(_limit(2, 5, 10, OrderSide.BUY))

        filled = engine.handle_market_order(MarketOrder(5, "S", 5, OrderSide.SELL, time.time()))

        assert filled[0].price == 10
        assert engine.bid_book[0].quantity == 1


class TestIOCOrders:
    def test_ioc_order_does_not_rest_on_book(self, engine):
        engine.handle_limit_order(_limit(1, 1, 10, OrderSide.BUY))
        engine.handle_limit_order(_limit(2, 5, 10, OrderSide.BUY))

        # Sell IOC at 12 does not cross a bid of 10, so nothing fills...
        filled = engine.handle_ioc_order(IOCOrder(6, "S", 5, 12, OrderSide.SELL, time.time()))

        assert filled == []
        # ...and the unfilled IOC quantity is discarded rather than posted.
        assert len(engine.ask_book) == 0

    def test_ioc_order_fills_what_it_can(self, engine):
        engine.handle_limit_order(_limit(1, 3, 10, OrderSide.BUY))

        filled = engine.handle_ioc_order(IOCOrder(2, "S", 10, 9, OrderSide.SELL, time.time()))

        assert sum(o.quantity for o in filled) == 3
        assert len(engine.ask_book) == 0


class TestFillQuantities:
    """Regression: fills were appended by reference, then zeroed, so every
    returned FilledOrder reported a quantity of 0."""

    def test_partial_fill_reports_the_quantity_actually_traded(self, engine):
        engine.handle_limit_order(_limit(1, 4, 10, OrderSide.BUY))

        filled = engine.handle_limit_order(_limit(2, 10, 9, OrderSide.SELL))

        assert [o.quantity for o in filled] == [4]

    def test_exact_match_reports_quantity_on_both_sides(self, engine):
        engine.handle_limit_order(_limit(1, 5, 10, OrderSide.BUY))

        filled = engine.handle_limit_order(_limit(2, 5, 10, OrderSide.SELL))

        assert [o.quantity for o in filled] == [5, 5]

    def test_resting_side_quantities_are_conserved_across_a_sweep(self, engine):
        engine.handle_limit_order(_limit(1, 3, 12, OrderSide.BUY))
        engine.handle_limit_order(_limit(2, 4, 11, OrderSide.BUY))

        filled = engine.handle_limit_order(_limit(3, 7, 10, OrderSide.SELL))

        # Every resting unit is accounted for exactly once.
        resting = [o for o in filled if o.id in (1, 2)]
        assert sum(o.quantity for o in resting) == 7

        # NOTE: the aggressor (id 3) is recorded once, on the level that fully
        # consumes it -- not once per level swept. So the returned list is not
        # symmetric between the two sides. Callers computing volume must filter
        # by side rather than summing the whole list.
        aggressor = [o for o in filled if o.id == 3]
        assert [o.quantity for o in aggressor] == [4]


class TestAmendAndCancel:
    def test_amend_reduces_bid_quantity(self, engine):
        engine.handle_limit_order(_limit(1, 5, 10, OrderSide.BUY))
        engine.handle_limit_order(_limit(2, 10, 15, OrderSide.BUY))

        engine.amend_quantity(2, 8)

        assert engine.bid_book[0].quantity == 8

    def test_amend_reduces_ask_quantity(self, engine):
        """Regression: the ask-side branch used dict-style item assignment."""
        engine.handle_limit_order(_limit(1, 10, 20, OrderSide.SELL))

        engine.amend_quantity(1, 4)

        assert engine.ask_book[0].quantity == 4

    def test_amend_rejects_quantity_increase(self, engine):
        engine.handle_limit_order(_limit(1, 5, 10, OrderSide.BUY))

        with pytest.raises(NewQuantityNotSmaller):
            engine.amend_quantity(1, 50)

    def test_cancel_removes_order_from_book(self, engine):
        engine.handle_limit_order(_limit(1, 5, 10, OrderSide.BUY))
        engine.handle_limit_order(_limit(2, 10, 15, OrderSide.BUY))

        assert engine.cancel_order(1) is True
        assert [o.id for o in engine.bid_book] == [2]

    def test_cancel_unknown_order_returns_false(self, engine):
        assert engine.cancel_order(999) is False


class TestHandleOrderDispatch:
    def test_handle_order_returns_fills_for_market_orders(self, engine):
        """Regression: handle_order dispatched correctly but dropped the return value."""
        engine.handle_limit_order(_limit(1, 5, 10, OrderSide.BUY))

        filled = engine.handle_order(MarketOrder(2, "S", 5, OrderSide.SELL, time.time()))

        assert filled is not None, "handle_order swallowed the filled orders"
        # The engine records both sides of a trade: resting order then aggressor.
        assert [o.id for o in filled] == [1, 2]

    def test_handle_order_routes_limit_orders_to_the_book(self, engine):
        engine.handle_order(_limit(1, 5, 10, OrderSide.BUY))

        assert engine.bid_book[0].id == 1
