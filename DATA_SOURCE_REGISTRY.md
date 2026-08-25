# Data Source Registry — Indian Healthcare Ecosystem

**Registry Version**: 2.0 (Clean Reference)  
**Verification Date**: 2026-08-25  
**Coverage**: National & State Tier 1-3 Health Infrastructure, Public Schemes, Private Insurers, and Geographic Indices.

---

## 📊 Comprehensive Source Catalog

| Source ID | Source Name | Organization | Level | Access Type | Auth Needed | Reliability | Hackathon Status | Primary Data Fields |
|---|---|---|---|---|---|---|---|---|
| `DATA_GOV_IN_HOSPITALS` | Hospital Directory with Geo-Codes | Ministry of Health & Family Welfare | National | `DOWNLOAD_AVAILABLE` / `API_AVAILABLE` | No (Download) / API Key | High | **Active Ingestion** | Facility Name, Type, State, District, Address, Pincode, Lat, Lon, Bed Count, Phone |
| `PMJAY_HBP_2022` | PM-JAY Health Benefit Packages 2022 | National Health Authority (NHA) | National | `DOWNLOAD_AVAILABLE` | None | High | **Active Ingestion** | 1,949 Procedures, Specialty Codes, Package Rates (INR), Preauth Flags, Minimum LOS |
| `CGHS_RATE_CARDS` | Central Government Health Scheme Rate Cards | MoHFW | National | `DOWNLOAD_AVAILABLE` | None | High | **Active Ingestion** | Room Rent Benchmarks (General: ₹1.5k, Semi-Private: ₹3k, Private: ₹4.5k, ICU: ₹5.4k), 1,800+ Tariff Items |
| `CGHS_EMPANELLED` | CGHS Empanelled Hospital Directory | MoHFW | National (80+ Cities) | `DOWNLOAD_AVAILABLE` | None | High | **Active Ingestion** | Hospital Name, City, Address, NABH Status, Empanelled Specialties |
| `ABDM_HFR` | Health Facility Registry | ABDM / NHA | National | `SANDBOX_AVAILABLE` | OAuth2 (Sandbox) | High | **Reference Schema** | Facility ID, Verification Status, Infrastructure Specs, Services, HFR Unique ID |
| `OSM_INDIA_HEALTH` | OpenStreetMap India Healthcare Layer | OSM Community | National | `API_AVAILABLE` (Overpass) | None | Medium | **Geospatial Cross-Check** | OSM ID, Healthcare Type, Coordinates, Emergency Availability |
| `DATAMEET_GEO` | DataMeet Health Facilities GeoJSON | DataMeet | National | `DOWNLOAD_AVAILABLE` | None (Open) | Medium | **Geospatial Cross-Check** | Geo-coordinates, Administrative Hierarchy, Pincode Mapping |
| `NRCES_FHIR_R4` | NRCeS ABDM FHIR R4 Profiles | NRCeS / MoHFW | National | `DOWNLOAD_AVAILABLE` | None | High | **Standard Architecture** | FHIR Location, Organization, Coverage, CoverageEligibility, Claim Schemas |
| `NHCX_SANDBOX` | National Health Claims Exchange | NHA | National | `SANDBOX_AVAILABLE` | ABDM OAuth2 | High | **Reference Architecture** | Electronic Claims Workflows, Pre-auth Standards, Communication Specs |
| `SYNTHETIC_BED_FEED` | Real-Time Bed Availability Engine | HOSPITALITY Internal | Simulated | `GENERATED` | None | High (Synthetic) | **Simulated Active** | Real-time Occupied/Available Beds by Category (General, Semi-Private, Private, ICU) |
| `SYNTHETIC_INSURER_NETWORKS` | Private Insurer Empanelment Allocator | HOSPITALITY Internal | Simulated | `GENERATED` | None | High (Synthetic) | **Simulated Active** | Cashless Network Mappings for Star Health, HDFC ERGO, ICICI Lombard, Care Health, Niva Bupa |

---

## 🏷️ Provenance Classification Protocol

Every piece of information in the HOSPITALITY database is stamped with one of three status flags:
1. `AUTHORITATIVE`: Data directly retrieved and verified from official government portals (e.g. CGHS rate cards, PM-JAY package costs, data.gov.in hospital records).
2. `PUBLIC_VERIFIED`: Data harvested from public open data repositories and cross-referenced (e.g. OpenStreetMap coordinates, DataMeet district boundaries).
3. `SIMULATED`: Data generated algorithmically because live national APIs do not exist (e.g. minute-by-minute ICU bed counts, proprietary private insurer cashless agreements). Every simulated item is clearly flagged in the UI.
