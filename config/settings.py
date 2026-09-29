from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    # Field names match the .env keys directly
    GCP_PROJECT_ID: str = "dental-clinic-rag"
    BIGQUERY_DATASET: str = "dental_service"
    GCP_REGION: str = "australia-southeast2"
    GOOGLE_APPLICATION_CREDENTIALS: str = "service_account.json"
    BATCH_CHUNK_SIZE: int = 50000
    RANDOM_SEED: int = 42

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Aliases so generate_and_load.py can use settings.PROJECT_ID, settings.DATASET_ID, etc.
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