from config import app_settings
from services.ai_model import ModelServiceFactory

from .model_config import model_settings


feedback_client = ModelServiceFactory.get_model_service(app_settings.FEEDBACK_SERVICE,
                                                        **model_settings[app_settings.FEEDBACK_SERVICE].model_dump()
                                                        )
