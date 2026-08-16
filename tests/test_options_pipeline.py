"""Tests for the options data pipeline and arbitrage strategy."""

import pandas as pd
import pytest

import _trade_data_management as tdm

ALL_OPTIONS = ["P60", "P70", "P80", "C60", "C70", "C80"]


class TestReadData:
    def test_splits_time_to_expiry_from_market_data(self, raw_market_data):
        time_to_expiry, market_data = raw_market_data

        assert list(time_to_expiry.columns) == ["TimeToExpiry"]
        assert len(time_to_expiry) == len(market_data)

    def test_market_data_has_two_level_instrument_columns(self, raw_market_data):
        _, market_data = raw_market_data

        assert market_data.columns.nlevels == 2
        assert "Stock" in market_data.columns.get_level_values(0)

    def test_every_instrument_has_the_four_quote_fields(self, raw_market_data):
        _, market_data = raw_market_data

        for instrument in market_data.columns.get_level_values(0).unique():
            fields = set(market_data[instrument].columns)
            assert {"BidPrice", "BidVolume", "AskPrice", "AskVolume"} <= fields

    def test_quotes_are_not_crossed(self, raw_market_data):
        """Sanity check on the fixture itself: ask >= bid on every row."""
        _, market_data = raw_market_data

        for instrument in market_data.columns.get_level_values(0).unique():
            spread = market_data[instrument]["AskPrice"] - market_data[instrument]["BidPrice"]
            assert (spread >= 0).all(), f"{instrument} has crossed quotes"


class TestInstrumentDiscovery:
    def test_returns_options_excluding_the_underlying(self, option_names):
        assert option_names == ALL_OPTIONS
        assert "Stock" not in option_names


class TestTimeToExpiryIndex:
    def test_reindexes_market_data_by_time_to_expiry(self, raw_market_data):
        time_to_expiry, market_data = raw_market_data

        result = tdm.set_tte_to_market_data(market_data, time_to_expiry)

        assert result.index.name == "TTE"
        assert result.index[0] == pytest.approx(time_to_expiry["TimeToExpiry"].iloc[0])

    def test_time_to_expiry_decreases_monotonically(self, raw_market_data):
        time_to_expiry, market_data = raw_market_data

        result = tdm.set_tte_to_market_data(market_data, time_to_expiry)

        assert list(result.index) == sorted(result.index, reverse=True)


class TestTheoreticalValues:
    def test_produces_a_value_and_delta_for_every_option(self, enriched_market_data):
        for option in ALL_OPTIONS:
            fields = set(enriched_market_data[option].columns)
            assert {"Expected BidPrice", "Expected AskPrice"} <= fields
            assert {"Delta Long", "Delta Short"} <= fields

    def test_theoretical_bid_never_exceeds_theoretical_ask(self, enriched_market_data):
        for option in ALL_OPTIONS:
            block = enriched_market_data[option]
            assert (block["Expected AskPrice"] >= block["Expected BidPrice"]).all()

    def test_call_deltas_are_positive_and_put_deltas_negative(self, enriched_market_data):
        for option in ALL_OPTIONS:
            delta = enriched_market_data[option]["Delta Long"].dropna()
            if option.startswith("C"):
                assert (delta >= 0).all()
            else:
                assert (delta <= 0).all()


class TestArbitrageDetection:
    def test_sample_data_contains_no_arbitrage(self, enriched_market_data):
        """The bundled sample is self-consistent with the pricing model.

        This is a characterisation test, not an aspiration: it documents that
        the shipped demo data never triggers the strategy.
        """
        for option in ALL_OPTIONS:
            short_opps, long_opps = tdm.option_opportunities(option, enriched_market_data)
            assert len(short_opps) == 0
            assert len(long_opps) == 0

    def test_overpriced_option_produces_short_opportunities(self, mispriced_market_data_path):
        enriched = _enrich(mispriced_market_data_path)

        short_opps, _ = tdm.option_opportunities("C80", enriched)

        assert len(short_opps) > 0

    def test_detection_is_confined_to_the_mispriced_instrument(self, mispriced_market_data_path):
        enriched = _enrich(mispriced_market_data_path)

        for option in [o for o in ALL_OPTIONS if o != "C80"]:
            short_opps, long_opps = tdm.option_opportunities(option, enriched)
            assert len(short_opps) == 0
            assert len(long_opps) == 0

    def test_every_flagged_row_clears_the_threshold(self, mispriced_market_data_path):
        enriched = _enrich(mispriced_market_data_path)

        short_opps, _ = tdm.option_opportunities("C80", enriched)

        edge = short_opps["BidPrice"] - short_opps["Expected AskPrice"]
        assert (edge >= 0.10).all()


