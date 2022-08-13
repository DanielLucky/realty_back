# Указывает Docker использовать официальный образ python 3 с dockerhub в качестве базового образа
FROM python:3.9.13
# Устанавливает переменную окружения, которая гарантирует, что вывод из python будет отправлен прямо в терминал без предварительной буферизации
ENV PYTHONUNBUFFERED 1
# Устанавливает рабочий каталог контейнера — "app"
WORKDIR /app
# Копирует pyproject.toml из нашего локального проекта в контейнер
COPY ["poetry.lock", "pyproject.toml", "./"]
# Обновление pip
RUN pip install --upgrade pip
# установка poetry
RUN pip install poetry
# установка зависимостей
RUN poetry lock --no-update; poetry export --without-hashes -f requirements.txt > requirements.txt
# Запускает команду pip install для всех библиотек, перечисленных в requirements.txt
RUN pip install -r requirements.txt