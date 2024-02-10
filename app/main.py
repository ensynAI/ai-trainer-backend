import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import message
from config import app_settings


def get_app():
    app = FastAPI()
    app.include_router(message.router)
    return app

app = get_app()


origins = ["http://localhost", "http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Hello World!"}


def launch_app():
    """Lanches the app"""
    uvicorn.run("main:app", 
                host=app_settings.HOST, 
                port=app_settings.PORT, 
                reload=app_settings.RELOAD)

if __name__ == "__main__":
    launch_app()
