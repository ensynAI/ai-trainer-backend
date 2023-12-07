from fastapi import APIRouter
from schemas import Message
from services.chatbot import chatbot_client

router = APIRouter(
    prefix="/message",
    tags=["message"]
)


@router.post("/generate")
def generate_message(messages: list[Message]) -> dict[str, Message]:
    response = chatbot_client.send_request(messages)
    new_message = chatbot_client.process_response(response)

    return {"message": new_message}


# @app.post("/initial")
# def initialize_conversation(user_login: str):
    # Makes a call to the database
    # Based on the user_login retrieves the company details
    # i.e. the input phrase to the SYSTEM model

    # Calls the prompt builder

    # Makes a call to the Model API initializing the conversation
    # returns the initial message to the client
    # ...
    # This functionality can be also implemented in the /generate_message endpoint


# @app.post("/feedback")
# def generate_feedback(messages: list[Message] = []) -> dict[str, Message]:
#     feedback_message = None
#     return {"feedback_message": feedback_message}
