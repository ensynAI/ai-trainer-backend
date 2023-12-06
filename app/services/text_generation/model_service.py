from abc import ABC, abstractmethod
from openai import OpenAI
from fastapi import HTTPException
from fastapi.responses import Response

from schemas import Message
from data_types import Model, ModelService, Role, ResponseFinishReason


class BaseModelService(ABC):
    """Base Template Model Service class"""
    @abstractmethod
    def send_request(self, messages):
        pass

    @abstractmethod
    def process_response(self, response):
        pass


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


class ModelServiceOpenAI(BaseModelService):
    """OpenAI Model Service class"""
    def __init__(self, **kwargs) -> None:
        self.client = OpenAI()
        self.model: Model = kwargs["MODEL"]

    def send_request(self, messages: list[Message]) -> Response:
        """Sends a request to the OpenAI API

        Args:
            messages (list[Message]): conversation containing all the history messages

        Returns:
            Response: model service response with the generated message
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )
        return response

    def process_response(self, response: Response) -> Message:
        """Extracts the generated message from the model's response

        Args:
            response (Response): model's response

        Returns:
            Message: message generated by the model
        """
        response_finish_reason = response.choices[0].finish_reason

        if response_finish_reason == ResponseFinishReason.STOP:
            return Message(role=Role.ASSISTANT, content=response.choices[0].message.content)
        else:
            self._handle_response_finish_reason(response_finish_reason)

    def _handle_response_finish_reason(self, finish_reason: ResponseFinishReason):
        """Handles the reason why the model stopped generating data.

        Args:
            finish_reason (ResponseFinishReason): reason returned by the model

        Raises:
            HTTPException: raised in case of an unknown reason
        """
        if finish_reason == ResponseFinishReason.LENGTH:
            self._handle_max_length_response()
        elif finish_reason == ResponseFinishReason.NULL:
            self._handle_null_response()
        elif finish_reason == ResponseFinishReason.CONTENT_FILTER:
            self._handle_content_filter_response()
        elif finish_reason == ResponseFinishReason.TOOL_CALLS or finish_reason == ResponseFinishReason.FUNCTION_CALL:
            self._handle_tool_calls_response()
        else:
            raise HTTPException(status_code=500, detail="Could not process the request.")

    def _handle_null_response(self):
        # TODO: API response still in progress or incomplete. Wait?
        raise HTTPException(status_code=504, detail="API response still in progress or incomplete.")

    def _handle_max_length_response(self):
        # Idea: summarize conversation?
        raise HTTPException(status_code=409,
                            detail="Sequence too long. The maximum number of tokens specified in the request was reached.")

    def _handle_content_filter_response(self):
        raise HTTPException(status_code=400, detail="Could not process the request as it did not pass the model's content filters.")

    def _handle_tool_calls_response(self):
        raise HTTPException(status_code=400, detail="Request caused the model to use an external tool (function).")