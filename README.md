# Backend and Distributed Systems

A hands-on engineering project focused on backend development, networking, Linux, databases, automated testing, and distributed systems. This repository documents my practical learning journey through building and improving **Taskflow**, a task-management API that will evolve into a distributed task-processing platform.

The goal is to develop strong foundations through implementation, testing, debugging, measurement, and progressively more advanced system design.

## Current Progress

**Completed through Day 5: Backend Foundations and Automated API Testing**

- HTTP fundamentals and client-server communication.
- A basic HTTP server implemented using Python sockets.
- REST API development using FastAPI.
- Request validation and response schemas using Pydantic.
- CRUD operations with PostgreSQL.
- SQL queries and database-backed task management.
- Query parameters for filtering, sorting, and pagination.
- HTTP status codes and error handling.
- Automated integration testing with pytest and FastAPI `TestClient`.
- Database persistence checks and dedicated test-database configuration.
- Test fixtures and test-data isolation.

**Latest test result:** 17 passed, 0 failed, 3 warnings.

The warnings are deprecation notices from dependencies and model declarations; they are maintenance items rather than test failures.

## Technology Stack

| Area | Technologies |
|---|---|
| Language | Python |
| API framework | FastAPI |
| Data validation | Pydantic |
| Database | PostgreSQL |
| Database access | SQLAlchemy |
| Testing | pytest, FastAPI `TestClient` |
| HTTP testing and debugging | curl |
| Development environment | Linux, WSL, Python virtual environment |
| Version control | Git and GitHub |

Additional technologies, including Redis, RabbitMQ, Docker, Nginx, Prometheus, Grafana, and load-testing tools, will be incorporated as the project develops.

## Project Goals

Taskflow is being developed incrementally toward a distributed task-processing architecture.

The planned system will eventually include:

- A REST API for submitting and managing tasks.
- PostgreSQL for persistent application data.
- Redis for caching, rate limiting, and selected coordination tasks.
- A message queue for asynchronous task processing.
- Background workers with retry handling and idempotent processing.
- Nginx as a reverse proxy and load balancer.
- Docker Compose for local multi-service deployment.
- Prometheus and Grafana for monitoring and observability.
- Automated tests, performance benchmarks, and failure analysis.

These are development goals, not claims that every component is already implemented.

## Getting Started

### Prerequisites

- Python 3
- Git
- Linux, WSL, or another compatible development environment
- PostgreSQL for the database-backed API

### 1. Clone the repository

```bash
git clone https://github.com/DHIRAJ-6-8-7/Backend-and-Distributed-system.git

cd Backend-and-Distributed-system
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv

source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip

python -m pip install -r requirements.txt
```

### 4. Configure the database

The database-backed application requires PostgreSQL and appropriate database credentials.

Configure the required environment variables using the names expected by the application:

- `DB_HOST`
- `DB_PORT`
- `DB_USER`
- `DB_NAME`
- `DB_PASSWORD`

For local development, store these values in a local `.env` file if the application is configured to load it.

**Security notes:**

- Never commit `.env` files or database credentials.
- Ensure `.env` is covered by `.gitignore`.
- Create and configure the development database before starting the database-backed API.
- Automated tests should use a dedicated test database rather than the development database.

The exact database initialization requirements depend on the SQL schema and setup scripts in the repository.

## Run the API

Activate the virtual environment and start the FastAPI application:

```bash
uvicorn app.main:app --reload
```

The API will normally be available at:

- Base URL: `http://127.0.0.1:8000`
- Interactive Swagger documentation: `http://127.0.0.1:8000/docs`
- ReDoc documentation: `http://127.0.0.1:8000/redoc`

The application requires its database configuration to be valid before database-backed endpoints can operate successfully.

## API Overview

