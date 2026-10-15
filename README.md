# Backend and Distributeed System

A hands-on learning project focused on backend development, networking, Linux, databases, and distributed systems.

## Current Features

- HTTP fundamentals and a basic HTTP server implemented with Python sockets.
- FastAPI application for learning REST API development.
- Pydantic models for request validation and response schemas.
- CRUD operations and HTTP error handling.
- Query parameters for filtering, sorting, and pagination.
- Automated testing with pytest.

## Technology Stack

- **Language:** Python
- **API framework:** FastAPI
- **Validation:** Pydantic
- **Testing:** pytest
- **Tools:** curl, Git, Linux/WSL

## Setup

Run the following commands in your Linux terminal:

```bash
git clone https://github.com/DHIRAJ-6-8-7/Backend-and-Distributed-system.git
cd Backend-and-Distributed-system

python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run the API

```bash
uvicorn app.main:app --reload
```

Open the interactive API documentation in your browser:

http://127.0.0.1:8000/docs

## Run Tests

```bash
pytest -v
```

## Project Structure

```text
taskflow/
├── app/
│   ├── main.py
│   ├── models.py
│   ├── models/
│   └── routers/
├── test/
├── http_server.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Learning Roadmap

- [x] HTTP and client-server fundamentals
- [x] FastAPI and REST API fundamentals
- [x] Validation, error handling, filtering, sorting, and pagination
- [ ] PostgreSQL integration
- [ ] Database migrations and transactions
- [ ] Redis caching
- [ ] Background workers and message queues
- [ ] Docker Compose and reverse proxy
- [ ] Logging, metrics, and load testing
- [ ] Distributed systems fundamentals

This repository is a continuously evolving engineering project. Features will be added and tested incrementally as the learning roadmap progresses.
