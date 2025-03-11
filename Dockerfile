FROM python:3.10


RUN apt-get update && apt-get install -y \
    poppler-utils \
    tesseract-ocr \
    tesseract-ocr-eng \
    zbar-tools && \
    rm -rf /var/lib/apt/lists/*


ENV TESSERACT_CMD=/usr/bin/tesseract


WORKDIR /app


COPY requirements.txt .
COPY files files/
COPY pdf_parser.py .
COPY test_pdf_validate.py .


RUN pip install --no-cache-dir -r requirements.txt


RUN ls -l /app


CMD ["pytest", "-sv"]
