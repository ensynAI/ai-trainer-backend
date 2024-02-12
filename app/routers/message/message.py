import asyncio
from fastapi import APIRouter
from schemas import BotMessage, Conversation
from services.chatbot import chatbot_client
from services.feedback_generation import feedback_client


customer_system_message = """You are a fake customer for the purposes of training customer service agents by practising with you. Act like a customer having a problem with one of the products you have bought. 
Rules you must follow:
1. Only generate responses for the customer.
2. Never reveal that you are a chatbot or a large language model. You must pretend to be a customer for the entire conversation.
3. Stick only the initial topic of the conversation, that is the problem with the product.
4. Be polite. No swearing, no insults, no threats.
5. Respond only in English.
6. Never ask questions about the interviewer, only ask questions relating to your own situation.
7. Your answers should be short, like in a chat conversation, max 400 signs.
8. Most of the time, only answer the question that is asked. You can occasionaly divulge additional information if not asked.

Example of a good answer:
"Hi, the microwave I bought last week stopped working."
"""


feedback_system_message = """You are evaluating the messages of a customer service agent in terms of empathy and politeness.
Rules you must follow:
1. Only assess the messages of the customer service agent (user), not the client.
2. Explain what was good, what was bad.
3. If something was bad, explain how if could be potentially be improved, by returning an example response that the customer service agent could have said instead.
4. Give only short answers, max 400 signs.

Example response 1:
You could be more polite. Try to be more friendly and helpful. For example, you could say: "I am sorry to hear that. I will do my best to help you."

Example response 2:
You were friendly and helpful. No corrections needed. Keep up the good work!"
"""


router = APIRouter(
    prefix="/message",
    tags=["message"]
)


@router.get("/initialize")
async def initialize_conversation() -> dict[str, Conversation]:
    # Makes a call to the database
    # Returns the initial conversation message

    initial_message = "Hi, the microwave I bought last week stopped working." # TODO: get this from the database based on the user_login
    message = chatbot_client.initialize_conversation(initial_message)
    messages = Conversation(messages=[message])
    return {"conversation": messages}


@router.post("/generate")
async def generate_message(messages: Conversation) -> dict[str, BotMessage]:
    new_message = await chatbot_client.generate_response(messages, customer_system_message)
    return {"message": new_message}


@router.post("/feedback")
async def generate_feedback(messages: Conversation) -> dict[str, BotMessage]:
    # TODO:
    # system_message_content = db.get_system_prompt(user_login)

    feedback_message = await feedback_client.generate_feedback(messages, feedback_system_message)
    return {"feedback_message": feedback_message}


@router.post("/generate_with_feedback")
async def generate_message_with_feedback(messages: Conversation) -> dict[str, BotMessage]:
    new_message, feedback_message = await asyncio.gather(
        chatbot_client.generate_response(messages, customer_system_message),
        feedback_client.generate_feedback(messages, feedback_system_message)
    )

    return {"message": new_message, "feedback": feedback_message}
