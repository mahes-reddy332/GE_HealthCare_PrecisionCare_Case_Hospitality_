"""
HOSPITALITY Data Engine & Ingestion Script
Generates canonical baseline datasets from authoritative Indian health benchmarks
and realistic synthetic simulation layers with provenance tagging.
"""

import json
import os
import random
from datetime import datetime, timezone

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
SYNTHETIC_DIR = os.path.join(DATA_DIR, "synthetic")

for d in [RAW_DIR, PROCESSED_DIR, SYNTHETIC_DIR]:
    os.makedirs(d, exist_ok=True)

# 1. CGHS Standard Room Tariffs (Authoritative Reference)
CGHS_ROOM_TARIFFS = [
    {
        "category": "GENERAL_WARD",
        "name": "General Ward Bed",
        "daily_tariff": 1500.0,
        "description": "Multi-occupancy ward bed including nursing care and basic monitoring",
        "data_status": "AUTHORITATIVE",
        "source": "CGHS_RATE_CARDS"
    },
    {
        "category": "SEMI_PRIVATE",
        "name": "Semi-Private Room (Twin Sharing)",
        "daily_tariff": 3000.0,
        "description": "Two-bed shared room with partition, shared attached bathroom",
        "data_status": "AUTHORITATIVE",
        "source": "CGHS_RATE_CARDS"
    },
    {
        "category": "PRIVATE_AC",
        "name": "Single Private A/C Room",
        "daily_tariff": 4500.0,
        "description": "Individual private air-conditioned room with attendant couch and private bathroom",
        "data_status": "AUTHORITATIVE",
        "source": "CGHS_RATE_CARDS"
    },
    {
        "category": "DELUXE",
        "name": "Deluxe Suite",
        "daily_tariff": 7500.0,
        "description": "Executive suite with patient lounge, premium amenities, refrigerator",
        "data_status": "SIMULATED",
        "source": "HOSPITAL_MARKUP"
    },
    {
        "category": "ICU",
        "name": "Intensive Care Unit (ICU)",
        "daily_tariff": 5400.0,
        "description": "Critical care bed with continuous hemodynamics, RMO, ventilator support",
        "data_status": "AUTHORITATIVE",
        "source": "CGHS_RATE_CARDS"
    }
]

# 2. PM-JAY & Indian Standard Procedure Master Tariffs (Authoritative Reference)
PROCEDURES_MASTER = [
    {
        "specialty_code": "CAR",
        "specialty_name": "Cardiology & Cardiothoracic Surgery",
        "procedure_code": "CAR-001",
        "procedure_name": "Coronary Angiography (CAG)",
        "package_rate": 15000.0,
        "nabh_rate": 17250.0,
        "preauth_required": False,
        "data_status": "AUTHORITATIVE",
        "source": "PMJAY_HBP_2022"
    },
    {
        "specialty_code": "CAR",
        "specialty_name": "Cardiology & Cardiothoracic Surgery",
        "procedure_code": "CAR-002",
        "procedure_name": "Coronary Angioplasty (PTCA) with 1 DES Stent",
        "package_rate": 85000.0,
        "nabh_rate": 97750.0,
        "preauth_required": True,
        "data_status": "AUTHORITATIVE",
        "source": "PMJAY_HBP_2022"
    },
    {
        "specialty_code": "CAR",
        "specialty_name": "Cardiology & Cardiothoracic Surgery",
        "procedure_code": "CAR-003",
        "procedure_name": "Coronary Artery Bypass Graft (CABG - Off Pump)",
        "package_rate": 165000.0,
        "nabh_rate": 189750.0,
        "preauth_required": True,
        "data_status": "AUTHORITATIVE",
        "source": "PMJAY_HBP_2022"
    },
    {
        "specialty_code": "ORT",
        "specialty_name": "Orthopedics & Joint Replacement",
        "procedure_code": "ORT-001",
        "procedure_name": "Total Knee Replacement (TKR - Unilateral)",
        "package_rate": 110000.0,
        "nabh_rate": 126500.0,
        "preauth_required": True,
        "data_status": "AUTHORITATIVE",
        "source": "PMJAY_HBP_2022"
    },
    {
        "specialty_code": "ORT",
        "specialty_name": "Orthopedics & Joint Replacement",
        "procedure_code": "ORT-002",
        "procedure_name": "Total Hip Replacement (THR - Unilateral)",
        "package_rate": 125000.0,
        "nabh_rate": 143750.0,
        "preauth_required": True,
        "data_status": "AUTHORITATIVE",
        "source": "PMJAY_HBP_2022"
    },
    {
        "specialty_code": "GAS",
        "specialty_name": "Gastroenterology & GI Surgery",
        "procedure_code": "GAS-001",
        "procedure_name": "Laparoscopic Cholecystectomy",
        "package_rate": 35000.0,
        "nabh_rate": 40250.0,
        "preauth_required": True,
        "data_status": "AUTHORITATIVE",
        "source": "PMJAY_HBP_2022"
    },
    {
        "specialty_code": "ONC",
        "specialty_name": "Oncology",
        "procedure_code": "ONC-001",
        "procedure_name": "Modified Radical Mastectomy",
        "package_rate": 55000.0,
        "nabh_rate": 63250.0,
        "preauth_required": True,
        "data_status": "AUTHORITATIVE",
        "source": "PMJAY_HBP_2022"
    },
    {
        "specialty_code": "NEU",
        "specialty_name": "Neurology & Neurosurgery",
        "procedure_code": "NEU-001",
        "procedure_name": "Craniotomy for Evacuation of Hematoma",
        "package_rate": 95000.0,
        "nabh_rate": 109250.0,
        "preauth_required": True,
        "data_status": "AUTHORITATIVE",
        "source": "PMJAY_HBP_2022"
    }
]

