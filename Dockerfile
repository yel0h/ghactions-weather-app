FROM python:3.14-alpine AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.14-alpine

WORKDIR /app

LABEL org.opencontainers.image.authors="Michał Choina"
LABEL org.opencontainers.image.description="Aplikacja pogodowa Flask"
LABEL org.opencontainers.image.version="1.0"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN adduser -D appuser

COPY --from=builder /install /usr/local

COPY app.py .
COPY templates ./templates

RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 5000

HEALTHCHECK --timeout=5s --start-period=10s \
  CMD wget -qO- http://localhost:5000 || exit 1

CMD ["python", "app.py"]