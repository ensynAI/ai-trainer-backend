import uvicorn
from openai import OpenAI

from fastapi import FastAPI

from config import settings
from schemas import Message
from data_types import Role, ResponseFinishReason


def get_app():
    return FastAPI()


def get_model():
    return OpenAI()


app = get_app()
client = get_model()


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Hello World!"}


@app.post("/generate_message")
def generate_message(messages: list[Message]) -> dict[str, Message]:
    response = client.chat.completions.create(
        model=settings.MODEL,
        messages=messages
    )

    # validate_response(response) -> check response code etc.
    # if response["choices"][0]["finish_reason"] == ResponseFinishReason.LENGTH:
    #     handle_max_length_response()  # summarize conversation?

    # if response["choices"][0]["finish_reason"] == ResponseFinishReason.NULL:
    #     handle_null_response()

    if response.choices[0].finish_reason == ResponseFinishReason.STOP:
        new_message = Message(role=Role.ASSISTANT, content=response.choices[0].message.content)

    return {"message": new_message}


if __name__ == "__main__":
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
