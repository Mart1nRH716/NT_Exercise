FROM python:3.10
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && \
    apt-get install -y \
    default-libmysqlclient-dev \
    python3-dev \
    netcat-openbsd

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .