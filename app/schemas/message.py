from pydantic import BaseModel
from data_types.data_types import Role


class Message(BaseModel):
    role: Role
    content: str

    def __str__(self) -> str:
        return self.model_dump_json()

    def __repr__(self) -> str:
        return self.model_dump_json()


class UserMessage(Message):
    role: Role = "user"
    feedback: str = None


class BotMessage(Message):
    role: Role = "assistant"


class SystemMessage(Message):
    role: Role = "system"


class Conversation(BaseModel):
    messages: list[Message]
    
    def __str__(self) -> str:
        return self.model_dump_json()
    
    def __repr__(self) -> str:
        return self.model_dump_json()
