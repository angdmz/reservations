FROM python:3.6.7-alpine
RUN apk add --no-cache git \
    build-base \
    postgresql \
    postgresql-dev \
    libpq
RUN mkdir -p /opt/project
WORKDIR /opt/project
ADD . /opt/project
RUN mkdir logs/
ENV PYTHONUNBUFFERED 1
RUN pip install -U pip
RUN pip install -r requirements.txt
RUN cp recommendations/local_settings_docker.py recommendations/local_settings.py

