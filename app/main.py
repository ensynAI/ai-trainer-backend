import uvicorn

from fastapi import FastAPI
from routers import message
from config import app_settings


def get_app():
    app = FastAPI()
    app.include_router(message.router)
    return app

app = get_app()


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Hello World!"}


if __name__ == "__main__":
    uvicorn.run(app, host=app_settings.HOST, port=app_settings.PORT)
