from pydantic import BaseModel, ConfigDict, Field
from pydantic_settings import BaseSettings


class RunSettings(BaseModel):
    host: str = Field(default="localhost")
    port: int = Field(default=8000)
    reload: bool = Field(default=True)


class Settings(BaseSettings):
    run: RunSettings = RunSettings()

    model_config = ConfigDict(
        case_sensitive = False,
        env_nested_delimiter = "__",
        env_prefix = "APP_CONFIG__",
        env_file = ".env",
    )

settings = Settings()