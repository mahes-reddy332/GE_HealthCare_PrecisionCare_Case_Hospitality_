import asyncio
import json
import os
import sys
from datetime import datetime

# Ensure backend root is on sys.path
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, backend_dir)

from app.database import init_db, AsyncSessionLocal
from app.models.hospital import Hospital, FacilityIdentifier, FacilitySpecialty, OperationalStatus
from app.models.room import BedInventory, RoomType
from app.models.tariff import Tariff
from app.models.scheme import Scheme, HospitalScheme, InsuranceNetwork
from app.models.policy import Policy, PolicyExtractionClause
from app.models.provenance import DataSource, DataStatus
from app.models.patient import Patient, PatientJourney, JourneyEventLog, JourneyEvent

async def seed_all():
    print("[*] Initializing database schema...")
    await init_db()
    
    repo_root = os.path.abspath(os.path.join(backend_dir, ".."))
    data_dir = os.path.join(repo_root, "data", "processed")
    
    hospitals_file = os.path.join(data_dir, "canonical_hospitals.json")
    tariffs_file = os.path.join(data_dir, "pmjay_procedure_tariffs.json")
    schemes_file = os.path.join(data_dir, "payers_schemes.json")
    
    if not os.path.exists(hospitals_file):
        print(f"[!] Data file missing at {hospitals_file}.")
        return

    with open(hospitals_file, "r", encoding="utf-8") as f:
        hospitals_data = json.load(f)
        
    with open(tariffs_file, "r", encoding="utf-8") as f:
        tariffs_data = json.load(f)
        
    with open(schemes_file, "r", encoding="utf-8") as f:
        schemes_data = json.load(f)

    async with AsyncSessionLocal() as session:
        print("[*] Seeding Data Sources...")
        sources = [
            DataSource(id=1, name="data.gov.in Hospital Directory", description="MoHFW National Health Directory", status=DataStatus.AUTHORITATIVE, url="https://data.gov.in"),
            DataSource(id=2, name="PM-JAY Health Benefit Packages 2022", description="NHA Master Package Rates", status=DataStatus.AUTHORITATIVE, url="https://pmjay.gov.in"),
            DataSource(id=3, name="CGHS Standard Rate Cards", description="Central Govt Health Scheme Rate List", status=DataStatus.AUTHORITATIVE, url="https://cghs.nic.in"),
            DataSource(id=4, name="HOSPITALITY Synthetic Bed Availability Feed", description="Real-time simulated bed telemetry", status=DataStatus.SIMULATED, url="http://localhost:8000")
        ]
        session.add_all(sources)
        await session.flush()

        print("[*] Seeding Schemes & Payers...")
        scheme_map = {}
        for s in schemes_data:
            sch = Scheme(
                name=s["name"],
                type="GOVERNMENT" if "GOVERNMENT" in s["type"] else "PRIVATE"
            )
            session.add(sch)
            await session.flush()
            scheme_map[s["id"]] = sch.id

        print("[*] Seeding Hospitals, Specialties, Rooms, Beds, and Tariffs...")
        for h in hospitals_data:
            hosp = Hospital(
                name=h["name"],
                address=h.get("address", ""),
                city=h.get("city", ""),
                state=h.get("state", ""),
                pincode=h.get("pincode", ""),
                latitude=h.get("latitude"),
                longitude=h.get("longitude"),
                operational_status=OperationalStatus.ACTIVE
            )
            session.add(hosp)
            await session.flush()

            # Identifier
            if h.get("hfr_id"):
                ident = FacilityIdentifier(
                    hospital_id=hosp.id,
                    system="HFR",
                    value=h["hfr_id"]
                )
                session.add(ident)

            # Specialties
            for sp in h.get("specialties", []):
                spec = FacilitySpecialty(
                    hospital_id=hosp.id,
                    name=sp
                )
                session.add(spec)

            # Schemes & Network mappings
            for payer_code in h.get("empaneled_payers", []):
                if payer_code in scheme_map:
                    hs = HospitalScheme(
                        hospital_id=hosp.id,
                        scheme_id=scheme_map[payer_code],
                        cashless_available=True
                    )
                    session.add(hs)
                    
                    net = InsuranceNetwork(
                        hospital_id=hosp.id,
                        insurer=payer_code.replace("_", " ").title(),
                        product="Comprehensive Healthcare Plan",
                        cashless_status=True,
                        tpa="Medi Assist / Vidal Health TPA"
                    )
                    session.add(net)

            # Bed inventories
            for b in h.get("beds", []):
                # map category to enum
                cat = b["category"]
                rtype = RoomType.GENERAL
                if cat == "SEMI_PRIVATE":
                    rtype = RoomType.SEMI_PRIVATE
                elif cat == "PRIVATE_AC":
                    rtype = RoomType.PRIVATE_AC
                elif cat == "DELUXE":
                    rtype = RoomType.DELUXE
                elif cat == "ICU":
                    rtype = RoomType.ICU

                bed = BedInventory(
                    hospital_id=hosp.id,
                    room_type=rtype,
                    total=b["total_beds"],
                    occupied=b["occupied_beds"],
                    available=b["available_beds"],
                    data_status="SIMULATED"
                )
                session.add(bed)

            # Tariffs for procedures
            markup = h.get("markup_multiplier", 1.0)
            for proc in tariffs_data:
                tar = Tariff(
                    hospital_id=hosp.id,
                    specialty_code=proc["specialty_code"],
                    procedure_code=proc["procedure_code"],
                    procedure_name=proc["procedure_name"],
                    package_rate=round(proc["package_rate"] * markup, 0),
                    nabh_rate=round(proc["nabh_rate"] * markup, 0),
                    preauth_required=proc.get("preauth_required", True),
                    source=proc.get("source", "PMJAY_HBP_2022")
                )
                session.add(tar)

        print("[*] Seeding Demo Patient & Policy for Ramesh Kumar...")
        patient = Patient(
            id=1,
            name="Suresh Kumar (Father)",
            abha_id="91-8273-1928-1144",
            phone="+91-98450-12345"
        )
        session.add(patient)
        await session.flush()

        policy = Policy(
            id=1,
            patient_id=patient.id,
            policy_number="STAR-FHO-2026-88192",
            insurer="Star Health and Allied Insurance",
            sum_insured=500000.0,
            room_rent_cap_type="PERCENTAGE_OF_SI",
            room_rent_limit=5000.0,
            icu_limit=10000.0,
            copay_percentage=10.0,
            deductible=0.0
        )
        session.add(policy)
        await session.flush()

        clauses = [
            PolicyExtractionClause(policy_id=policy.id, clause_type="ROOM_RENT", page_number=2, source_text="Section 3.1: Room rent limit is 1% of Sum Insured per day (Max Rs. 5,000/-)", confidence="HIGH"),
            PolicyExtractionClause(policy_id=policy.id, clause_type="COPAY", page_number=4, source_text="Section 5.2: Co-payment of 10% shall apply to all claims for insured persons aged above 60 years", confidence="HIGH"),
            PolicyExtractionClause(policy_id=policy.id, clause_type="PROPORTIONATE_DEDUCTION", page_number=3, source_text="Section 3.2: If insured occupies a room higher than eligible category, associated medical charges shall be paid in proportionate ratio", confidence="HIGH")
        ]
        session.add_all(clauses)

        journey = PatientJourney(
            id=1,
            patient_id=patient.id,
            current_stage=JourneyEvent.PRE_ADMISSION
        )
        session.add(journey)
        await session.flush()

        event = JourneyEventLog(
            journey_id=journey.id,
            event_type=JourneyEvent.PRE_ADMISSION,
            description="Policy uploaded. Comparing cardiology procedure options at Apollo Hospitals Bannerghatta Road."
        )
        session.add(event)

        await session.commit()
        print("[+] SUCCESS: Database successfully seeded with rich Indian health datasets, networks, tariffs, and demo scenario!")

if __name__ == "__main__":
    asyncio.run(seed_all())
