FROM python:3.9-slim-buster

SHELL ["/bin/bash", "-c"]

ENV APP_DIR=/opt/chord-progressions

COPY chord_progressions $APP_DIR/chord_progressions/
COPY tests $APP_DIR/tests/
COPY requirements.txt $APP_DIR/requirements.txt
COPY setup.cfg $APP_DIR/setup.cfg
COPY pyproject.toml $APP_DIR/pyproject.toml

WORKDIR $APP_DIR

RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["/bin/bash", "-c"]
