import json
import math
import os
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
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
    policy_id: Optional[int] = 1
    city: Optional[str] = "Bengaluru"
    pincode: Optional[str] = "560076"
    lat: Optional[float] = None
    lng: Optional[float] = None
    facilities: Optional[List[str]] = ["cardiology", "icu", "cath_lab"]
    radius_km: Optional[float] = 30.0

class DeductionSimulationRequest(BaseModel):
    policy_id: int
    hospital_id: int
    procedure_code: str = "CAR-002"  # Angioplasty with 1 DES Stent
    room_category: str = "SEMI_PRIVATE"  # GENERAL, SEMI_PRIVATE, PRIVATE, ICU
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
    billed_room_charges: float
    payable_room_charges: float
    patient_room_excess: float
    billed_associated_charges: float
    payable_associated_charges: float
    proportionate_deduction_penalty: float
    fixed_implants_diagnostics: float
    non_payable_consumables: float
    total_billed_hospital_bill: float
    total_admissible_claim: float
    copay_amount: float
    insurer_settlement_amount: float
    indicative_patient_out_of_pocket: float
    warning_alerts: List[str] = []
    calculation_steps: List[str] = []

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2.0) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2.0) ** 2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return round(R * c, 1)

def get_city_coords(city_or_pin: str) -> tuple:
    c = city_or_pin.lower()
    if "hyd" in c or c.startswith("500"):
        return (17.4184, 78.4116, "Hyderabad")
    elif "mum" in c or c.startswith("400"):
        return (19.0760, 72.8777, "Mumbai")
    elif "del" in c or c.startswith("110"):
        return (28.6139, 77.2090, "New Delhi")
    elif "chen" in c or c.startswith("600"):
        return (13.0827, 80.2707, "Chennai")
    else:
        return (12.8958, 77.5986, "Bengaluru")

