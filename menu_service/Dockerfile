# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apt-get update
RUN apt-get -y install gettext
WORKDIR /code
COPY requirements.txt /code/
COPY django-micro-auth-1.0.tar.gz /code/
RUN pip install -r requirements.txt
RUN pip install django-micro-auth-1.0.tar.gz  
COPY . /code/
