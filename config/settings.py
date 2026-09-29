from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    # GCP Infrastructure
    GCP_PROJECT_ID: str = "dental-clinic-rag"
    BIGQUERY_DATASET: str = "dental_service"
    GCP_REGION: str = "australia-southeast2"
    GOOGLE_APPLICATION_CREDENTIALS: str = "service_account.json"
    BATCH_CHUNK_SIZE: int = 50000
    RANDOM_SEED: int = 42

    # Model Configuration & API Keys
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-3.5-flash-lite"
    EMBEDDING_MODEL: str = "text-embedding-004"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Aliases
    @property
    def PROJECT_ID(self) -> str:
        return self.GCP_PROJECT_ID

    @property
    def DATASET_ID(self) -> str:
        return self.BIGQUERY_DATASET

    @property
    def REGION(self) -> str:
        return self.GCP_REGION

    @property
    def full_credentials_path(self) -> Path:
        cred_path = Path(self.GOOGLE_APPLICATION_CREDENTIALS)
        return cred_path if cred_path.is_absolute() else BASE_DIR / cred_path

settings = Settings()