FROM ubuntu:18.04

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

# install psycopg2
RUN apt-get update \
    && apt-get install gcc g++ python3-dev musl-dev -y

# install dependencies
COPY ./requirements.txt .
RUN apt-get install python3-pip -y
RUN pip3 install -r requirements.txt

# copy project
COPY . .
RUN python3 manage.py collectstatic --noinput
# add and run as non-root user

# run gunicorn
CMD gunicorn myproject.wsgi:application --bind 0.0.0.0:$PORT
