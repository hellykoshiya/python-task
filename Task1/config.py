from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=Path(__file__).resolve().parent / ".env")
    APP_NAME: str
    DEBUG: bool
    TAX_RATE: float


settings = Settings()

print("App Name:", settings.APP_NAME)
print("Debug:", settings.DEBUG)
print("Tax Rate:", settings.TAX_RATE)
