from pydantic_settings import BaseSettings, SettingsConfigDict
from data_types import Model


class Settings(BaseSettings):
    # App
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Model
    MODEL: Model = Model.GPT_3_5_TURBO

    # Env variables
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8')


settings = Settings()
