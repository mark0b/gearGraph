FROM python:3

ENV NUM_WORKERS 4

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY ./app /app

ENTRYPOINT gunicorn -w ${NUM_WORKERS} app:app
