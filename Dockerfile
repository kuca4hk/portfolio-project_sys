ARG VIRTUAL_ENV=/opt/venv

FROM python:3.11-slim AS base
RUN apt update && apt -y install curl gcc
RUN pip install poetry

FROM base AS build
ARG VIRTUAL_ENV
RUN python -m venv ${VIRTUAL_ENV}
ENV PATH="${VIRTUAL_ENV}/bin:$PATH"

#RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

WORKDIR /app
COPY . .
RUN . ${VIRTUAL_ENV}/bin/activate && poetry install

FROM base AS final
ARG VIRTUAL_ENV
ENV PYTHONBUFFERED=1

RUN useradd -u 1000 app

WORKDIR /app
USER app

COPY --from=build --chown=1000:1000 ${VIRTUAL_ENV} ${VIRTUAL_ENV}
ENV PATH="${VIRTUAL_ENV}/bin:$PATH"

COPY --chown=1000:1000 . .

EXPOSE 8000
