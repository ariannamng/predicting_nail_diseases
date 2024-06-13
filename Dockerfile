FROM python:3.8.12-buster

RUN pip install -U pip

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY models /models

COPY predicting_nails /predicting_nails
COPY setup.py /setup.py

COPY API /API
COPY gen_ai /gen_ai

CMD uvicorn API.api:app --host 0.0.0.0 --port $PORT
