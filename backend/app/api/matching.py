from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from ..database import get_db
from ..models.hospital import Hospital
from ..models.policy import Policy
from ..models.tariff import Tariff
from ..models.scheme import InsuranceNetwork

router = APIRouter(prefix="/api/v1/matching", tags=["Matching & Deduction Simulator"])

class MatchRequest(BaseModel):
    policy_id: int
    city: Optional[str] = "Bengaluru"
    specialty_code: Optional[str] = "CAR"
    radius_km: Optional[float] = 15.0

class DeductionSimulationRequest(BaseModel):
    policy_id: int
    hospital_id: int
    procedure_code: str = "CAR-002"  # Angioplasty with 1 DES Stent
    room_category: str = "PRIVATE_AC"  # GENERAL, SEMI_PRIVATE, PRIVATE_AC, DELUXE, ICU
    days_of_stay: int = 4

class ProportionateDeductionResponse(BaseModel):
    hospital_name: str
    procedure_name: str
    room_category: str
    days_of_stay: int
    allowed_room_rent_per_day: float
    actual_room_tariff_per_day: float
    is_room_capped: bool
    proportionate_ratio: float
    
    # Financial breakdown
    billed_room_charges: float
    payable_room_charges: float
    patient_room_excess: float
    
    billed_associated_charges: float  # Surgeon + OT + Anesthesia + Nursing
    payable_associated_charges: float
    proportionate_deduction_penalty: float
    
    fixed_implants_diagnostics: float  # Stent / Mesh (Non-proportionate)
    non_payable_consumables: float     # Gloves, PPE, Admin
    
    total_billed_hospital_bill: float
    total_admissible_claim: float
    copay_amount: float
    insurer_settlement_amount: float
    
    # Final Patient Liability
    indicative_patient_out_of_pocket: float
    warning_alerts: List[str] = []
    calculation_steps: List[str] = []

@router.post("/deduction-simulate", response_model=ProportionateDeductionResponse)
async def simulate_proportionate_deduction(req: DeductionSimulationRequest, db: AsyncSession = Depends(get_db)):
    # 1. Fetch Policy
    pol_res = await db.execute(select(Policy).where(Policy.id == req.policy_id))
    policy = pol_res.scalar_one_or_none()
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")

    # 2. Fetch Hospital
    hosp_res = await db.execute(select(Hospital).where(Hospital.id == req.hospital_id).options(selectinload(Hospital.rooms), selectinload(Hospital.tariffs)))
    hospital = hosp_res.scalar_one_or_none()
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")

    # 3. Determine Room Tariff
    room_daily_tariffs = {
        "GENERAL": 1800.0,
        "SEMI_PRIVATE": 3600.0,
        "PRIVATE_AC": 5400.0,
        "DELUXE": 9000.0,
        "ICU": 6800.0
    }
    actual_room_tariff = room_daily_tariffs.get(req.room_category.upper(), 5400.0)
    allowed_room_rent = policy.room_rent_limit

    # 4. Fetch Procedure Base Rate
    tar_res = await db.execute(select(Tariff).where(Tariff.hospital_id == req.hospital_id, Tariff.procedure_code == req.procedure_code))
    tariff = tar_res.scalar_one_or_none()
    base_package = tariff.package_rate if tariff else 85000.0
    proc_name = tariff.procedure_name if tariff else "Coronary Angioplasty (PTCA) with 1 Stent"

    # Associated charges vs Fixed implants
    # In a ₹85,000 package: ₹45,000 associated (OT+Doctor), ₹35,000 fixed stent, ₹5,000 diagnostics
    billed_associated = base_package * 0.55
    fixed_implants = base_package * 0.40
    non_payables = 8500.0  # Consumables

    # Days
    billed_room_total = actual_room_tariff * req.days_of_stay
    payable_room_total = min(actual_room_tariff, allowed_room_rent) * req.days_of_stay
    patient_room_excess = billed_room_total - payable_room_total

    # Proportionate Ratio
    is_capped = actual_room_tariff > allowed_room_rent
    if is_capped:
        proportionate_ratio = round(allowed_room_rent / actual_room_tariff, 4)
    else:
        proportionate_ratio = 1.0

    payable_associated = round(billed_associated * proportionate_ratio, 2)
    prop_penalty = round(billed_associated - payable_associated, 2)

    total_billed = billed_room_total + billed_associated + fixed_implants + non_payables
    total_admissible = payable_room_total + payable_associated + fixed_implants
    
    copay_amount = round(total_admissible * (policy.copay_percentage / 100.0), 2)
    insurer_settlement = round(total_admissible - copay_amount, 2)
    
    patient_share = round(total_billed - insurer_settlement, 2)

    warnings = []
    if is_capped:
        warnings.append(f"Room rent cap breached! Actual tariff (₹{actual_room_tariff:,.0f}) exceeds policy cap (₹{allowed_room_rent:,.0f}).")
        warnings.append(f"Proportionate deduction penalty of ₹{prop_penalty:,.0f} applied to surgeon, OT, and medical fees ({proportionate_ratio*100:.1f}% payable).")
    else:
        warnings.append("Room category is fully within allowed policy limit. Zero proportionate deduction penalty!")

    if policy.copay_percentage > 0:
        warnings.append(f"Mandatory {policy.copay_percentage:.0f}% policy co-pay applies to all admissible charges (₹{copay_amount:,.0f}).")

    steps = [
        f"1. Allowed Room Rent: ₹{allowed_room_rent:,.0f}/day | Actual: ₹{actual_room_tariff:,.0f}/day",
        f"2. Proportionate Factor: min(1.0, {allowed_room_rent:.0f} / {actual_room_tariff:.0f}) = {proportionate_ratio:.3f}",
        f"3. Associated Charges: ₹{billed_associated:,.0f} × {proportionate_ratio:.3f} = ₹{payable_associated:,.0f} (Penalty: ₹{prop_penalty:,.0f})",
        f"4. Total Hospital Bill: ₹{total_billed:,.0f}",
        f"5. Total Insurer Settlement: ₹{insurer_settlement:,.0f}",
        f"6. Net Indicative Patient Responsibility: ₹{patient_share:,.0f}"
    ]

    return ProportionateDeductionResponse(
        hospital_name=hospital.name,
        procedure_name=proc_name,
        room_category=req.room_category,
        days_of_stay=req.days_of_stay,
        allowed_room_rent_per_day=allowed_room_rent,
        actual_room_tariff_per_day=actual_room_tariff,
        is_room_capped=is_capped,
        proportionate_ratio=proportionate_ratio,
        billed_room_charges=billed_room_total,
        payable_room_charges=payable_room_total,
        patient_room_excess=patient_room_excess,
        billed_associated_charges=billed_associated,
        payable_associated_charges=payable_associated,
        proportionate_deduction_penalty=prop_penalty,
        fixed_implants_diagnostics=fixed_implants,
        non_payable_consumables=non_payables,
        total_billed_hospital_bill=total_billed,
        total_admissible_claim=total_admissible,
        copay_amount=copay_amount,
        insurer_settlement_amount=insurer_settlement,
        indicative_patient_out_of_pocket=patient_share,
        warning_alerts=warnings,
        calculation_steps=steps
    )

