import uvicorn

from fastapi import FastAPI
from routers import message
from config import settings

# from schemas import Message
# from data_types import Role, ResponseFinishReason


def get_app():
    app = FastAPI()
    app.include_router(message.router)

    return app

app = get_app()


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Hello World!"}


if __name__ == "__main__":
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
