# установка базового образа (host OS)
FROM cr-sk-prod.otr.ru:5005/registry/docker-images/python:3.8-slim-buster
ENV TZ Europe/Moscow
# установка рабочей директории в контейнере
WORKDIR /code
# копирование файла зависимостей в рабочую директорию
COPY requirements.txt .
# установка зависимостей
RUN pip install -r requirements.txt
# копирование содержимого локальной директории src в рабочую директорию
COPY src/ .
