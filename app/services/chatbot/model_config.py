from pydantic_settings import BaseSettings
from data_types import Model, ModelService


class OpenAIModelSettings(BaseSettings):
    # Model
    MODEL: Model = Model.GPT_3_5_TURBO


model_settings = {
    ModelService.OPENAI: OpenAIModelSettings()
    }
