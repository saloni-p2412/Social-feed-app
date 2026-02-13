#!/bin/bash
# Start the Django backend (API). Keep this terminal open.
# In another terminal, run the frontend: cd frontend && npm run dev

cd "$(dirname "$0")/backend"

if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv venv
fi

echo "Installing dependencies..."
./venv/bin/pip install -q -r requirements.txt

echo "Running migrations..."
./venv/bin/python manage.py migrate

echo ""
echo "Starting backend at http://localhost:8000"
echo "API: http://localhost:8000/api/"
echo "Keep this terminal open. Use another terminal for the frontend."
echo ""
./venv/bin/python manage.py runserver
