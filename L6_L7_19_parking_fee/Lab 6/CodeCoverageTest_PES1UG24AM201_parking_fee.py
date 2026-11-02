"""Lab 6 statement coverage tests. SRN: PES1UG24AM201.

Run this file explicitly with pytest: its handout-required name is not part
of pytest's default test_*.py discovery pattern. Keep parking_fee.py unchanged.
"""

import pytest

from parking_fee import find_slot, monthly_pass, parking_fee


# Preserve the starter cases, then exercise every executable statement.
def test_free_short_stay():
    assert parking_fee("car", 20, False, False) == 0


def test_any_floor():
    assert find_slot("car", 5, False) == "any floor"


def test_unknown_vehicle_is_rejected():
    with pytest.raises(ValueError, match="^unknown vehicle$"):
        parking_fee("bus", 60, False, False)


def test_negative_duration_is_rejected():
    with pytest.raises(ValueError, match="^invalid duration$"):
        parking_fee("bike", -1, False, False)


def test_started_hour_ev_discount_then_lost_ticket_penalty():
    # 61 minutes costs two car hours: 60 / 2 + 200 = 230.
    assert parking_fee("car", 61, True, True) == 230


@pytest.mark.parametrize(
    "vehicle,free_slots,is_disabled,expected",
    [
        pytest.param("car", 0, False, "full", id="no-slots"),
        pytest.param("car", 1, True, "ground floor", id="accessible-slot"),
        pytest.param("truck", 1, False, "basement", id="truck-slot"),
    ],
)
def test_other_slot_results(vehicle, free_slots, is_disabled, expected):
    assert find_slot(vehicle, free_slots, is_disabled) == expected


@pytest.mark.parametrize(
    "vehicle,expected",
    [pytest.param("bike", 400, id="resident-bike"),
     pytest.param("car", 1200, id="resident-car")],
)
def test_resident_monthly_pass(vehicle, expected):
    assert monthly_pass(vehicle, True) == expected


def test_unsupported_monthly_pass_is_rejected():
    with pytest.raises(ValueError, match="^no pass for this vehicle$"):
        monthly_pass("truck", False)
