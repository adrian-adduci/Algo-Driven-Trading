"""Tests for the Black-Scholes pricing functions.

These assert against closed-form identities (put-call parity, delta bounds,
vega symmetry) rather than against hardcoded expected numbers, so they stay
meaningful if the implementation is refactored.
"""

import math

import pytest

from _trade_data_management import (
    call_delta,
    call_value,
    call_vega,
    put_delta,
    put_value,
    put_vega,
)

# S, K, T, r, sigma
BASE = (70.0, 70.0, 0.5, 0.0, 0.20)


class TestPutCallParity:
    def test_parity_holds_at_the_money(self):
        S, K, T, r, sigma = BASE
        call = call_value(S, K, T, r, sigma)
        put = put_value(S, K, T, r, sigma)

        assert call - put == pytest.approx(S - K * math.exp(-r * T), abs=1e-9)

    @pytest.mark.parametrize("K", [60.0, 65.0, 70.0, 75.0, 80.0])
    def test_parity_holds_across_strikes(self, K):
        S, _, T, r, sigma = BASE
        call = call_value(S, K, T, r, sigma)
        put = put_value(S, K, T, r, sigma)

        assert call - put == pytest.approx(S - K * math.exp(-r * T), abs=1e-9)


class TestValueBounds:
    def test_deep_in_the_money_call_approaches_intrinsic_value(self):
        _, _, T, r, sigma = BASE
        value = call_value(200.0, 70.0, T, r, sigma)

        assert value == pytest.approx(200.0 - 70.0, abs=1e-6)

    def test_deep_out_of_the_money_call_approaches_zero(self):
        _, _, T, r, sigma = BASE
        assert call_value(10.0, 70.0, T, r, sigma) == pytest.approx(0.0, abs=1e-6)

    def test_call_value_increases_with_spot(self):
        _, K, T, r, sigma = BASE
        values = [call_value(S, K, T, r, sigma) for S in (60.0, 65.0, 70.0, 75.0, 80.0)]

        assert values == sorted(values)
        assert len(set(values)) == len(values)

    def test_call_value_never_below_intrinsic(self):
        _, K, T, r, sigma = BASE
        for S in (60.0, 70.0, 80.0):
            assert call_value(S, K, T, r, sigma) >= max(S - K, 0.0) - 1e-9


class TestDeltas:
    def test_call_delta_is_bounded_between_zero_and_one(self):
        _, K, T, r, sigma = BASE
        for S in (40.0, 70.0, 120.0):
            assert 0.0 <= call_delta(S, K, T, r, sigma) <= 1.0

    def test_put_delta_is_bounded_between_minus_one_and_zero(self):
        _, K, T, r, sigma = BASE
        for S in (40.0, 70.0, 120.0):
            assert -1.0 <= put_delta(S, K, T, r, sigma) <= 0.0

    def test_call_and_put_delta_differ_by_one(self):
        """With r = 0 and no dividends, N(d1) - (N(d1) - 1) == 1."""
        S, K, T, r, sigma = BASE
        assert call_delta(S, K, T, r, sigma) - put_delta(S, K, T, r, sigma) == pytest.approx(1.0)

    def test_at_the_money_call_delta_is_near_one_half(self):
        S, K, T, r, sigma = BASE
        assert call_delta(S, K, T, r, sigma) == pytest.approx(0.5, abs=0.05)


class TestVega:
    def test_vega_is_positive(self):
        S, K, T, r, sigma = BASE
        assert call_vega(S, K, T, r, sigma) > 0

    def test_call_and_put_vega_are_equal(self):
        S, K, T, r, sigma = BASE
        assert call_vega(S, K, T, r, sigma) == pytest.approx(put_vega(S, K, T, r, sigma))
