"""Lab 6 branch coverage tests. SRN: PES1UG24AM201.

This independent suite retains the starter scenarios and adds boundaries,
decision outcomes, and priority/discount interactions. Run explicitly with
pytest because the handout-required filename is not a test_*.py filename.
"""

import pytest

from parking_fee import find_slot, monthly_pass, parking_fee


@pytest.mark.parametrize(
    "vehicle,minutes,is_ev,lost_ticket,expected",
    [
        pytest.param("car", 20, False, False, 0, id="starter-free-short-stay"),
        pytest.param("bike", 0, False, False, 0, id="zero-minutes"),
        pytest.param("car", 30, False, False, 0, id="free-limit-30"),
        pytest.param("car", 31, False, False, 30, id="first-paid-minute"),
        pytest.param("car", 59, False, False, 30, id="before-one-hour"),
        pytest.param("car", 60, False, False, 30, id="exactly-one-hour"),
        pytest.param("car", 61, False, False, 60, id="second-hour-started"),
        pytest.param("car", 120, False, False, 60, id="two-whole-hours"),
        pytest.param("car", 121, False, False, 90, id="third-hour-started"),
        pytest.param("bike", 31, False, False, 10, id="bike-hourly-rate"),
        pytest.param("truck", 31, False, False, 60, id="truck-hourly-rate"),
        pytest.param("bike", 61, False, False, 20, id="bike-round-up"),
        pytest.param("truck", 61, False, False, 120, id="truck-round-up"),
        pytest.param("car", 60, True, False, 15, id="car-ev-half-price"),
        pytest.param("bike", 60, True, False, 5, id="bike-ev-half-price"),
        pytest.param("truck", 60, True, False, 60, id="ev-truck-no-discount"),
        pytest.param("car", 30, True, False, 0, id="free-ev-stay"),
        pytest.param("car", 30, False, True, 200, id="lost-ticket-free-stay"),
        pytest.param("car", 60, False, True, 230, id="lost-ticket-paid-stay"),
        pytest.param("car", 61, True, True, 230, id="ev-before-penalty"),
        pytest.param("bike", 60, True, True, 205, id="bike-ev-with-penalty"),
        pytest.param("truck", 60, True, True, 260, id="ev-truck-with-penalty"),
    ],
)
def test_parking_fee_results(vehicle, minutes, is_ev, lost_ticket, expected):
    assert parking_fee(vehicle, minutes, is_ev, lost_ticket) == expected


@pytest.mark.parametrize("vehicle", ["bus", "CAR", ""])
def test_unknown_vehicle_is_rejected(vehicle):
    with pytest.raises(ValueError, match="^unknown vehicle$"):
        parking_fee(vehicle, 60, False, False)


@pytest.mark.parametrize("vehicle", ["bike", "car", "truck"])
def test_negative_duration_is_rejected(vehicle):
    with pytest.raises(ValueError, match="^invalid duration$"):
        parking_fee(vehicle, -1, False, False)


def test_unknown_vehicle_validation_precedes_duration_validation():
    with pytest.raises(ValueError, match="^unknown vehicle$"):
        parking_fee("bus", -1, True, True)


@pytest.mark.parametrize(
    "vehicle,free_slots,is_disabled,expected",
    [
        pytest.param("car", 5, False, "any floor", id="starter-any-floor"),
        pytest.param("car", 0, False, "full", id="zero-slots"),
        pytest.param("bike", -1, False, "full", id="negative-slots"),
        pytest.param("truck", 0, True, "full", id="full-before-disability"),
        pytest.param("car", 1, True, "ground floor", id="disabled-car"),
        pytest.param("truck", 1, True, "ground floor", id="disability-before-truck"),
        pytest.param("truck", 1, False, "basement", id="non-disabled-truck"),
        pytest.param("bike", 1, False, "any floor", id="last-slot-bike"),
        pytest.param("car", 1, False, "any floor", id="last-slot-car"),
    ],
)
def test_slot_selection(vehicle, free_slots, is_disabled, expected):
    assert find_slot(vehicle, free_slots, is_disabled) == expected


@pytest.mark.parametrize(
    "vehicle,is_resident,expected",
    [
        pytest.param("bike", False, 500, id="bike-regular"),
        pytest.param("bike", True, 400, id="bike-resident"),
        pytest.param("car", False, 1500, id="car-regular"),
        pytest.param("car", True, 1200, id="car-resident"),
    ],
)
def test_monthly_pass_price(vehicle, is_resident, expected):
    assert monthly_pass(vehicle, is_resident) == expected


@pytest.mark.parametrize("vehicle", ["truck", "bus", "CAR", ""])
@pytest.mark.parametrize("is_resident", [False, True])
def test_unsupported_monthly_pass_is_rejected(vehicle, is_resident):
    with pytest.raises(ValueError, match="^no pass for this vehicle$"):
        monthly_pass(vehicle, is_resident)
