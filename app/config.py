from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "SHL Assessment Recommender"
    app_version: str = "1.0.0"

    catalog_path: str = "data/processed_catalog.json"
    raw_catalog_path: str = "data/raw_catalog.json"
    vector_index_path: str = "data/vector_index/index.faiss"
    vector_metadata_path: str = "data/vector_index/metadata.json"

    max_recommendations: int = 10
    gemini_api_key: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()