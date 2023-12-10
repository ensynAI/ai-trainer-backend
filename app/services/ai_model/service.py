from data_types import ModelService
from schemas import BaseModelService
from .open_ai import ModelServiceOpenAI


class ModelServiceFactory:
    """Model Service Factory class"""
    @staticmethod
    def get_model_service(model_service: ModelService, **kwargs) -> BaseModelService:
        """Function creating a corresponding model service given a model service name.

        Args:
            model_service (ModelService): name of the model service

        Raises:
            ValueError: raised when an unsupported model service name is provided.

        Returns:
            BaseModelService: _description_
        """
        if model_service == ModelService.OPENAI:
            return ModelServiceOpenAI(**kwargs)
        else:
            raise ValueError("Unsupported model service.")
