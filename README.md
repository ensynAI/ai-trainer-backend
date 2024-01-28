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

Also add poetry to path using:

```shell
export PATH="$HOME/.local/bin:$PATH"
```

## Configure environment

Enter the directory containing the `pyproject.toml` file and install all the dependencies using the following command

```shell
$ poetry install
```

Subsequently, add your `OPENAI_API_KEY` to your environment variables or create a `.env` file containing your API Key.

`.env` file structure:

```
OPENAI_API_KEY="your-api-key"
```

## Running the app

There are 2 ways to run the app. First go to the [app](app) directory and run one of the below commands:

1. Automatic. Using the prepared script

```shell
$ poetry run launch_app
```

or

```shell
$ poetry run python main.py
```

2. Manual

```shell
$ poetry run uvicorn main:app --reload
```
