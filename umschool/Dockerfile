FROM python:3.12.3-slim

WORKDIR /umschool

COPY . .

RUN apt-get update -y && apt-get install -y gcc
RUN pip install -r requirements.txt

RUN chmod +x entrypoint.sh
