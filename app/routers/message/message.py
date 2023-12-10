from fastapi import APIRouter
from schemas import Message
from services.chatbot import chatbot_client

router = APIRouter(
    prefix="/message",
    tags=["message"]
)


@router.post("/generate")
def generate_message(messages: list[Message]) -> dict[str, Message]:
    new_message = chatbot_client.generate_response_message(messages)
    return {"message": new_message}


@router.post("/initialize")
def initialize_conversation() -> dict[str, list[Message]]:
    # Makes a call to the database
    # Based on the user_login retrieves the company details and hence the initial prompt message
    # Returns the initial conversation message

    # TODO:
    # system_message_content = db.get_system_prompt(user_login)
    # assistant_message_content = db.get_assistant_prompt(user_login)

    system_message = "You are a fake customer for the purposes of training customer service agents by practising with you. Act like a customer having a problem with one of the products you have bought. Only generate responses for the customer."
    initial_message = "Hi, the microwave I bought last week stopped working"

    messages = chatbot_client.initialize_conversation(initial_message, system_message)

    return {"messages": messages}


# @route.post("/feedback")
# def generate_feedback(messages: list[Message] = []) -> dict[str, Message]:
#     feedback_message = None
#     return {"feedback_message": feedback_message}
