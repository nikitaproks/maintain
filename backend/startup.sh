#!/bin/bash
set -e
# Let the DB start
poetry run python app/pre_start.py

# Run migrations
poetry run alembic upgrade head

# Create initial data in DB
poetry run python app/initial_data.py


#Start app
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload