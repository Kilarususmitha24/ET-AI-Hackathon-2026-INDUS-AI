from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "INDUS-AI"
    secret_key: str = "indus-ai-hackathon-2026-secret-key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.0-flash"
    embedding_model: str = "models/text-embedding-004"
    database_url: str = "sqlite:///./indus_ai.db"
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "indusai2026"
    upload_dir: str = "./uploads"
    faiss_index_dir: str = "./data/faiss"
    tesseract_cmd: str = ""
    cors_origins: str = "http://localhost:5173,http://localhost:3000"
    chunk_size: int = 1000
    chunk_overlap: int = 200
    top_k_retrieval: int = 5

    class Config:
        env_file = ".env"
        extra = "ignore"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
