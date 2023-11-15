FROM python:3.10.6-alpine
RUN apk update && apk add gcc python3-dev musl-dev libffi-dev

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk add --no-cache jpeg-dev zlib-dev
RUN apk add --no-cache --virtual .build-deps build-base linux-headers

WORKDIR /code
COPY ./some_package/requirements.txt /code/some_package/requirements.txt
RUN pip3 install -r /code/some_package/requirements.txt
COPY . /code/

EXPOSE 22