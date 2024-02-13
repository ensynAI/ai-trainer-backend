FROM python:3.11.8-slim-bookworm

ARG USERNAME=backend_app_user

ENV POETRY_VERSION=1.7.1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local'

RUN groupadd -r $USERNAME \
    && useradd -r -g $USERNAME $USERNAME

RUN pip install "poetry==$POETRY_VERSION"

COPY poetry.lock pyproject.toml /src/

WORKDIR /src

RUN poetry install --no-interaction --no-ansi --only main

COPY ./app /src/app
WORKDIR /src/app

EXPOSE 8000

USER $USERNAME

ENTRYPOINT [ "poetry", "run"]

CMD [ "launch_app" ]