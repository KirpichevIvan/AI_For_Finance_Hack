FROM python:3.12-slim


# Создаём рабочую директорию
WORKDIR /app

# Копируем файлы
COPY . /app

# Установим зависимости
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt


# Установим NLTK данные
RUN python -m nltk.downloader punkt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
