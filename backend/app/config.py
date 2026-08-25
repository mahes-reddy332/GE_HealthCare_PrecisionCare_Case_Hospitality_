from pydantic_settings import BaseSettings, SettingsConfigDict

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
