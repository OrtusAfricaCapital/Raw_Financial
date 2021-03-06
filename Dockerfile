FROM python:3.9
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code

COPY requirements.txt /
RUN pip install -r /requirements.txt
COPY . /code

RUN python manage.py migrate
EXPOSE 8000

