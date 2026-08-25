from fastapi import FastAPI
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
