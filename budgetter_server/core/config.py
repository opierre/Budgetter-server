from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings and configuration.

    Attributes:
        PROJECT_NAME: Name of the project.
        API_V1_STR: API version prefix.
        DATABASE_URL: Database connection string.
        BACKEND_CORS_ORIGINS: List of allowed CORS origins.
    """
    PROJECT_NAME: str = "Budgetter Server"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str
    
    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env")


settings = Settings()