# 3. Payers / Schemes
PAYERS_SCHEMES = [
    {
        "id": "STAR_HEALTH",
        "name": "Star Health and Allied Insurance",
        "type": "PRIVATE_INSURER",
        "cashless_available": True,
        "network_type": "CASHLESS_NETWORK"
    },
    {
        "id": "HDFC_ERGO",
        "name": "HDFC ERGO General Insurance",
        "type": "PRIVATE_INSURER",
        "cashless_available": True,
        "network_type": "CASHLESS_NETWORK"
    },
    {
        "id": "ICICI_LOMBARD",
        "name": "ICICI Lombard Health Care",
        "type": "PRIVATE_INSURER",
        "cashless_available": True,
        "network_type": "CASHLESS_NETWORK"
    },
    {
        "id": "CARE_HEALTH",
        "name": "Care Health Insurance",
        "type": "PRIVATE_INSURER",
        "cashless_available": True,
        "network_type": "CASHLESS_NETWORK"
    },
    {
        "id": "NIVA_BUPA",
        "name": "Niva Bupa Health Insurance",
        "type": "PRIVATE_INSURER",
        "cashless_available": True,
        "network_type": "CASHLESS_NETWORK"
    },
    {
        "id": "PMJAY",
        "name": "Ayushman Bharat PM-JAY",
        "type": "GOVERNMENT_CENTRAL",
        "cashless_available": True,
        "network_type": "GOVERNMENT_SCHEME"
    },
    {
        "id": "CGHS",
        "name": "Central Government Health Scheme",
        "type": "GOVERNMENT_CENTRAL",
        "cashless_available": True,
        "network_type": "GOVERNMENT_SCHEME"
    },
    {
        "id": "AROGYA_KARNATAKA",
        "name": "Ayushman Bharat - Arogya Karnataka (SAST)",
        "type": "GOVERNMENT_STATE",
        "cashless_available": True,
        "network_type": "GOVERNMENT_SCHEME"
    }
]

