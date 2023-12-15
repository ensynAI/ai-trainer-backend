from fastapi import APIRouter
from schemas import Message
from services.chatbot import chatbot_client
from services.feedback_generation import feedback_client

router = APIRouter(
    prefix="/message",
    tags=["message"]
)


@router.post("/generate")
def generate_message(messages: list[Message]) -> dict[str, Message]:
    new_message = chatbot_client.generate_response(messages)
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


@router.post("/feedback")
def generate_feedback(messages: list[Message]) -> dict[str, Message]:
    # TODO:
    # system_message_content = db.get_system_prompt(user_login)

    system_message = "Give only short answers, max 400 signs. You are responsible for evaluating messages of a customer service agent in terms of empathy they show. Provide a user with short instructions on how he could improve the message to be more polite, kind and empathetic. Return an example. Furthermore, give a score from 0 to 10, assessing the politeness and empathy of a message sent by the user, where 0 is super impolite, and 10 is perfectly polite. Return the score in the format of: {'SCORE': VALUE}."

    feedback_message = feedback_client.generate_feedback(messages,
                                                         system_message)
    
    return {"feedback_message": feedback_message}
