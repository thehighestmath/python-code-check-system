FROM python:3.11.3-slim

WORKDIR /umschool

COPY . .

RUN pip install -r requirements.txt

RUN python manage.py migrate