class TestPositionsAndOrders:
    def test_positions_cover_every_market_data_row(self, market_data_path):
        positions = _positions(market_data_path)
        _, market_data = tdm.read_data(market_data_path)

        assert len(positions) == len(market_data)

    def test_positions_include_a_stock_hedge_column(self, market_data_path):
        positions = _positions(market_data_path)

        assert ("Stock Position", "Stock") in positions.columns

    def test_flat_market_produces_no_trades(self, market_data_path):
        """No arbitrage in the sample means no positions and therefore no orders."""
        positions = _positions(market_data_path)
        orders, final_positions = tdm.create_orders(positions)

        assert (orders[ALL_OPTIONS] == 0).all().all()
        for option in ALL_OPTIONS:
            assert int(final_positions[option].iloc[0]) == 0

    def test_mispriced_market_produces_trades(self, mispriced_market_data_path):
        positions = _positions(mispriced_market_data_path)
        orders, _ = tdm.create_orders(positions)

        assert (orders["C80"] != 0).any(), "expected the strategy to trade the mispriced option"

    def test_orders_are_the_row_over_row_change_in_position(self, mispriced_market_data_path):
        positions = _positions(mispriced_market_data_path)
        orders, _ = tdm.create_orders(positions)

        held = positions["Call Position"]["C80"].reset_index(drop=True)
        traded = orders["C80"].reset_index(drop=True)

        assert traded.sum() == pytest.approx(held.iloc[-1] - held.iloc[0])

    def test_orders_drop_one_row_relative_to_positions(self, mispriced_market_data_path):
        """`create_orders` is `positions.diff()[1:]`, so the opening row is lost.

        Consequence: any position established at the very first timestamp is
        never emitted as an order. Harmless while the book starts flat, but it
        means sum(orders) reconstructs the position only up to that offset.
        """
        positions = _positions(mispriced_market_data_path)
        orders, _ = tdm.create_orders(positions)

        assert len(orders) == len(positions) - 1

    def test_final_positions_match_the_last_position_row(self, mispriced_market_data_path):
        positions = _positions(mispriced_market_data_path)
        _, final_positions = tdm.create_orders(positions)

        expected = positions["Call Position"]["C80"].iloc[-1]
        assert final_positions["C80"].iloc[0] == expected


# --- helpers -----------------------------------------------------------------


def _enrich(path):
    """Run a CSV through the full six-step Black-Scholes enrichment."""
    time_to_expiry, market_data = tdm.read_data(path)
    option_names = tdm.get_list_of_all_instruments(market_data)
    market_data = tdm.set_tte_to_market_data(market_data, time_to_expiry)
    option_values, option_deltas = tdm.create_df_to_store_options_values_delta(
        market_data, option_names
    )
    return tdm.add_blacksholes_data_to_market_data(
        market_data, option_names, option_values, option_deltas
    )


def _positions(path):
    time_to_expiry, market_data = tdm.read_data(path)
    option_names = tdm.get_list_of_all_instruments(market_data)
    timestamp = market_data.index
    enriched = _enrich(path)
    return tdm.create_positions(enriched, option_names, timestamp)


def test_pandas_version_is_modern():
    """Guard against silently sliding back to the pinned pandas 1.x."""
    assert int(pd.__version__.split(".")[0]) >= 2
