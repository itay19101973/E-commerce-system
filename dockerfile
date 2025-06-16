FROM python:3.12

RUN mkdir -p /app

WORKDIR /app

COPY ./requirements.txt ./requirements.txt


RUN pip install --no-cache-dir --upgrade -r ./requirements.txt
