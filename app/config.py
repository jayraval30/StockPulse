from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    groq_api_key: str
    twilio_account_sid: str = "placeholder"
    twilio_auth_token: str = "placeholder"
    twilio_phone_number: str = "+10000000000"
    finnhub_api_key: str
    news_api_key: str
    user_phone_number: str = "+910000000000"
    watchlist: List[str] = ["NVDA", "AAPL", "TSLA"]

    model_config = SettingsConfigDict(
        env_file=str(ROOT_DIR / ".env"),
        env_file_encoding="utf-8"
    )


settings = Settings()