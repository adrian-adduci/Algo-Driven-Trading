"""Tests that position accumulation is local to a call.

``create_positions`` tracked each instrument's running position in a
dynamically named module-level global (``positions_call_C60`` and friends,
created via ``globals()[...] = ...``).

Sequential calls happened to be safe because the counters are re-initialised
at the top of every call. The genuine consequences are narrower but real:
the module namespace accumulates arbitrary names, and two concurrent calls
share one set of counters and corrupt each other.
"""

import threading

import pytest
from test_options_pipeline import _enrich  # noqa: F401  (shared helper)

import _trade_data_management as tdm


def _positions(path):
    time_to_expiry, market_data = tdm.read_data(path)
    option_names = tdm.get_list_of_all_instruments(market_data)
    timestamp = market_data.index
    enriched = _enrich(path)
    return tdm.create_positions(enriched, option_names, timestamp)


class TestNoModuleNamespacePollution:
    def test_leaves_no_position_globals_behind(self, mispriced_market_data_path):
        for name in [n for n in vars(tdm) if n.startswith("positions_")]:
            delattr(tdm, name)

        _positions(mispriced_market_data_path)

        leaked = sorted(n for n in vars(tdm) if n.startswith("positions_"))
        assert leaked == [], f"module namespace polluted with {leaked}"


class TestConcurrentCallsAreIndependent:
    def test_threaded_calls_match_the_serial_result(self, mispriced_market_data_path):
        """Shared module-level counters make concurrent calls corrupt each other."""
        expected = _positions(mispriced_market_data_path)

        results = {}
        errors = {}

        def run(index):
            try:
                results[index] = _positions(mispriced_market_data_path)
            except Exception as exc:  # noqa: BLE001 - surfaced by the assert below
                errors[index] = exc

        threads = [threading.Thread(target=run, args=(i,)) for i in range(4)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        assert not errors, f"concurrent calls raised: {errors}"
        for index, frame in results.items():
            assert frame.equals(expected), (
                f"thread {index} produced different positions than a serial call"
            )


class TestRepeatedCallsAreDeterministic:
    def test_two_sequential_calls_agree(self, mispriced_market_data_path):
        first = _positions(mispriced_market_data_path)
        second = _positions(mispriced_market_data_path)

        assert first.equals(second)

    def test_differing_instrument_sets_do_not_interfere(self, mispriced_market_data_path):
        """A call restricted to some options must not be affected by an earlier
        call over all of them."""
        enriched = _enrich(mispriced_market_data_path)
        _, market_data = tdm.read_data(mispriced_market_data_path)
        timestamp = market_data.index
        every = tdm.get_list_of_all_instruments(market_data)
        # Keep one call and one put: create_positions unconditionally sums both
        # a 'Call Delta' and a 'Put Delta' block, so a calls-only or puts-only
        # universe raises KeyError. That is a separate defect from the shared
        # position counters under test here.
        subset = [next(o for o in every if o.startswith("C")),
                  next(o for o in every if o.startswith("P"))]

        alone = tdm.create_positions(enriched, subset, timestamp)
        tdm.create_positions(enriched, every, timestamp)
        after = tdm.create_positions(enriched, subset, timestamp)

        assert alone.equals(after)


@pytest.mark.parametrize("option", ["C60", "P70"])
def test_position_columns_are_cumulative(mispriced_market_data_path, option):
    """Guards the refactor: positions accumulate rather than reset per row."""
    positions = _positions(mispriced_market_data_path)
    kind = "Call Position" if option.startswith("C") else "Put Position"

    series = positions[kind][option]

    assert len(series) == len(positions)
    assert series.notna().all()
