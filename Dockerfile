FROM python:3.10

ENV PYTHONUNBUFFERED=1

# https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#sort-multi-line-arguments
RUN apt update && \
    apt install -y python3-gdal && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/

CMD python manage.py runserver 0.0.0.0:8000