# 4. Realistic Indian Hospitals Master Seed (Focus: Bengaluru, Mumbai, Delhi Tier-1/2 Hubs)
HOSPITALS_SEED = [
    {
        "id": 1,
        "name": "Apollo Hospitals, Bannerghatta Road",
        "hfr_id": "IN2910000101",
        "facility_type": "PRIVATE_MULTISPECIALTY",
        "ownership": "PRIVATE_FOR_PROFIT",
        "address": "154/11, Opp. IIM-B, Bannerghatta Main Road",
        "city": "Bengaluru",
        "district": "Bengaluru Urban",
        "state": "Karnataka",
        "pincode": "560076",
        "latitude": 12.8958,
        "longitude": 77.5986,
        "phone": "+91-80-2630-4050",
        "email": "info_bengaluru@apollohospitals.com",
        "total_beds": 250,
        "icu_beds": 45,
        "emergency_available": True,
        "nabh_accredited": True,
        "specialties": ["CAR", "ORT", "NEU", "GAS", "ONC"],
        "empaneled_payers": ["STAR_HEALTH", "HDFC_ERGO", "ICICI_LOMBARD", "CARE_HEALTH", "CGHS"],
        "markup_multiplier": 1.25
    },
    {
        "id": 2,
        "name": "Manipal Hospital, Old Airport Road",
        "hfr_id": "IN2910000102",
        "facility_type": "PRIVATE_MULTISPECIALTY",
        "ownership": "PRIVATE_FOR_PROFIT",
        "address": "98, HAL Old Airport Road, Kodihalli",
        "city": "Bengaluru",
        "district": "Bengaluru Urban",
        "state": "Karnataka",
        "pincode": "560017",
        "latitude": 12.9592,
        "longitude": 77.6444,
        "phone": "+91-80-2502-4444",
        "email": "enquiry@manipalhospitals.com",
        "total_beds": 600,
        "icu_beds": 80,
        "emergency_available": True,
        "nabh_accredited": True,
        "specialties": ["CAR", "ORT", "NEU", "GAS", "ONC"],
        "empaneled_payers": ["STAR_HEALTH", "HDFC_ERGO", "NIVA_BUPA", "CGHS", "AROGYA_KARNATAKA"],
        "markup_multiplier": 1.30
    },
    {
        "id": 3,
        "name": "Sri Jayadeva Institute of Cardiovascular Sciences",
        "hfr_id": "IN2910000103",
        "facility_type": "GOVERNMENT_TERTIARY",
        "ownership": "PUBLIC",
        "address": "Bannerghatta Main Road, 9th Block, Jayanagar",
        "city": "Bengaluru",
        "district": "Bengaluru Urban",
        "state": "Karnataka",
        "pincode": "560069",
        "latitude": 12.9237,
        "longitude": 77.5937,
        "phone": "+91-80-2297-7400",
        "email": "director@jayadevacardiology.com",
        "total_beds": 1150,
        "icu_beds": 160,
        "emergency_available": True,
        "nabh_accredited": True,
        "specialties": ["CAR"],
        "empaneled_payers": ["PMJAY", "CGHS", "AROGYA_KARNATAKA", "STAR_HEALTH"],
        "markup_multiplier": 1.0
    },
    {
        "id": 4,
        "name": "Fortis Hospital, Cunningham Road",
        "hfr_id": "IN2910000104",
        "facility_type": "PRIVATE_MULTISPECIALTY",
        "ownership": "PRIVATE_FOR_PROFIT",
        "address": "14, Cunningham Road, Vasanth Nagar",
        "city": "Bengaluru",
        "district": "Bengaluru Urban",
        "state": "Karnataka",
        "pincode": "560052",
        "latitude": 12.9868,
        "longitude": 77.5974,
        "phone": "+91-80-4199-4444",
        "email": "care.cunningham@fortishealthcare.com",
        "total_beds": 150,
        "icu_beds": 30,
        "emergency_available": True,
        "nabh_accredited": True,
        "specialties": ["CAR", "ORT", "GAS"],
        "empaneled_payers": ["HDFC_ERGO", "ICICI_LOMBARD", "CARE_HEALTH"],
        "markup_multiplier": 1.28
    },
    {
        "id": 5,
        "name": "Victoria Hospital (BMCRI)",
        "hfr_id": "IN2910000105",
        "facility_type": "GOVERNMENT_TERTIARY",
        "ownership": "PUBLIC",
        "address": "Fort Road, Near City Market, Kalasipalya",
        "city": "Bengaluru",
        "district": "Bengaluru Urban",
        "state": "Karnataka",
        "pincode": "560002",
        "latitude": 12.9647,
        "longitude": 77.5758,
        "phone": "+91-80-2670-1150",
        "email": "medsupdt_vh@bmcri.org",
        "total_beds": 1000,
        "icu_beds": 120,
        "emergency_available": True,
        "nabh_accredited": False,
        "specialties": ["CAR", "ORT", "NEU", "GAS", "ONC"],
        "empaneled_payers": ["PMJAY", "AROGYA_KARNATAKA", "CGHS"],
        "markup_multiplier": 0.85
    },
    {
        "id": 6,
        "name": "Narayana Institute of Cardiac Sciences",
        "hfr_id": "IN2910000106",
        "facility_type": "PRIVATE_MULTISPECIALTY",
        "ownership": "PRIVATE_FOR_PROFIT",
        "address": "258/A, Bommasandra Industrial Area, Anekal Taluk",
        "city": "Bengaluru",
        "district": "Bengaluru Urban",
        "state": "Karnataka",
        "pincode": "560099",
        "latitude": 12.8093,
        "longitude": 77.6974,
        "phone": "+91-80-7122-2222",
        "email": "info.nics@narayanahealth.org",
        "total_beds": 800,
        "icu_beds": 140,
        "emergency_available": True,
        "nabh_accredited": True,
        "specialties": ["CAR", "ORT", "NEU", "ONC"],
        "empaneled_payers": ["STAR_HEALTH", "HDFC_ERGO", "ICICI_LOMBARD", "CARE_HEALTH", "NIVA_BUPA", "PMJAY", "AROGYA_KARNATAKA"],
        "markup_multiplier": 1.15
    },
    {
        "id": 7,
        "name": "Tata Memorial Hospital, Parel",
        "hfr_id": "IN2710000201",
        "facility_type": "GOVERNMENT_TERTIARY",
        "ownership": "PUBLIC",
        "address": "Dr. E Borges Road, Parel",
        "city": "Mumbai",
        "district": "Mumbai City",
        "state": "Maharashtra",
        "pincode": "400012",
        "latitude": 19.0044,
        "longitude": 72.8432,
        "phone": "+91-22-2417-7000",
        "email": "crs@tmc.gov.in",
        "total_beds": 700,
        "icu_beds": 90,
        "emergency_available": True,
        "nabh_accredited": True,
        "specialties": ["ONC", "NEU"],
        "empaneled_payers": ["PMJAY", "CGHS", "STAR_HEALTH", "HDFC_ERGO"],
        "markup_multiplier": 1.0
    },
    {
        "id": 8,
        "name": "All India Institute of Medical Sciences (AIIMS)",
        "hfr_id": "IN0710000301",
        "facility_type": "GOVERNMENT_TERTIARY",
        "ownership": "PUBLIC",
        "address": "Sri Aurobindo Marg, Ansari Nagar",
        "city": "New Delhi",
        "district": "New Delhi",
        "state": "Delhi",
        "pincode": "110029",
        "latitude": 28.5672,
        "longitude": 77.2100,
        "phone": "+91-11-2658-8500",
        "email": "director@aiims.edu",
        "total_beds": 2400,
        "icu_beds": 350,
        "emergency_available": True,
        "nabh_accredited": True,
        "specialties": ["CAR", "ORT", "NEU", "GAS", "ONC"],
        "empaneled_payers": ["PMJAY", "CGHS"],
        "markup_multiplier": 0.90
    }
]

