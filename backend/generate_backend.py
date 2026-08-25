import os

base_dir = r"c:\Users\PC-ACER\Documents\GEHealthCare\backend"

files = {
    "requirements.txt": """fastapi>=0.110.0
uvicorn[standard]>=0.28.0
sqlalchemy[asyncio]>=2.0.28
aiosqlite>=0.20.0
pydantic>=2.6.0
pydantic-settings>=2.2.0
python-dotenv>=1.0.1
httpx>=0.27.0
aiofiles>=23.2.1
python-multipart>=0.0.9
pdfplumber>=0.11.0
PyPDF2>=3.0.1
pandas>=2.2.0
openpyxl>=3.1.2
geopy>=2.4.1
jinja2>=3.1.3
python-jose[cryptography]>=3.3.0
pytest>=8.0.0
pytest-asyncio>=0.23.0
""",
    "app/__init__.py": "",
    "app/models/__init__.py": "",
    "app/schemas/__init__.py": "",
    "app/services/__init__.py": "",
    "app/api/__init__.py": "",
    "app/scripts/__init__.py": "",
    
    "app/config.py": """from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./data/hospitality.db"
    APP_ENV: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = "supersecretkey"
    CORS_ORIGINS: list[str] = ["*"]
    
    LLM_PROVIDER: str = "mock"
    GEMINI_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    LLM_MODEL: str = "gemini-pro"
    
    ABDM_CLIENT_ID: str = ""
    ABDM_CLIENT_SECRET: str = ""
    ABDM_BASE_URL: str = ""
    NHCX_BASE_URL: str = ""
    
    DATA_GOV_IN_API_KEY: str = ""
    DATA_GOV_IN_BASE_URL: str = ""
    
    UPLOAD_DIR: str = "./uploads"
    DATA_DIR: str = "./data"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
""",
    "app/database.py": """from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from .config import settings
import os

os.makedirs(settings.DATA_DIR, exist_ok=True)
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

engine = create_async_engine(settings.DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
""",
    "app/models/provenance.py": """from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from ..database import Base
import enum
from datetime import datetime

class DataStatus(str, enum.Enum):
    AUTHORITATIVE = "AUTHORITATIVE"
    PUBLIC_VERIFIED = "PUBLIC_VERIFIED"
    SIMULATED = "SIMULATED"

class ConfidenceLevel(str, enum.Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class DataSource(Base):
    __tablename__ = "data_sources"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    status = Column(Enum(DataStatus))
    url = Column(String)

class DataRecord(Base):
    __tablename__ = "data_records"
    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("data_sources.id"))
    retrieved_at = Column(DateTime, default=datetime.utcnow)
    data_status = Column(Enum(DataStatus))
    confidence = Column(Enum(ConfidenceLevel))
    
    source = relationship("DataSource")
""",
    "app/models/hospital.py": """from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from ..database import Base
import enum

class OperationalStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

class Hospital(Base):
    __tablename__ = "hospitals"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    pincode = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    operational_status = Column(Enum(OperationalStatus), default=OperationalStatus.ACTIVE)
    
    identifiers = relationship("FacilityIdentifier", back_populates="hospital")
    specialties = relationship("FacilitySpecialty", back_populates="hospital")
    services = relationship("FacilityService", back_populates="hospital")
    rooms = relationship("BedInventory", back_populates="hospital")
    tariffs = relationship("Tariff", back_populates="hospital")
    schemes = relationship("HospitalScheme", back_populates="hospital")

class FacilityIdentifier(Base):
    __tablename__ = "facility_identifiers"
    id = Column(Integer, primary_key=True, index=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"))
    system = Column(String) # HFR, ROHINI, NIN
    value = Column(String)
    
    hospital = relationship("Hospital", back_populates="identifiers")

class FacilitySpecialty(Base):
    __tablename__ = "facility_specialties"
    id = Column(Integer, primary_key=True, index=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"))
    name = Column(String)
    
    hospital = relationship("Hospital", back_populates="specialties")

class FacilityService(Base):
    __tablename__ = "facility_services"
    id = Column(Integer, primary_key=True, index=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"))
    name = Column(String)
    
    hospital = relationship("Hospital", back_populates="services")
""",
    "app/models/scheme.py": """from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Scheme(Base):
    __tablename__ = "schemes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True) # e.g. PM-JAY, CGHS, Star Health
    type = Column(String) # GOVERNMENT, PRIVATE
    
    hospital_mappings = relationship("HospitalScheme", back_populates="scheme")

class HospitalScheme(Base):
    __tablename__ = "hospital_schemes"
    id = Column(Integer, primary_key=True, index=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"))
    scheme_id = Column(Integer, ForeignKey("schemes.id"))
    cashless_available = Column(Boolean, default=False)
    
    hospital = relationship("Hospital", back_populates="schemes")
    scheme = relationship("Scheme", back_populates="hospital_mappings")

class InsuranceNetwork(Base):
    __tablename__ = "insurance_networks"
    id = Column(Integer, primary_key=True, index=True)
    insurer = Column(String)
    product = Column(String)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"))
    cashless_status = Column(Boolean, default=False)
    tpa = Column(String)
""",
    "app/models/room.py": """from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from ..database import Base
from datetime import datetime
import enum

class RoomType(str, enum.Enum):
    GENERAL = "General"
    SEMI_PRIVATE = "Semi-Private"
    PRIVATE_AC = "Private AC"
    DELUXE = "Deluxe"
    ICU = "ICU"

class BedInventory(Base):
    __tablename__ = "bed_inventories"
    id = Column(Integer, primary_key=True, index=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"))
    room_type = Column(Enum(RoomType))
    total = Column(Integer)
    occupied = Column(Integer)
    available = Column(Integer)
    last_updated = Column(DateTime, default=datetime.utcnow)
    data_status = Column(String, default="SIMULATED")
    
    hospital = relationship("Hospital", back_populates="rooms")
""",
    "app/models/tariff.py": """from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Tariff(Base):
    __tablename__ = "tariffs"
    id = Column(Integer, primary_key=True, index=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"))
    specialty_code = Column(String)
    procedure_code = Column(String)
    procedure_name = Column(String)
    package_rate = Column(Float)
    nabh_rate = Column(Float, nullable=True)
    preauth_required = Column(Boolean, default=False)
    source = Column(String) # PMJAY, CGHS, HOSPITAL
    
    hospital = relationship("Hospital", back_populates="tariffs")
""",
    "app/models/policy.py": """from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Policy(Base):
    __tablename__ = "policies"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    policy_number = Column(String)
    insurer = Column(String)
    sum_insured = Column(Float)
    room_rent_cap_type = Column(String)
    room_rent_limit = Column(Float)
    icu_limit = Column(Float)
    copay_percentage = Column(Float, default=0)
    deductible = Column(Float, default=0)
    
    exclusions = relationship("PolicyExclusion", back_populates="policy")
    extractions = relationship("PolicyExtractionClause", back_populates="policy")

class PolicyExclusion(Base):
    __tablename__ = "policy_exclusions"
    id = Column(Integer, primary_key=True, index=True)
    policy_id = Column(Integer, ForeignKey("policies.id"))
    description = Column(String)
    
    policy = relationship("Policy", back_populates="exclusions")

class PolicyExtractionClause(Base):
    __tablename__ = "policy_extraction_clauses"
    id = Column(Integer, primary_key=True, index=True)
    policy_id = Column(Integer, ForeignKey("policies.id"))
    clause_type = Column(String)
    source_text = Column(String)
    page_number = Column(Integer)
    confidence = Column(String)
    
    policy = relationship("Policy", back_populates="extractions")
""",
    "app/models/patient.py": """from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from ..database import Base
from datetime import datetime
import enum

class JourneyEvent(str, enum.Enum):
    PRE_ADMISSION = "PRE_ADMISSION"
    HOSPITAL_SELECTION = "HOSPITAL_SELECTION"
    PRE_AUTH = "PRE_AUTH"
    ADMISSION = "ADMISSION"
    INVESTIGATION = "INVESTIGATION"
    PROCEDURE = "PROCEDURE"
    RECOVERY = "RECOVERY"
    DISCHARGE = "DISCHARGE"
    CLAIM = "CLAIM"

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    abha_id = Column(String, nullable=True)
    phone = Column(String)
    
    journeys = relationship("PatientJourney", back_populates="patient")

class PatientJourney(Base):
    __tablename__ = "patient_journeys"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    current_stage = Column(Enum(JourneyEvent))
    start_date = Column(DateTime, default=datetime.utcnow)
    
    patient = relationship("Patient", back_populates="journeys")
    events = relationship("JourneyEventLog", back_populates="journey")

class JourneyEventLog(Base):
    __tablename__ = "journey_events"
    id = Column(Integer, primary_key=True, index=True)
    journey_id = Column(Integer, ForeignKey("patient_journeys.id"))
    event_type = Column(Enum(JourneyEvent))
    description = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    journey = relationship("PatientJourney", back_populates="events")
""",
    "app/schemas/hospital.py": """from pydantic import BaseModel
from typing import List, Optional

class HospitalSearchParams(BaseModel):
    radius_km: Optional[float] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    specialty: Optional[str] = None
    payer: Optional[str] = None

class HospitalResponse(BaseModel):
    id: int
    name: str
    city: str
    state: str
    
    class Config:
        from_attributes = True

class HospitalComparisonResponse(BaseModel):
    hospitals: List[HospitalResponse]

class BedAvailabilityResponse(BaseModel):
    hospital_id: int
    room_type: str
    available: int
    total: int
""",
    "app/schemas/policy.py": """from pydantic import BaseModel
from typing import List, Optional

class PolicyCreate(BaseModel):
    policy_number: str
    insurer: str
    sum_insured: float

class PolicyResponse(BaseModel):
    id: int
    policy_number: str
    insurer: str
    sum_insured: float

    class Config:
        from_attributes = True

class PolicyExtracted(BaseModel):
    sum_insured: float
    room_rent_cap_type: str
    room_rent_limit: float
    icu_limit: float
    copay_percentage: float
    deductible: float

class PolicyUploadResponse(BaseModel):
    message: str
    extracted_data: PolicyExtracted
""",
    "app/schemas/matching.py": """from pydantic import BaseModel
from typing import List, Optional

class MatchRequest(BaseModel):
    patient_id: int
    lat: float
    lon: float
    procedure_code: str
    
class ExplainableOption(BaseModel):
    reason: str
    weight: float

class FacilityScore(BaseModel):
    hospital_id: int
    score: float
    reasons: List[ExplainableOption]
    
class RoomEligibilityResult(BaseModel):
    room_type: str
    eligible: bool
    
class ProportionateDeductionResult(BaseModel):
    net_patient_share: float
    deductions: float
    
class MatchResult(BaseModel):
    scores: List[FacilityScore]
""",
    "app/schemas/tariff.py": """from pydantic import BaseModel

class TariffResponse(BaseModel):
    id: int
    procedure_code: str
    procedure_name: str
    package_rate: float
    
    class Config:
        from_attributes = True

class CostBreakdownEstimate(BaseModel):
    procedure_cost: float
    room_cost: float
    total: float

class FinancialResponsibility(BaseModel):
    insurance_pays: float
    patient_pays: float
""",
    "app/schemas/journey.py": """from pydantic import BaseModel
from typing import List
from datetime import datetime
from ..models.patient import JourneyEvent

class JourneyEventCreate(BaseModel):
    event_type: JourneyEvent
    description: str

class JourneyEventResponse(BaseModel):
    id: int
    event_type: JourneyEvent
    description: str
    timestamp: datetime
    
    class Config:
        from_attributes = True

class JourneyResponse(BaseModel):
    id: int
    current_stage: JourneyEvent
    events: List[JourneyEventResponse]
    
    class Config:
        from_attributes = True
""",
    "app/schemas/fhir.py": """from pydantic import BaseModel
from typing import List, Optional

class FHIRLocation(BaseModel):
    resourceType: str = "Location"
    id: str
    name: str

class FHIROrganization(BaseModel):
    resourceType: str = "Organization"
    id: str
    name: str

class FHIRCoverage(BaseModel):
    resourceType: str = "Coverage"
    id: str
    status: str

class FHIRCovEligibilityRequest(BaseModel):
    resourceType: str = "CoverageEligibilityRequest"
    patient_id: str

class FHIRCovEligibilityResponse(BaseModel):
    resourceType: str = "CoverageEligibilityResponse"
    status: str
    
class FHIRClaim(BaseModel):
    resourceType: str = "Claim"
    status: str
""",
    "app/schemas/chat.py": """from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    message: str
    patient_id: Optional[int] = None

class ChatSourceCitation(BaseModel):
    source: str
    confidence: str

class ChatToolCall(BaseModel):
    tool: str
    args: str

class ChatResponse(BaseModel):
    reply: str
    citations: List[ChatSourceCitation] = []
""",
    "app/services/hospital_service.py": """from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from ..models.hospital import Hospital

class HospitalService:
    @staticmethod
    async def get_all_hospitals(db: AsyncSession):
        result = await db.execute(select(Hospital))
        return result.scalars().all()
    
    @staticmethod
    async def get_hospital(db: AsyncSession, hospital_id: int):
        result = await db.execute(select(Hospital).where(Hospital.id == hospital_id).options(selectinload(Hospital.rooms), selectinload(Hospital.tariffs)))
        return result.scalar_one_or_none()
""",
    "app/services/policy_service.py": """from ..schemas.policy import PolicyExtracted

class PolicyService:
    @staticmethod
    async def extract_from_pdf(file_path: str) -> PolicyExtracted:
        # Mock implementation for OCR / LLM fallback
        return PolicyExtracted(
            sum_insured=500000.0,
            room_rent_cap_type="1% of SI",
            room_rent_limit=5000.0,
            icu_limit=10000.0,
            copay_percentage=10.0,
            deductible=0.0
        )
""",
    "app/services/network_service.py": """class NetworkService:
    @staticmethod
    async def resolve_network(insurer: str, hospital_id: int):
        return {"cashless": True, "tpa": "MediAssist"}
""",
    "app/services/cost_service.py": """class CostService:
    @staticmethod
    def calculate_deductions(total_bill: float, copay_pct: float) -> float:
        return total_bill * (copay_pct / 100.0)
""",
    "app/services/matching_service.py": """class MatchingService:
    @staticmethod
    async def find_matches():
        return []
""",
    "app/services/fhir_service.py": """from ..schemas.fhir import FHIRLocation

class FHIRService:
    @staticmethod
    def convert_hospital_to_location(hospital_id: int, name: str) -> FHIRLocation:
        return FHIRLocation(id=str(hospital_id), name=name)
""",
    "app/services/chat_service.py": """from ..schemas.chat import ChatResponse

class ChatService:
    @staticmethod
    async def handle_query(query: str) -> ChatResponse:
        return ChatResponse(reply="I am a mock response.")
""",
    "app/api/hospitals.py": """from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..services.hospital_service import HospitalService
from ..schemas.hospital import HospitalResponse

router = APIRouter(prefix="/api/v1/hospitals", tags=["Hospitals"])

@router.get("", response_model=list[HospitalResponse])
async def list_hospitals(db: AsyncSession = Depends(get_db)):
    return await HospitalService.get_all_hospitals(db)

@router.get("/{id}")
async def get_hospital(id: int, db: AsyncSession = Depends(get_db)):
    return await HospitalService.get_hospital(db, id)
""",
    "app/api/policies.py": """from fastapi import APIRouter
router = APIRouter(prefix="/api/v1/policies", tags=["Policies"])

@router.post("/upload")
async def upload_policy():
    return {"message": "Mock upload success"}
""",
    "app/api/matching.py": """from fastapi import APIRouter
router = APIRouter(prefix="/api/v1/matching", tags=["Matching"])

@router.post("/hospitals")
async def match_hospitals():
    return []
""",
    "app/api/journey.py": """from fastapi import APIRouter
router = APIRouter(prefix="/api/v1/patients", tags=["Journey"])

@router.get("/{id}/journey")
async def get_journey(id: int):
    return {"message": "mock journey"}
""",
    "app/api/fhir.py": """from fastapi import APIRouter
router = APIRouter(prefix="/api/v1/fhir", tags=["FHIR"])

@router.get("/Location/{id}")
async def get_location(id: str):
    return {"resourceType": "Location", "id": id, "name": "Mock"}
""",
    "app/api/chat.py": """from fastapi import APIRouter
router = APIRouter(prefix="/api/v1/chat", tags=["Chat"])

@router.post("/query")
async def chat_query():
    return {"reply": "Mock"}
""",
    "app/api/data_sources.py": """from fastapi import APIRouter
router = APIRouter(prefix="/api/v1", tags=["DataSources"])

@router.get("/data-sources")
async def data_sources():
    return []
""",
    "app/api/health.py": """from fastapi import APIRouter
router = APIRouter(tags=["Health"])

@router.get("/health")
async def health_check():
    return {"status": "ok"}
""",
    "app/scripts/seed_database.py": """import asyncio
from ..database import init_db, AsyncSessionLocal
from ..models.hospital import Hospital, RoomType
from ..models.room import BedInventory

async def seed():
    await init_db()
    async with AsyncSessionLocal() as session:
        h1 = Hospital(name="Apollo Hospitals", city="Bengaluru", state="Karnataka", address="Bannerghatta Road")
        session.add(h1)
        await session.commit()
        print("Database seeded!")

if __name__ == "__main__":
    asyncio.run(seed())
""",
    "app/main.py": """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import contextlib
from .database import init_db
from .api import hospitals, policies, matching, journey, fhir, chat, data_sources, health

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(title="HOSPITALITY API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(hospitals.router)
app.include_router(policies.router)
app.include_router(matching.router)
app.include_router(journey.router)
app.include_router(fhir.router)
app.include_router(chat.router)
app.include_router(data_sources.router)
app.include_router(health.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
"""
}

for rel_path, content in files.items():
    full_path = os.path.join(base_dir, rel_path.replace("/", os.sep))
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

print("Files generated successfully.")
