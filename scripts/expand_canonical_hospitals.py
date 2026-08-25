import json
import os
import math

hospitals = [
    # --- BENGALURU ---
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
        "specialties": ["cardiology", "icu", "cath_lab", "emergency", "radiology", "oncology", "orthopedics", "diagnostics"],
        "empaneled_payers": ["STAR_HEALTH", "HDFC_ERGO", "ICICI_LOMBARD", "CARE_HEALTH", "CGHS"],
        "markup_multiplier": 1.25,
        "rooms": [
            {"category": "GENERAL", "name": "General Ward Bed", "daily_tariff": 2000.0, "status": "COMPATIBLE", "description": "Multi-occupancy ward", "data_status": "AUTHORITATIVE"},
            {"category": "SEMI_PRIVATE", "name": "Semi-Private Room", "daily_tariff": 4500.0, "status": "COMPATIBLE", "description": "Twin sharing room", "data_status": "AUTHORITATIVE"},
            {"category": "PRIVATE", "name": "Single Private A/C Room", "daily_tariff": 8000.0, "status": "EXCEEDS_CAP", "description": "Private room", "data_status": "AUTHORITATIVE"},
            {"category": "ICU", "name": "Intensive Care Unit (ICU)", "daily_tariff": 12000.0, "status": "VERIFY", "description": "Critical care ICU", "data_status": "AUTHORITATIVE"}
        ],
        "beds": [
            {"category": "GENERAL", "total_beds": 60, "occupied_beds": 52, "available_beds": 8, "data_status": "SIMULATED"},
            {"category": "SEMI_PRIVATE", "total_beds": 20, "occupied_beds": 17, "available_beds": 3, "data_status": "SIMULATED"},
            {"category": "PRIVATE", "total_beds": 15, "occupied_beds": 13, "available_beds": 2, "data_status": "SIMULATED"},
            {"category": "ICU", "total_beds": 12, "occupied_beds": 9, "available_beds": 3, "data_status": "SIMULATED"}
        ]
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
        "specialties": ["cardiology", "icu", "emergency", "radiology", "orthopedics", "dialysis"],
        "empaneled_payers": ["STAR_HEALTH", "HDFC_ERGO", "NIVA_BUPA", "CGHS", "AROGYA_KARNATAKA"],
        "markup_multiplier": 1.3,
        "rooms": [
            {"category": "GENERAL", "name": "General Ward Bed", "daily_tariff": 2200.0, "status": "COMPATIBLE", "description": "Multi-occupancy ward", "data_status": "AUTHORITATIVE"},
            {"category": "SEMI_PRIVATE", "name": "Semi-Private Room", "daily_tariff": 4800.0, "status": "COMPATIBLE", "description": "Twin sharing room", "data_status": "AUTHORITATIVE"},
            {"category": "PRIVATE", "name": "Single Private A/C Room", "daily_tariff": 8500.0, "status": "EXCEEDS_CAP", "description": "Private room", "data_status": "AUTHORITATIVE"},
            {"category": "ICU", "name": "Intensive Care Unit (ICU)", "daily_tariff": 13000.0, "status": "VERIFY", "description": "Critical care ICU", "data_status": "AUTHORITATIVE"}
        ],
        "beds": [
            {"category": "GENERAL", "total_beds": 100, "occupied_beds": 82, "available_beds": 18, "data_status": "SIMULATED"},
            {"category": "SEMI_PRIVATE", "total_beds": 35, "occupied_beds": 27, "available_beds": 8, "data_status": "SIMULATED"},
            {"category": "PRIVATE", "total_beds": 25, "occupied_beds": 21, "available_beds": 4, "data_status": "SIMULATED"},
            {"category": "ICU", "total_beds": 20, "occupied_beds": 19, "available_beds": 1, "data_status": "SIMULATED"}
        ]
    },
    {
        "id": 3,
        "name": "Sri Jayadeva Institute of Cardiovascular Sciences",
        "hfr_id": "IN2910000103",
        "facility_type": "GOVERNMENT_AUTONOMOUS",
        "ownership": "STATE_GOVERNMENT",
        "address": "Jayanagar 9th Block, Bannerghatta Road",
        "city": "Bengaluru",
        "district": "Bengaluru Urban",
        "state": "Karnataka",
        "pincode": "560069",
        "latitude": 12.9182,
        "longitude": 77.5929,
        "phone": "+91-80-2297-7400",
        "email": "director@jayadevacardiology.com",
        "total_beds": 600,
        "icu_beds": 120,
        "emergency_available": True,
        "nabh_accredited": True,
        "specialties": ["cardiology", "icu", "cath_lab", "emergency", "radiology", "diagnostics"],
        "empaneled_payers": ["STAR_HEALTH", "HDFC_ERGO", "PM_JAY", "CGHS", "AROGYA_KARNATAKA"],
        "markup_multiplier": 1.0,
        "rooms": [
            {"category": "GENERAL", "name": "General Ward Bed", "daily_tariff": 1200.0, "status": "COMPATIBLE", "description": "Subsidized ward", "data_status": "AUTHORITATIVE"},
            {"category": "SEMI_PRIVATE", "name": "Semi-Private Room", "daily_tariff": 3000.0, "status": "COMPATIBLE", "description": "Twin sharing room", "data_status": "AUTHORITATIVE"},
            {"category": "PRIVATE", "name": "Single Private Room", "daily_tariff": 5000.0, "status": "COMPATIBLE", "description": "Special room", "data_status": "AUTHORITATIVE"},
            {"category": "ICU", "name": "Intensive Care Unit (ICU)", "daily_tariff": 8000.0, "status": "VERIFY", "description": "CCU", "data_status": "AUTHORITATIVE"}
        ],
        "beds": [
            {"category": "GENERAL", "total_beds": 200, "occupied_beds": 178, "available_beds": 22, "data_status": "SIMULATED"},
            {"category": "SEMI_PRIVATE", "total_beds": 50, "occupied_beds": 38, "available_beds": 12, "data_status": "SIMULATED"},
            {"category": "PRIVATE", "total_beds": 30, "occupied_beds": 26, "available_beds": 4, "data_status": "SIMULATED"},
            {"category": "ICU", "total_beds": 40, "occupied_beds": 34, "available_beds": 6, "data_status": "SIMULATED"}
        ]
    },

    # --- HYDERABAD ---
    {
        "id": 4,
        "name": "Apollo Hospitals, Jubilee Hills",
        "hfr_id": "IN3610000201",
        "facility_type": "PRIVATE_MULTISPECIALTY",
        "ownership": "PRIVATE_FOR_PROFIT",
        "address": "Road No 72, Opp. Bharatiya Vidya Bhavan, Film Nagar, Jubilee Hills",
        "city": "Hyderabad",
        "district": "Hyderabad",
        "state": "Telangana",
        "pincode": "500096",
        "latitude": 17.4184,
        "longitude": 78.4116,
        "phone": "+91-40-2360-7777",
        "email": "info_hyderabad@apollohospitals.com",
        "total_beds": 550,
        "icu_beds": 90,
        "emergency_available": True,
        "nabh_accredited": True,
        "specialties": ["cardiology", "icu", "cath_lab", "emergency", "radiology", "oncology", "orthopedics", "diagnostics", "dialysis"],
        "empaneled_payers": ["STAR_HEALTH", "HDFC_ERGO", "ICICI_LOMBARD", "CARE_HEALTH", "CGHS", "AAROGYASRI"],
        "markup_multiplier": 1.25,
        "rooms": [
            {"category": "GENERAL", "name": "General Ward Bed", "daily_tariff": 1900.0, "status": "COMPATIBLE", "description": "Multi-occupancy ward", "data_status": "AUTHORITATIVE"},
            {"category": "SEMI_PRIVATE", "name": "Semi-Private Room", "daily_tariff": 4200.0, "status": "COMPATIBLE", "description": "Twin sharing room", "data_status": "AUTHORITATIVE"},
            {"category": "PRIVATE", "name": "Single Private A/C Room", "daily_tariff": 7800.0, "status": "EXCEEDS_CAP", "description": "Private room", "data_status": "AUTHORITATIVE"},
            {"category": "ICU", "name": "Intensive Care Unit (ICU)", "daily_tariff": 11500.0, "status": "VERIFY", "description": "Critical care ICU", "data_status": "AUTHORITATIVE"}
        ],
        "beds": [
            {"category": "GENERAL", "total_beds": 80, "occupied_beds": 64, "available_beds": 16, "data_status": "SIMULATED"},
            {"category": "SEMI_PRIVATE", "total_beds": 30, "occupied_beds": 24, "available_beds": 6, "data_status": "SIMULATED"},
            {"category": "PRIVATE", "total_beds": 25, "occupied_beds": 21, "available_beds": 4, "data_status": "SIMULATED"},
            {"category": "ICU", "total_beds": 18, "occupied_beds": 14, "available_beds": 4, "data_status": "SIMULATED"}
        ]
    },
    {
        "id": 5,
        "name": "Yashoda Hospitals, Somajiguda",
        "hfr_id": "IN3610000202",
        "facility_type": "PRIVATE_MULTISPECIALTY",
        "ownership": "PRIVATE_FOR_PROFIT",
        "address": "Raj Bhavan Road, Matha Nagar, Somajiguda",
        "city": "Hyderabad",
        "district": "Hyderabad",
        "state": "Telangana",
        "pincode": "500082",
        "latitude": 17.4244,
        "longitude": 78.4578,
        "phone": "+91-40-4567-4567",
        "email": "somajiguda@yashodamail.com",
        "total_beds": 450,
        "icu_beds": 75,
        "emergency_available": True,
        "nabh_accredited": True,
        "specialties": ["cardiology", "icu", "cath_lab", "emergency", "radiology", "oncology", "orthopedics"],
        "empaneled_payers": ["STAR_HEALTH", "HDFC_ERGO", "ICICI_LOMBARD", "CARE_HEALTH", "AAROGYASRI"],
        "markup_multiplier": 1.2,
        "rooms": [
            {"category": "GENERAL", "name": "General Ward Bed", "daily_tariff": 1800.0, "status": "COMPATIBLE", "description": "Multi-occupancy ward", "data_status": "AUTHORITATIVE"},
            {"category": "SEMI_PRIVATE", "name": "Semi-Private Room", "daily_tariff": 4000.0, "status": "COMPATIBLE", "description": "Twin sharing room", "data_status": "AUTHORITATIVE"},
            {"category": "PRIVATE", "name": "Single Private A/C Room", "daily_tariff": 7500.0, "status": "EXCEEDS_CAP", "description": "Private room", "data_status": "AUTHORITATIVE"},
            {"category": "ICU", "name": "Intensive Care Unit (ICU)", "daily_tariff": 11000.0, "status": "VERIFY", "description": "Critical care ICU", "data_status": "AUTHORITATIVE"}
        ],
        "beds": [
            {"category": "GENERAL", "total_beds": 70, "occupied_beds": 58, "available_beds": 12, "data_status": "SIMULATED"},
            {"category": "SEMI_PRIVATE", "total_beds": 25, "occupied_beds": 20, "available_beds": 5, "data_status": "SIMULATED"},
            {"category": "PRIVATE", "total_beds": 20, "occupied_beds": 17, "available_beds": 3, "data_status": "SIMULATED"},
            {"category": "ICU", "total_beds": 15, "occupied_beds": 13, "available_beds": 2, "data_status": "SIMULATED"}
        ]
    },
    {
        "id": 6,
        "name": "CARE Hospitals, Banjara Hills",
        "hfr_id": "IN3610000203",
        "facility_type": "PRIVATE_MULTISPECIALTY",
        "ownership": "PRIVATE_FOR_PROFIT",
        "address": "Road No 1, Prem Nagar, Banjara Hills",
        "city": "Hyderabad",
        "district": "Hyderabad",
        "state": "Telangana",
        "pincode": "500034",
        "latitude": 17.4147,
        "longitude": 78.4482,
        "phone": "+91-40-6165-6565",
        "email": "banjara@carehospitals.com",
        "total_beds": 300,
        "icu_beds": 50,
        "emergency_available": True,
        "nabh_accredited": True,
        "specialties": ["cardiology", "icu", "cath_lab", "emergency", "radiology", "diagnostics"],
        "empaneled_payers": ["STAR_HEALTH", "HDFC_ERGO", "NIVA_BUPA", "CGHS", "AAROGYASRI"],
        "markup_multiplier": 1.15,
        "rooms": [
            {"category": "GENERAL", "name": "General Ward Bed", "daily_tariff": 1700.0, "status": "COMPATIBLE", "description": "Multi-occupancy ward", "data_status": "AUTHORITATIVE"},
            {"category": "SEMI_PRIVATE", "name": "Semi-Private Room", "daily_tariff": 3800.0, "status": "COMPATIBLE", "description": "Twin sharing room", "data_status": "AUTHORITATIVE"},
            {"category": "PRIVATE", "name": "Single Private A/C Room", "daily_tariff": 7000.0, "status": "EXCEEDS_CAP", "description": "Private room", "data_status": "AUTHORITATIVE"},
            {"category": "ICU", "name": "Intensive Care Unit (ICU)", "daily_tariff": 10500.0, "status": "VERIFY", "description": "Critical care ICU", "data_status": "AUTHORITATIVE"}
        ],
        "beds": [
            {"category": "GENERAL", "total_beds": 50, "occupied_beds": 41, "available_beds": 9, "data_status": "SIMULATED"},
            {"category": "SEMI_PRIVATE", "total_beds": 20, "occupied_beds": 16, "available_beds": 4, "data_status": "SIMULATED"},
            {"category": "PRIVATE", "total_beds": 15, "occupied_beds": 13, "available_beds": 2, "data_status": "SIMULATED"},
            {"category": "ICU", "total_beds": 12, "occupied_beds": 10, "available_beds": 2, "data_status": "SIMULATED"}
        ]
    },
    {
        "id": 7,
        "name": "Nizam's Institute of Medical Sciences (NIMS)",
        "hfr_id": "IN3610000204",
        "facility_type": "GOVERNMENT_AUTONOMOUS",
        "ownership": "STATE_GOVERNMENT",
        "address": "Punjagutta, Hyderabad",
        "city": "Hyderabad",
        "district": "Hyderabad",
        "state": "Telangana",
        "pincode": "500082",
        "latitude": 17.4223,
        "longitude": 78.4526,
        "phone": "+91-40-2348-9000",
        "email": "nims@telangana.gov.in",
        "total_beds": 1400,
        "icu_beds": 180,
        "emergency_available": True,
        "nabh_accredited": True,
        "specialties": ["cardiology", "icu", "cath_lab", "emergency", "radiology", "dialysis", "oncology", "orthopedics"],
        "empaneled_payers": ["STAR_HEALTH", "HDFC_ERGO", "PM_JAY", "CGHS", "AAROGYASRI"],
        "markup_multiplier": 1.0,
        "rooms": [
            {"category": "GENERAL", "name": "General Ward Bed", "daily_tariff": 1000.0, "status": "COMPATIBLE", "description": "Subsidized government ward", "data_status": "AUTHORITATIVE"},
            {"category": "SEMI_PRIVATE", "name": "Semi-Private Room", "daily_tariff": 2500.0, "status": "COMPATIBLE", "description": "Twin sharing room", "data_status": "AUTHORITATIVE"},
            {"category": "PRIVATE", "name": "Single Private Room", "daily_tariff": 4500.0, "status": "COMPATIBLE", "description": "Special room", "data_status": "AUTHORITATIVE"},
            {"category": "ICU", "name": "Intensive Care Unit (ICU)", "daily_tariff": 7500.0, "status": "VERIFY", "description": "CCU", "data_status": "AUTHORITATIVE"}
        ],
        "beds": [
            {"category": "GENERAL", "total_beds": 400, "occupied_beds": 365, "available_beds": 35, "data_status": "SIMULATED"},
            {"category": "SEMI_PRIVATE", "total_beds": 100, "occupied_beds": 82, "available_beds": 18, "data_status": "SIMULATED"},
            {"category": "PRIVATE", "total_beds": 50, "occupied_beds": 44, "available_beds": 6, "data_status": "SIMULATED"},
            {"category": "ICU", "total_beds": 60, "occupied_beds": 53, "available_beds": 7, "data_status": "SIMULATED"}
        ]
    },

    # --- MUMBAI ---
    {
        "id": 8,
        "name": "Asian Heart Institute, BKC",
        "hfr_id": "IN2710000301",
        "facility_type": "PRIVATE_SUPERSPECIALTY",
        "ownership": "PRIVATE_FOR_PROFIT",
        "address": "G / N Block, Bandra Kurla Complex, Bandra East",
        "city": "Mumbai",
        "district": "Mumbai Suburban",
        "state": "Maharashtra",
        "pincode": "400051",
        "latitude": 19.0664,
        "longitude": 72.8687,
        "phone": "+91-22-6698-6666",
        "email": "info@ahimsl.com",
        "total_beds": 250,
        "icu_beds": 50,
        "emergency_available": True,
        "nabh_accredited": True,
        "specialties": ["cardiology", "icu", "cath_lab", "emergency", "radiology", "diagnostics"],
        "empaneled_payers": ["STAR_HEALTH", "HDFC_ERGO", "ICICI_LOMBARD", "CARE_HEALTH", "CGHS", "MAHATMA_JYOTIBA_PHULE"],
        "markup_multiplier": 1.35,
        "rooms": [
            {"category": "GENERAL", "name": "General Ward Bed", "daily_tariff": 2500.0, "status": "COMPATIBLE", "description": "Multi-occupancy ward", "data_status": "AUTHORITATIVE"},
            {"category": "SEMI_PRIVATE", "name": "Semi-Private Room", "daily_tariff": 5000.0, "status": "COMPATIBLE", "description": "Twin sharing room", "data_status": "AUTHORITATIVE"},
            {"category": "PRIVATE", "name": "Single Private A/C Room", "daily_tariff": 9500.0, "status": "EXCEEDS_CAP", "description": "Private room", "data_status": "AUTHORITATIVE"},
            {"category": "ICU", "name": "Intensive Care Unit (ICU)", "daily_tariff": 14000.0, "status": "VERIFY", "description": "Critical care ICU", "data_status": "AUTHORITATIVE"}
        ],
        "beds": [
            {"category": "GENERAL", "total_beds": 60, "occupied_beds": 49, "available_beds": 11, "data_status": "SIMULATED"},
            {"category": "SEMI_PRIVATE", "total_beds": 25, "occupied_beds": 21, "available_beds": 4, "data_status": "SIMULATED"},
            {"category": "PRIVATE", "total_beds": 20, "occupied_beds": 18, "available_beds": 2, "data_status": "SIMULATED"},
            {"category": "ICU", "total_beds": 15, "occupied_beds": 12, "available_beds": 3, "data_status": "SIMULATED"}
        ]
    },

    # --- DELHI ---
    {
        "id": 9,
        "name": "Fortis Escorts Heart Institute, Okhla",
        "hfr_id": "IN0710000401",
        "facility_type": "PRIVATE_SUPERSPECIALTY",
        "ownership": "PRIVATE_FOR_PROFIT",
        "address": "Okhla Road, Sukhdev Vihar Metro Station",
        "city": "New Delhi",
        "district": "South East Delhi",
        "state": "Delhi",
        "pincode": "110025",
        "latitude": 28.5601,
        "longitude": 77.2797,
        "phone": "+91-11-4713-5000",
        "email": "fehi@fortishealthcare.com",
        "total_beds": 310,
        "icu_beds": 65,
        "emergency_available": True,
        "nabh_accredited": True,
        "specialties": ["cardiology", "icu", "cath_lab", "emergency", "radiology", "diagnostics", "dialysis"],
        "empaneled_payers": ["STAR_HEALTH", "HDFC_ERGO", "ICICI_LOMBARD", "CARE_HEALTH", "CGHS", "PM_JAY"],
        "markup_multiplier": 1.3,
        "rooms": [
            {"category": "GENERAL", "name": "General Ward Bed", "daily_tariff": 2200.0, "status": "COMPATIBLE", "description": "Multi-occupancy ward", "data_status": "AUTHORITATIVE"},
            {"category": "SEMI_PRIVATE", "name": "Semi-Private Room", "daily_tariff": 4800.0, "status": "COMPATIBLE", "description": "Twin sharing room", "data_status": "AUTHORITATIVE"},
            {"category": "PRIVATE", "name": "Single Private A/C Room", "daily_tariff": 8800.0, "status": "EXCEEDS_CAP", "description": "Private room", "data_status": "AUTHORITATIVE"},
            {"category": "ICU", "name": "Intensive Care Unit (ICU)", "daily_tariff": 13500.0, "status": "VERIFY", "description": "Critical care ICU", "data_status": "AUTHORITATIVE"}
        ],
        "beds": [
            {"category": "GENERAL", "total_beds": 75, "occupied_beds": 62, "available_beds": 13, "data_status": "SIMULATED"},
            {"category": "SEMI_PRIVATE", "total_beds": 30, "occupied_beds": 25, "available_beds": 5, "data_status": "SIMULATED"},
            {"category": "PRIVATE", "total_beds": 25, "occupied_beds": 22, "available_beds": 3, "data_status": "SIMULATED"},
            {"category": "ICU", "total_beds": 20, "occupied_beds": 17, "available_beds": 3, "data_status": "SIMULATED"}
        ]
    }
]

out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "processed", "canonical_hospitals.json"))
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(hospitals, f, indent=2)

print(f"Successfully generated {len(hospitals)} canonical hospitals in Bengaluru, Hyderabad, Mumbai, and Delhi to {out_path}")
