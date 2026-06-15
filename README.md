# Hostage Game

A real-time multiplayer location-based game built with Flask, Leaflet, and PostgreSQL.

## Features
- Join or create game lobbies with a code
- Role selection: Hostage / Searcher
- Real-time player location tracking on a map
- Team-based gameplay system

## Tech Stack
- Flask (Python backend)
- Flask-SQLAlchemy
- PostgreSQL (RDS database)
- Leaflet.js (interactive maps)
- JavaScript (frontend updates)

## Run Locally
pip install -r requirements.txt
python app.py

## Notes
- Uses session-based player tracking
- Map updates every few seconds using fetch requests