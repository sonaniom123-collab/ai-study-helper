FROM python:3.11-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY . .
RUN python train/train_intent.py

ENV PORT=10000
EXPOSE 10000
CMD gunicorn --bind 0.0.0.0:${PORT} --workers 1 --timeout 120 app:app