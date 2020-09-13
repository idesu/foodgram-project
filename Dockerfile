FROM python:3.8.5

WORKDIR /code

COPY . .

RUN apt update -y && apt install netcat -y

RUN pip install -r /code/requirements.txt

ENTRYPOINT ["/code/entrypoint.sh"]

CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000
