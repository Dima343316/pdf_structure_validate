# Используем Python 3.10 в качестве базового образа
FROM python:3.10

# Устанавливаем зависимости для работы с PDF и OCR
RUN apt-get update && apt-get install -y \
    poppler-utils \
    tesseract-ocr \
    tesseract-ocr-eng \
    zbar-tools && \
    rm -rf /var/lib/apt/lists/*

# Устанавливаем переменную окружения для Tesseract
ENV TESSERACT_CMD=/usr/bin/tesseract

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY requirements.txt .
COPY files files/
COPY pdf_parser.py .
COPY test_pdf_validate.py .

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Просмотр содержимого директории /app
RUN ls -l /app

# Запуск тестов при старте контейнера
CMD ["pytest", "-sv"]