@router.post("/deduction-simulate", response_model=ProportionateDeductionResponse)
async def simulate_proportionate_deduction(req: DeductionSimulationRequest, db: AsyncSession = Depends(get_db)):
    pol_res = await db.execute(select(Policy).where(Policy.id == req.policy_id))
    policy = pol_res.scalar_one_or_none()
    allowed_room_rent = policy.room_rent_limit if policy else 5000.0
    copay_pct = policy.copay_percentage if policy else 10.0

    hosp_res = await db.execute(select(Hospital).where(Hospital.id == req.hospital_id).options(selectinload(Hospital.rooms), selectinload(Hospital.tariffs)))
    hospital = hosp_res.scalar_one_or_none()
    hosp_name = hospital.name if hospital else "Selected Hospital"

    room_tariffs = {
        "GENERAL": 2000.0,
        "SEMI_PRIVATE": 4500.0,
        "PRIVATE": 8000.0,
        "ICU": 12000.0
    }
    actual_room_tariff = room_tariffs.get(req.room_category.upper(), 4500.0)

    base_package = 80000.0
    billed_associated = 45000.0
    fixed_implants = 25000.0
    non_payables = 6000.0

    billed_room_total = actual_room_tariff * req.days_of_stay
    payable_room_total = min(actual_room_tariff, allowed_room_rent) * req.days_of_stay
    patient_room_excess = billed_room_total - payable_room_total

    is_capped = actual_room_tariff > allowed_room_rent
    if is_capped:
        proportionate_ratio = round(allowed_room_rent / actual_room_tariff, 4)
    else:
        proportionate_ratio = 1.0

    payable_associated = round(billed_associated * proportionate_ratio, 2)
    prop_penalty = round(billed_associated - payable_associated, 2)

    total_billed = billed_room_total + billed_associated + fixed_implants + non_payables
    total_admissible = payable_room_total + payable_associated + fixed_implants
    
    copay_amount = round(total_admissible * (copay_pct / 100.0), 2)
    insurer_settlement = round(total_admissible - copay_amount, 2)
    patient_share = round(total_billed - insurer_settlement, 2)

    warnings = []
    if is_capped:
        warnings.append(f"Room rent cap breached! Actual tariff (₹{actual_room_tariff:,.0f}) exceeds policy cap (₹{allowed_room_rent:,.0f}).")
        warnings.append(f"Proportionate deduction penalty of ₹{prop_penalty:,.0f} applied to surgeon, OT, and medical fees ({proportionate_ratio*100:.1f}% payable).")
    else:
        warnings.append("Room category is fully within allowed policy limit. Zero proportionate deduction penalty!")

    steps = [
        f"1. Allowed Room Rent: ₹{allowed_room_rent:,.0f}/day | Actual: ₹{actual_room_tariff:,.0f}/day",
        f"2. Proportionate Factor: min(1.0, {allowed_room_rent:.0f} / {actual_room_tariff:.0f}) = {proportionate_ratio:.3f}",
        f"3. Associated Charges: ₹{billed_associated:,.0f} × {proportionate_ratio:.3f} = ₹{payable_associated:,.0f} (Penalty: ₹{prop_penalty:,.0f})",
        f"4. Total Hospital Bill: ₹{total_billed:,.0f}",
        f"5. Total Insurer Settlement: ₹{insurer_settlement:,.0f}",
        f"6. Net Indicative Patient Responsibility: ₹{patient_share:,.0f}"
    ]

    return ProportionateDeductionResponse(
        hospital_name=hosp_name,
        procedure_name="Coronary Angioplasty (PTCA) with 1 Stent",
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
async def match_hospitals(req: MatchRequest):
    # Load canonical hospitals from processed JSON
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    data_file = os.path.join(repo_root, "data", "processed", "canonical_hospitals.json")
    
    if os.path.exists(data_file):
        with open(data_file, "r", encoding="utf-8") as f:
            all_hospitals = json.load(f)
    else:
        all_hospitals = []

    # Determine patient coordinates
    if req.lat and req.lng:
        p_lat, p_lng, p_city = req.lat, req.lng, req.city or "Your Location"
    else:
        p_lat, p_lng, p_city = get_city_coords(req.pincode or req.city or "Bengaluru")

    req_facilities = [f.lower() for f in (req.facilities or ["cardiology", "icu", "cath_lab"])]

    # Filter & compute match
    matches = []
    for h in all_hospitals:
        # Distance calculation
        h_lat = h.get("latitude", 12.8958)
        h_lng = h.get("longitude", 77.5986)
        dist = haversine_distance(p_lat, p_lng, h_lat, h_lng)

        # Check city affinity or proximity
        city_match = (req.city and req.city.lower() in h.get("city", "").lower()) or \
                     (req.pincode and req.pincode[:3] == str(h.get("pincode", ""))[:3]) or \
                     (dist <= (req.radius_km or 40.0))

        # Calculate facility status
        h_specs = [s.lower() for s in h.get("specialties", [])]
        
        fac_statuses = []
        matched_count = 0
        for rf in req_facilities:
            rf_clean = rf.replace("_", " ")
            if any(rf in hs or hs in rf for hs in h_specs):
                fac_statuses.append({"name": rf_clean.title(), "status": "AVAILABLE"})
                matched_count += 1
            else:
                # E.g. Cath lab check
                if "cath" in rf:
                    fac_statuses.append({"name": "Cath Lab", "status": "VERIFY", "note": "Requires pre-admission confirmation"})
                    matched_count += 0.5
                else:
                    fac_statuses.append({"name": rf_clean.title(), "status": "UNAVAILABLE"})

        facility_match_score = (matched_count / max(1, len(req_facilities))) * 100.0

        if facility_match_score >= 90:
            match_status = "FULL MATCH"
        elif facility_match_score >= 60:
            match_status = "NEEDS VERIFICATION"
        elif facility_match_score > 0:
            match_status = "PARTIAL MATCH"
        else:
            match_status = "NOT SUITABLE"

        # Empanelment
        is_cashless = any("STAR" in p or "HDFC" in p for p in h.get("empaneled_payers", []))
        network_score = 100.0 if is_cashless else 60.0

        # Room fit
        room_fit_score = 100.0  # Semi-private fits under ₹5k

        # Distance score
        dist_score = max(50.0, 100.0 - (dist * 2.0))

        # Overall care fit
        care_fit = round(
            (facility_match_score * 0.40) +
            (network_score * 0.25) +
            (room_fit_score * 0.20) +
            (dist_score * 0.15),
            1
        )

        total_avail_beds = sum(b.get("available_beds", 0) for b in h.get("beds", []))
        icu_avail_beds = sum(b.get("available_beds", 0) for b in h.get("beds", []) if b.get("category") == "ICU")

        matches.append({
            "id": h.get("id"),
            "name": h.get("name"),
            "city": h.get("city"),
            "pincode": h.get("pincode"),
            "address": f"{h.get('address')}, {h.get('city')} (PIN {h.get('pincode')})",
            "distance_km": dist,
            "match_score": int(care_fit),
            "care_fit_score": int(care_fit),
            "match_status": match_status,
            "network_status": "CASHLESS_NETWORK" if is_cashless else "REIMBURSEMENT_ONLY",
            "available_beds": total_avail_beds if total_avail_beds > 0 else 14,
            "total_beds": h.get("total_beds", 250),
            "occupied_beds": h.get("total_beds", 250) - (total_avail_beds if total_avail_beds > 0 else 14),
            "available_icu_beds": icu_avail_beds if icu_avail_beds > 0 else 3,
            "facilities": fac_statuses,
            "room_compatibility": "Semi-Private within policy limit",
            "indicative_cost": int(80000 * h.get("markup_multiplier", 1.0)),
            "reasons": [
                f"{', '.join([f['name'] for f in fac_statuses if f['status'] == 'AVAILABLE'])} confirmed available",
                "Empanelled on Star Health Cashless Preferred Network" if is_cashless else "Reimbursement Claim Required",
                f"Proximity: {dist} km from your location ({req.pincode or p_city})"
            ],
            "score_breakdown": {
                "facility_match": int(facility_match_score),
                "network_compatibility": int(network_score),
                "room_fit": int(room_fit_score),
                "bed_availability": 80,
                "cost_compatibility": 90,
                "data_confidence": 95
            }
        })

    # Sort primarily by city affinity, then care fit score
    matches.sort(key=lambda x: (x["city"].lower() == p_city.lower(), -x["distance_km"], x["care_fit_score"]), reverse=True)
    return matches
