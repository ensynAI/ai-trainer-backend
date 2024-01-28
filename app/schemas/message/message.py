from pydantic import BaseModel
from data_types.data_types import Role


class Message(BaseModel):
    role: Role = "user"
    content: str

    def __str__(self) -> str:
        return self.model_dump_json()

    def __repr__(self) -> str:
        return self.model_dump_json()


class Conversation(BaseModel):
    messages: list[Message]
    
    def __str__(self) -> str:
        return self.model_dump_json()
    
    def __repr__(self) -> str:
        return self.model_dump_json()
