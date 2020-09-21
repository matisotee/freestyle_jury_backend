# pull official base image
FROM python:3.8-slim-buster as builder

COPY . /app

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
&& apt-get install gcc -y \
&& apt-get install libpq-dev -y \
&& apt-get install build-essential -y \
&& apt-get install libssl-dev -y \
&& apt-get install libffi-dev -y \
&& apt-get install libxml2-dev -y \
&& apt-get install libxslt1-dev -y \
&& apt-get install zlib1g-dev -y \
&& apt-get clean

RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

FROM python:3.8-slim-buster AS build-image

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
&& apt-get install libpq-dev -y \
&& apt-get clean

COPY --from=builder /app /app

RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
