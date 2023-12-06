from fastapi import APIRouter
from openai import OpenAI
from schemas import Message
from data_types import Role, ResponseFinishReason
from config import settings

from .service import handle_response_finish_reason


router = APIRouter(
    prefix="/message",
    tags=["message"]
)

def get_model():
    return OpenAI()


client = get_model()


@router.post("/generate")
def generate_message(messages: list[Message]) -> dict[str, Message]:
    response = client.chat.completions.create(
        model=settings.MODEL,
        messages=messages,
    )
    response_finish_reason = response.choices[0].finish_reason

    if response_finish_reason == ResponseFinishReason.STOP:
        new_message = Message(role=Role.ASSISTANT, content=response.choices[0].message.content)
    else:
        handle_response_finish_reason(response_finish_reason)
    return {"message": new_message}


# @app.post("/initial")


# @app.post("/feedback")



