# pull official base image
FROM python:3.8-slim-buster as builder

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

COPY requirements.txt /app/requirements.txt
WORKDIR app
RUN pip install --user -r requirements.txt
COPY . /app

FROM python:3.8-slim-buster AS build-image

COPY --from=builder /root/.local /root/.local
COPY --from=builder /app /app

WORKDIR /app
ENV PATH=/root/.local/bin:$PATH

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