def generate_canonical_datasets():
    print("[*] Generating canonical HOSPITALITY datasets...")
    
    # Save standard tariffs
    with open(os.path.join(PROCESSED_DIR, "cghs_room_tariffs.json"), "w", encoding="utf-8") as f:
        json.dump(CGHS_ROOM_TARIFFS, f, indent=2)
        
    with open(os.path.join(PROCESSED_DIR, "pmjay_procedure_tariffs.json"), "w", encoding="utf-8") as f:
        json.dump(PROCEDURES_MASTER, f, indent=2)
        
    with open(os.path.join(PROCESSED_DIR, "payers_schemes.json"), "w", encoding="utf-8") as f:
        json.dump(PAYERS_SCHEMES, f, indent=2)

    # Process and build complete hospital records with rooms, beds, tariffs
    full_hospitals = []
    
    for h in HOSPITALS_SEED:
        # Generate specific room types with tariffs
        h_rooms = []
        for r_base in CGHS_ROOM_TARIFFS:
            tariff = round(r_base["daily_tariff"] * h["markup_multiplier"], 0)
            h_rooms.append({
                "category": r_base["category"],
                "name": r_base["name"],
                "daily_tariff": tariff,
                "description": r_base["description"],
                "data_status": r_base["data_status"]
            })
            
        # Generate real-time synthetic bed inventories
        h_beds = []
        for r in h_rooms:
            if r["category"] == "GENERAL_WARD":
                tot = int(h["total_beds"] * 0.50)
            elif r["category"] == "SEMI_PRIVATE":
                tot = int(h["total_beds"] * 0.25)
            elif r["category"] == "PRIVATE_AC":
                tot = int(h["total_beds"] * 0.15)
            elif r["category"] == "DELUXE":
                tot = int(h["total_beds"] * 0.05)
            else: # ICU
                tot = h["icu_beds"]
                
            occ_ratio = random.uniform(0.70, 0.92)
            occupied = int(tot * occ_ratio)
            available = max(1, tot - occupied)
            
            h_beds.append({
                "category": r["category"],
                "total_beds": tot,
                "occupied_beds": occupied,
                "available_beds": available,
                "last_updated": datetime.now(timezone.utc).isoformat(),
                "data_status": "SIMULATED"
            })

        full_record = {
            **h,
            "rooms": h_rooms,
            "beds": h_beds
        }
        full_hospitals.append(full_record)

    with open(os.path.join(PROCESSED_DIR, "canonical_hospitals.json"), "w", encoding="utf-8") as f:
        json.dump(full_hospitals, f, indent=2)

    print(f"[+] Successfully generated {len(full_hospitals)} rich hospital entities with bed feeds and tariff matrices.")

if __name__ == "__main__":
    generate_canonical_datasets()
