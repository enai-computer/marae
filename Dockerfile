FROM python:3.12

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app
COPY env-data /code/env-data

ENV RUN_MODE=prod

CMD ["fastapi", "run", "app/main.py", "--port", "80"]
