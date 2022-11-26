FROM python:3.10-slim-bullseye

ENV VIRTUAL_ENV=/usr/local/python

RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN apt-get update \
    && apt-get install -y netcat

RUN python -m pip install --upgrade pip
RUN pip install poetry

WORKDIR /code

COPY . /code/

RUN poetry install --without=dev