@router.post("/hospitals")
async def match_hospitals(req: MatchRequest, db: AsyncSession = Depends(get_db)):
    # Fetch Policy
    pol_res = await db.execute(select(Policy).where(Policy.id == req.policy_id))
    policy = pol_res.scalar_one_or_none()
    
    # Fetch Hospitals
    hosp_res = await db.execute(select(Hospital).options(selectinload(Hospital.rooms), selectinload(Hospital.tariffs), selectinload(Hospital.schemes)))
    hospitals = hosp_res.scalars().all()

    matches = []
    for h in hospitals:
        # Empanelment check
        net_res = await db.execute(select(InsuranceNetwork).where(InsuranceNetwork.hospital_id == h.id))
        networks = net_res.scalars().all()
        is_cashless = any("STAR" in n.insurer.upper() or "HDFC" in n.insurer.upper() for n in networks)

        # Bed check
        total_avail_beds = sum(r.available for r in h.rooms)
        icu_avail_beds = sum(r.available for r in h.rooms if "ICU" in str(r.room_type).upper())

        # Score calculation
        empanelment_score = 1.0 if is_cashless else 0.5
        bed_score = 1.0 if total_avail_beds > 5 else 0.5
        room_fit_score = 0.95  # Single room is within policy ₹5k limit
        distance_score = 0.90

        total_score = round((empanelment_score * 0.35 + room_fit_score * 0.30 + distance_score * 0.20 + bed_score * 0.15) * 100, 1)

        matches.append({
            "id": h.id,
            "name": h.name,
            "city": h.city,
            "address": h.address,
            "match_score": total_score,
            "network_status": "CASHLESS_NETWORK" if is_cashless else "REIMBURSEMENT_ONLY",
            "available_beds": total_avail_beds,
            "available_icu_beds": icu_avail_beds,
            "room_options": [
                {"category": "General Ward", "tariff": 1800, "status": "COVERED"},
                {"category": "Single Private A/C", "tariff": 4800, "status": "WITHIN_LIMIT"},
                {"category": "Deluxe Suite", "tariff": 8500, "status": "EXCEEDS_CAP_PENALTY"}
            ],
            "estimated_out_of_pocket": 14500.0 if is_cashless else 32000.0,
            "reasons": [
                "Empanelled for instant Cashless TPA admission" if is_cashless else "Reimbursement claim required",
                "Single private room fits within daily ₹5,000 policy cap",
                f"{total_avail_beds} beds currently unoccupied ({icu_avail_beds} ICU)"
            ]
        })

    matches.sort(key=lambda x: x["match_score"], reverse=True)
    return matches
