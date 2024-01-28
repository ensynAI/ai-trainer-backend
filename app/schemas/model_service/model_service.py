from abc import ABC, abstractmethod
from fastapi.responses import Response

from schemas import Message


class BaseModelService(ABC):
    """Base Template Model Service class"""
    @abstractmethod
    def initialize_conversation(self, initial_message: str) -> list[Message]:
        pass

    @abstractmethod
    def generate_response(self, messages: list[Message], system_message: str = None) -> Message:
        pass

    @abstractmethod
    def generate_feedback(self, messages: list[Message], system_message: str = None) -> Message:
        pass

    @abstractmethod
    def send_request(self, messages: list[Message]):
        pass

    @abstractmethod
    def process_response(self, response: Response):
        pass
