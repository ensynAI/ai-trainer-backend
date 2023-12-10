from services.ai_model import ModelServiceFactory

from config import app_settings
from .model_config import model_settings


chatbot_client = ModelServiceFactory.get_model_service(app_settings.CHATBOT_SERVICE,
                                                       **model_settings[app_settings.CHATBOT_SERVICE].model_dump()
                                                       )
