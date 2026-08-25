import pytest

def calculate_proportionate_deduction(
    allowed_room_rent: float,
    actual_room_tariff: float,
    days: int,
    billed_associated_charges: float,
    fixed_implants: float,
    non_payables: float,
    copay_pct: float
):
    is_capped = actual_room_tariff > allowed_room_rent
    prop_ratio = min(1.0, allowed_room_rent / actual_room_tariff) if actual_room_tariff > 0 else 1.0
    
    billed_room = actual_room_tariff * days
    payable_room = min(actual_room_tariff, allowed_room_rent) * days
    patient_room_excess = billed_room - payable_room
    
    payable_associated = round(billed_associated_charges * prop_ratio, 2)
    prop_penalty = round(billed_associated_charges - payable_associated, 2)
    
    total_billed = billed_room + billed_associated_charges + fixed_implants + non_payables
    total_admissible = payable_room + payable_associated + fixed_implants
    
    copay_amount = round(total_admissible * (copay_pct / 100.0), 2)
    insurer_settlement = round(total_admissible - copay_amount, 2)
    patient_share = round(total_billed - insurer_settlement, 2)
    
    return {
        "is_capped": is_capped,
        "proportionate_ratio": prop_ratio,
        "proportionate_penalty": prop_penalty,
        "patient_room_excess": patient_room_excess,
        "total_admissible": total_admissible,
        "insurer_settlement": insurer_settlement,
        "patient_share": patient_share
    }

def test_room_within_limit_no_penalty():
    # Scenario: Policy allows ₹5,000/day. Patient takes Single Room at ₹4,800/day.
    res = calculate_proportionate_deduction(
        allowed_room_rent=5000.0,
        actual_room_tariff=4800.0,
        days=4,
        billed_associated_charges=46750.0,
        fixed_implants=34000.0,
        non_payables=8500.0,
        copay_pct=10.0
    )
    assert res["is_capped"] is False
    assert res["proportionate_ratio"] == 1.0
    assert res["proportionate_penalty"] == 0.0
    assert res["patient_room_excess"] == 0.0
    assert res["patient_share"] < 25000.0  # Only copay + non-payables

def test_room_exceeds_limit_triggers_penalty():
    # Scenario: Policy allows ₹5,000/day. Patient takes Deluxe at ₹9,000/day.
    res = calculate_proportionate_deduction(
        allowed_room_rent=5000.0,
        actual_room_tariff=9000.0,
        days=4,
        billed_associated_charges=46750.0,
        fixed_implants=34000.0,
        non_payables=8500.0,
        copay_pct=10.0
    )
    assert res["is_capped"] is True
    assert round(res["proportionate_ratio"], 3) == round(5000.0 / 9000.0, 3)
    assert res["proportionate_penalty"] > 20000.0
    assert res["patient_room_excess"] == 16000.0
    assert res["patient_share"] > 50000.0  # Massive jump due to penalty!
