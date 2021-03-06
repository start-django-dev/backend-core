# syntax=docker/dockerfile:1
FROM python:3.8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir /src
WORKDIR /src

COPY requirements/ /src/requirements/
COPY requirements.txt /src
RUN pip install -r requirements.txt
COPY . /src/