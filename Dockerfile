FROM python:3

ENV NUM_WORKERS 4

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

COPY ./app /app
COPY ./instance /instance

EXPOSE 80

ENTRYPOINT gunicorn app:app -b 0.0.0.0:80 --log-level=debug