The task API is organized under the `/api/v1/tasks` route.

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/v1/tasks` | Create a task |
| GET | `/api/v1/tasks` | Retrieve a task list |
| GET | `/api/v1/tasks/{task_id}` | Retrieve a task by ID |
| PATCH | `/api/v1/tasks/{task_id}` | Update selected task fields |
| PUT | `/api/v1/tasks/{task_id}` | Replace a task representation |
| DELETE | `/api/v1/tasks/{task_id}` | Delete a task |

The list endpoint supports the filtering, sorting, and pagination options implemented by the application.

Request validation is handled using Pydantic models, while the database layer uses SQLAlchemy to interact with PostgreSQL.

For the exact request schemas and query parameters, consult the interactive API documentation at `/docs`.

## Automated Testing

Automated tests are maintained in the `tests/` directory.

Run the complete test suite:

```bash
python -m pytest -v
```

Run the task API tests:

```bash
python -m pytest -v tests/test_tasks.py
```

Run the database configuration test:

```bash
python -m pytest -v tests/test_database_config.py
```

Run an individual test:

```bash
python -m pytest -v tests/test_tasks.py::test_create_task
```

### What the tests cover

- Successful task creation.
- Database persistence.
- Request validation failures.
- Missing required fields.
- Invalid age values.
- Retrieval by ID.
- Nonexistent resources and invalid IDs.
- Task listing and filtering.
- Sorting and pagination.
- Partial updates with PATCH.
- Replacement updates with PUT.
- Successful deletion and subsequent retrieval.
- Database configuration and test-data isolation.

### Test database safety

The test configuration selects `taskflow_test` and checks the connected database before performing destructive cleanup.

The fixture clears test task data before and after individual tests to help keep tests independent and repeatable.

Never remove the database-name safety check or run destructive test cleanup against a development or production database.

## Project Structure

The following is a conceptual overview of the main project areas. Individual filenames may evolve as the architecture develops.

```text
taskflow/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models/
│   ├── routers/
│   └── services/
├── tests/
│   ├── conftest.py
│   ├── test_database_config.py
│   └── test_tasks.py
├── test/
├── http_server.py
├── requirements.txt
├── .gitignore
└── README.md
```

The `app/` directory contains the API and database-related implementation. The `tests/` directory contains automated tests and their shared fixtures.

The older `test/` directory and other listed paths should be retained in this overview only if they exist in the current repository.

## Learning Roadmap

### Phase 1 — Backend Foundations

- [x] HTTP and client-server fundamentals
- [x] Basic HTTP server using Python sockets
- [x] FastAPI and REST API fundamentals
- [x] Pydantic validation and response schemas
- [x] CRUD operations
- [x] Filtering, sorting, and pagination
- [x] PostgreSQL integration
- [x] Database-backed API operations
- [x] Automated API integration tests with pytest
- [x] Test fixtures and test-database isolation
- [ ] Cumulative review and practical assessment

### Phase 2 — Database Engineering

- [ ] Database schema design and normalization
- [ ] Database migrations
- [ ] Transactions and isolation levels
- [ ] Indexes and query-plan analysis
- [ ] Connection pooling
- [ ] Database concurrency and consistency

### Phase 3 — Backend Reliability

- [ ] Redis caching and rate limiting
- [ ] Background task processing
- [ ] Message queues and asynchronous workers
- [ ] Retries, timeouts, and idempotency
- [ ] Structured logging and error observability

### Phase 4 — Deployment and Distributed Systems

- [ ] Docker and Docker Compose
- [ ] Nginx reverse proxy and load balancing
- [ ] Multiple API instances
- [ ] Prometheus and Grafana
- [ ] Load testing and performance analysis
- [ ] Replication and consistency
- [ ] Distributed coordination and failure handling
- [ ] System design and architecture documentation

The roadmap represents planned learning and implementation work. A checkbox is marked complete only when the corresponding work has been implemented or assessed.

## Engineering Principles

This project follows several principles:

1. **Understand before implementing:** study the purpose and trade-offs behind each component.
2. **Test behavior, not assumptions:** verify HTTP responses, data persistence, and error handling.
3. **Keep tests isolated:** avoid hidden dependencies between test cases.
4. **Protect data:** separate test databases from development and production environments.
5. **Measure before optimizing:** use benchmarks and query plans rather than guesswork.
6. **Build incrementally:** introduce architectural complexity when the project needs it.
7. **Document failures:** record bugs, their causes, and the reasoning behind fixes.

## Development Status

Taskflow is an actively evolving learning project. Its current foundation includes a FastAPI task API, PostgreSQL integration, CRUD operations, and automated tests.

The next stage focuses on cumulative review and strengthening the existing foundations before introducing more advanced backend and distributed-systems concepts.

---

**Author:** Dhiraj Shrestha  
**Institution:** IOE, Pulchowk Campus  
**Focus:** Backend Engineering, Systems Programming, and Distributed Systems
