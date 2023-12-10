from abc import ABC, abstractmethod
from fastapi.responses import Response

from schemas import Message


class BaseModelService(ABC):
    """Base Template Model Service class"""
    @abstractmethod
    def initialize_conversation(self, initial_message: str, system_message: str=None, rules: str=None) -> list[Message]:
        pass

    @abstractmethod
    def generate_response_message(self, messages: list[Message]) -> Message:
        pass

    @abstractmethod
    def send_request(self, messages: list[Message]):
        pass

    @abstractmethod
    def process_response(self, response: Response):
        pass
