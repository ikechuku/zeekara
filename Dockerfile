FROM python:3.7-alpine
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
# ENV DEBUG 0
RUN mkdir /api
WORKDIR /api
COPY requirements.txt /api/
RUN \
    python3 -m pip install -r requirements.txt 
COPY . /api/

RUN python manage.py collectstatic --noinput

RUN adduser -D myuser
USER myuser

CMD gunicorn zeekara.wsgi:application --bind 0.0.0.0:$PORT\