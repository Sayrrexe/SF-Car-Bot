FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Add labels for metadata
LABEL org.opencontainers.image.title="Aiogram Bot"
LABEL org.opencontainers.image.description="A Telegram bot built with Aiogram for managing car."
LABEL org.opencontainers.image.version="1.0"
LABEL org.opencontainers.image.maintainer="SF-hakaton <your.email@example.com>"
LABEL org.opencontainers.image.source="https://github.com/Sayrrexe/SF-Car-Bot"

RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install locales and set up en_US.UTF-8
RUN apt-get update && apt-get install -y locales && \
    echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen en_US.UTF-8 && \
    update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 && \
    dpkg-reconfigure --frontend=noninteractive locales

# Set environment variables for locale
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

RUN aerich init -t config.TORTOISE_ORM  
RUN aerich init-db

CMD ["python", "run.py"]
