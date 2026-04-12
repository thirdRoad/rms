FROM python:3.12-slim AS base

WORKDIR /app
ENV POETRY_VIRTUALENVS_CREATE=false

RUN apt update && apt upgrade -y && apt autoclean
RUN apt install vim -y
RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock ./

COPY flaskr /app/flaskr
COPY app.py app.py

FROM base AS dev

RUN poetry install --no-root

COPY tests /app/tests

COPY sh/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

FROM base AS prod

RUN poetry install --no-root --only main

COPY sh/prod-entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]