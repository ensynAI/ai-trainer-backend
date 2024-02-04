from abc import ABC, abstractmethod
from fastapi.responses import Response

from schemas import Message, BotMessage, Conversation


class BaseModelService(ABC):
    """Base Template Model Service class"""
    @abstractmethod
    def initialize_conversation(self, initial_message: str) -> Conversation:
        pass

    @abstractmethod
    async def generate_response(self, messages: Conversation, system_message: str = None) -> BotMessage:
        pass

    @abstractmethod
    async def generate_feedback(self, messages: Conversation, system_message: str = None) -> BotMessage:
        pass

    @abstractmethod
    async def send_request(self, messages: Conversation):
        pass

    @abstractmethod
    def process_response(self, response: Response):
        pass
