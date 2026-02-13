#!/usr/bin/env bash
# Quick setup script for local development

set -o errexit

echo "Setting up Django backend..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Install dependencies
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file. Please update it with your settings."
fi

# Run migrations
python manage.py migrate

echo "Backend setup complete!"
echo "Run 'python manage.py runserver' to start the development server."
