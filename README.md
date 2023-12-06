# Customer Service AI Trainer Platform - Backend

## Directory structure

```
├── main.py
├── config.py
├── data_types
├── routers
│   ├── ...
│   └── ...
├── schemas
│   ├── schema_1
│   └── schema_2
└── services
    ├── service_1
    └── service_2
```

## Prerequisites

The project requirements are build using [poetry](https://python-poetry.org/docs/#installation). Install it configure the environment.

## Configure environment

Cd into the directory containing the `pyproject.toml` file and run the following command

```shell
$ poetry install
```

Subsequently, add your `OPENAI_API_KEY` to your environment variables or create a `.env` file containing your API Key.

`.env` file structure:

```
OPENAI_API_KEY="your-api-key"
```

## Running the app

There are 2 ways to run the app:

1. Automatic. Using the prepared script

```shell
$ sh run.sh
```

2. Manual

```shell
$ poetry run uvicorn main:app --reload
```
