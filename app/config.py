from pydantic_settings import BaseSettings, SettingsConfigDict
from data_types import ModelService


class AppSettings(BaseSettings):
    # App
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    CHATBOT_SERVICE: ModelService = ModelService.OPENAI

    # Env variables
    # model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8')


app_settings = AppSettings()
