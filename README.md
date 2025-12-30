
# Log Analyzer REST API

Log Analyzer is a FastAPI-based backend application designed to ingest, store, and analyze structured log files.
The system reads log files from a directory, parses each log entry, stores the data in a relational database, and exposes REST APIs for querying and analysis.

---

## Problem Overview

Applications generate log files containing valuable operational data.
This project provides a REST API that:

- Reads log files from a given directory
- Parses structured log entries
- Stores logs in a database
- Allows querying logs with filters and pagination
- Provides aggregated statistics
- Ensures data consistency using database transactions

---

## Log File Format

Log files must be **tab-separated (\t)** and follow the format below:

2025-05-07 10:00:00	INFO	UserAuth	User 'john.doe' logged in successfully.
2025-05-07 10:00:15	WARNING	GeoIP	Could not resolve IP address '192.168.1.100'.
2025-05-07 10:00:20	ERROR	Payment	Transaction failed for user 'jane.doe'.
2025-05-07 10:00:25	INFO	UserAuth	User 'alice.smith' logged out.

---

## Features

- Ingest logs from a directory
- Skip already processed directories and files
- Parse timestamp, level, component, and message
- Store logs using a normalized database schema
- Use database transactions to avoid partial ingestion
- REST APIs to:
  - Fetch logs with filters and pagination
  - Fetch a specific log by ID
  - Fetch aggregated log statistics
- Database schema management using Alembic
- Clean, modular project structure

---

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
---

## Setup & Run Instructions

pipenv shell
pipenv install
alembic upgrade head
python main.py

---

## API Documentation

Swagger UI:
http://127.0.0.1:8000/docs

ReDoc:
http://127.0.0.1:8000/redoc

---

## Available APIs

POST /logs/ingest  
GET /logs  
GET /logs/{log_id}  
GET /logs/stats  
