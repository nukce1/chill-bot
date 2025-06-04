from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    bot_token: str
    backend_url: str

    log_level: str
    log_format: str
    log_date_format: str
    log_path: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()

from aiogram.types import BotCommand

BOT_COMMANDS = [
    BotCommand(command="/start", description="Start"),
]
