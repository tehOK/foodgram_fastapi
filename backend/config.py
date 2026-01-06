from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field
from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).resolve().parent

class RunSettings(BaseModel):
    host: str = Field(default="localhost")
    port: int = Field(default=8008)
    reload: bool = Field(default=True)

class DBSettings(BaseModel):
    db_url: str = Field(default="sqlite+aiosqlite:///./test.db")
    echo: bool = Field(default=False)

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

class AuthSettings(BaseModel):
    private_jwt_path: str = BASE_DIR / "secrets" / "jwt_private.pem"
    public_jwt_path: str = BASE_DIR / "secrets" / "jwt_public.pem"
    jwt_algorithm: str = "RS256"

class Settings(BaseSettings):
    run: RunSettings = RunSettings()
    db: DBSettings = DBSettings()

    model_config = ConfigDict(
        case_sensitive = False,
        env_nested_delimiter = "__",
        env_prefix = "APP_CONFIG__",
        env_file = ".env",
    )

settings = Settings()