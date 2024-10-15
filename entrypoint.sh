#!/bin/bash

# Wait for database to be ready (optional, depending on your setup)
echo "Waiting for the database to be ready..."
while ! nc -z db 5432; do
  sleep 1
done
echo "Database is ready."

# Run migrations
echo "Running migrations..."
aerich init -t config.TORTOISE_ORM
aerich migrate

# Start the bot
echo "Starting the bot..."
exec python run.py
