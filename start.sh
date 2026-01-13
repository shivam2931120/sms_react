#!/bin/bash

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo "Running database migrations..."
if [ ! -d "migrations" ]; then
    flask db init
    flask db migrate -m "Initial migration"
fi
flask db upgrade

# Run application
echo "Starting Flask Server..."
python run.py
