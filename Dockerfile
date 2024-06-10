FROM python:3.8.12-buster

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY predicting_nails predicting_nails
COPY setup.py setup.py

COPY API /API
COPY app /app
COPY gen_ai /gen_ai

RUN pip install .

CMD uvicorn API.api:app --host 0.0.0.0 --port $PORT
