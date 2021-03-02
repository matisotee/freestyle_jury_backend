# pull official base image
FROM python:3.8-slim-buster as builder

COPY requirements.txt ./

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

RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.8-slim-buster AS build-image

COPY --from=builder /usr/local/lib/python3.8/site-packages/ /usr/local/lib/python3.8/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /code:$PYTHONPATH

RUN apt-get update \
&& apt-get install libpq-dev -y \
&& apt-get clean

RUN echo "deb [trusted=yes] https://apt.secrethub.io stable main" > /etc/apt/sources.list.d/secrethub.sources.list && apt-get update
RUN apt-get install -y secrethub-cli

COPY . /app/

RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
