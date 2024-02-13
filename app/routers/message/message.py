import asyncio
from fastapi import APIRouter
from schemas import BotMessage, Conversation
from services.chatbot import chatbot_client
from services.feedback_generation import feedback_client

from config import app_settings


router = APIRouter(
    prefix="/message",
    tags=["message"]
)


@router.get("/initialize")
async def initialize_conversation() -> dict[str, Conversation]:
    # TODO: Make a call to the database
    # Returns the initial conversation message based on the user_login

    message = chatbot_client.initialize_conversation(app_settings.INITIAL_MESSAGE)
    messages = Conversation(messages=[message])
    return {"conversation": messages}


@router.post("/generate")
async def generate_message(messages: Conversation) -> dict[str, BotMessage]:
    new_message = await chatbot_client.generate_response(messages, app_settings.CUSTOMER_SYSTEM_MESSAGE)
    return {"message": new_message}


@router.post("/feedback")
async def generate_feedback(messages: Conversation) -> dict[str, BotMessage]:
    feedback_message = await feedback_client.generate_feedback(messages, app_settings.FEEDBACK_SYSTEM_MESSAGE)
    return {"feedback_message": feedback_message}


@router.post("/generate_with_feedback")
async def generate_message_with_feedback(messages: Conversation) -> dict[str, BotMessage]:
    new_message, feedback_message = await asyncio.gather(
        chatbot_client.generate_response(messages, app_settings.CUSTOMER_SYSTEM_MESSAGE),
        feedback_client.generate_feedback(messages, app_settings.FEEDBACK_SYSTEM_MESSAGE)
    )

    return {"message": new_message, "feedback": feedback_message}
