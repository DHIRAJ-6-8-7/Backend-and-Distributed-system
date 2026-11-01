# Taskflow — Backend & Distributed Systems

**A hands-on backend engineering project evolving into a distributed task-processing platform.**

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/PostgreSQL-Database-4169E1?logo=postgresql" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Redis-Cache-DC382D?logo=redis" alt="Redis">
  <img src="https://img.shields.io/badge/RabbitMQ-Message Broker-FF6600?logo=rabbitmq" alt="RabbitMQ">
  <img src="https://img.shields.io/badge/SQLAlchemy-ORM-D71F00" alt="SQLAlchemy">
  <img src="https://img.shields.io/badge/Alembic-Migrations-6BA81E" alt="Alembic">
</p>

---

## 1. Project Overview

**Taskflow** is a backend engineering project built to explore the principles, technologies, and engineering practices behind modern backend and distributed systems.

It began as a PostgreSQL-backed task management API and is progressively evolving into an asynchronous task-processing platform.

The project is developed through practical implementation, testing, debugging, failure analysis, and performance investigation rather than relying exclusively on theoretical exercises.

### Primary objectives

- Build maintainable REST APIs using FastAPI.
- Understand HTTP, networking, and client-server communication.
- Design and interact with relational databases.
- Implement database access using SQLAlchemy ORM.
- Manage database schema changes using Alembic.
- Improve application performance using Redis caching.
- Introduce asynchronous processing using message queues.
- Build background workers and understand message-delivery behaviour.
- Explore Linux, processes, networking, and system-level behaviour.
- Deploy and observe multi-service applications.
- Understand distributed-system trade-offs, failures, and consistency.

## 2. Current Development Status

<details>
<summary><strong>Completed work — Days 1–12</strong></summary>

### Backend and HTTP foundations

- HTTP fundamentals and client-server communication.
- Basic HTTP server implemented using Python sockets.
- REST API development using FastAPI.
- Request validation and response schemas using Pydantic.
- CRUD operations and HTTP status codes.
- Filtering, sorting, and pagination.
- Error handling and API testing.

### PostgreSQL and database engineering

- PostgreSQL integration.
- SQL queries and relational database fundamentals.
- SQLAlchemy Core and ORM.
- Declarative ORM models.
- Session management and dependency injection.
- Database connection pooling fundamentals.
- Alembic migration workflow.
- Schema upgrades and downgrades.

### Automated testing

- pytest and FastAPI `TestClient`.
- Integration testing of API endpoints.
- Database persistence verification.
- Test fixtures and test database isolation.

### Redis integration

- Redis architecture and client-server communication.
- Keys, expiration, TTL, and data structures.
- Redis CLI and persistence mechanisms.
- Python integration using `redis-py`.
- Cache-aside implementation.
- GET-by-ID caching with a 300-second TTL.
- Cache invalidation after PATCH, PUT, and DELETE.
- Redis failure handling and PostgreSQL fallback.
- Redis outage and recovery verification.

### RabbitMQ and asynchronous processing

- RabbitMQ installation and service verification.
- Python integration using Pika.
- RabbitMQ connection and channel management.
- Queue declaration and message publishing.
- Durable queue configuration.
- Persistent message properties.
- Publisher confirmation and mandatory publishing.
- JSON message payloads.
- Background consumer and worker implementation.
- Manual message acknowledgement.
- Task status tracking in PostgreSQL.
- Database-backed task claiming.
- API integration with asynchronous message publishing.
- Successful end-to-end task processing verification.

</details>

**Current milestone:** RabbitMQ integration and basic asynchronous task processing completed (Day 12).

The project is now entering the operating-systems and concurrency stage.

> Development status reflects work implemented and verified. Planned architecture components are not presented as completed features.

## 3. Architecture

### Current application architecture

The current system combines synchronous API operations, PostgreSQL persistence, Redis caching, and RabbitMQ-based asynchronous processing.

```text
                         Client
                           |
                           v
                    FastAPI Application
                           |
             +-------------+-------------+
             |             |             |
             v             v             v
        PostgreSQL       Redis        RabbitMQ
        Task Data        Cache        Task Queue
             |                           |
             |                           v
             |                    Background Worker
             |                           |
             +---------------------------+
                         |
                         v
                  Task Status Update
```

### Asynchronous task-processing flow

When a client submits a task:

1. FastAPI validates the request.
2. The task is inserted into PostgreSQL.
3. The API publishes a message containing the task ID to RabbitMQ.
4. RabbitMQ delivers the message to a consumer.
5. The worker retrieves and processes the task.
6. The worker updates the task status in PostgreSQL.

```text
Client
  |
  | POST /api/v1/tasks
  v
FastAPI
  |
  | 1. Insert task
  v
PostgreSQL
  |
  | 2. Publish task_id
  v
RabbitMQ Queue
  |
  | 3. Deliver message
  v
Consumer / Worker
  |
  | 4. Process task
  v
PostgreSQL
  |
  | 5. Update status
  v
Completed
```

### Target distributed architecture

The long-term architecture is planned to evolve toward:

```text
                         Clients
                            |
                            v
                       Nginx / Proxy
                            |
                 +----------+----------+
                 |          |          |
                 v          v          v
              FastAPI    FastAPI    FastAPI
              Instance   Instance   Instance
                 |          |          |
                 +----------+----------+
                            |
              +-------------+-------------+
              |             |             |
              v             v             v
            Redis       PostgreSQL     RabbitMQ
            Cache       Persistent     Message
                        Database       Broker
                                           |
                                      +----+----+
                                      |         |
                                      v         v
                                   Worker 1  Worker 2
                                      |         |
                                      +----+----+
                                           |
                                           v
                                    Task Processing
                                           |
                                           v
                                     Results / Status

                         Observability:
                        Prometheus + Grafana
```

This is the target architecture, not a claim that every component is already implemented.

## 4. Technology Stack

| Category | Technology | Purpose |
|---|---|---|
| Language | Python | Application development |
| API framework | FastAPI | REST API implementation |
| Validation | Pydantic | Request and response validation |
| Primary database | PostgreSQL | Persistent relational data |
| Database toolkit | SQLAlchemy | SQL execution and ORM |
| Migrations | Alembic | Database schema versioning |
| Cache | Redis | In-memory caching |
| Redis client | redis-py | Python–Redis communication |
| Message broker | RabbitMQ | Asynchronous message delivery |
| RabbitMQ client | Pika | Python–RabbitMQ communication |
| Testing | pytest | Automated testing |
| API testing | FastAPI TestClient, curl | Endpoint verification |
| ASGI server | Uvicorn | Application server |
| Environment | Linux / WSL | Development environment |
| Version control | Git / GitHub | Source control |

### Planned technologies

| Technology | Planned purpose |
|---|---|
| Docker | Application containerization |
| Docker Compose | Multi-service development environment |
| Nginx | Reverse proxy and load balancing |
| Prometheus | Metrics collection |
| Grafana | Monitoring and visualization |
| k6 | Load and performance testing |

## 5. Project Structure

```text
taskflow/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── redis_client.py
│   ├── rabbitmq_client.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── task.py
│   │   └── task_model.py
│   │
│   ├── routers/
│   │
│   └── services/
│       ├── __init__.py
│       ├── cache_service.py
│       ├── message_service.py
│       └── task_service.py
│
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── tests/
│   ├── conftest.py
│   ├── test_database_config.py
│   └── test_tasks.py
│
├── alembic.ini
├── consumer.py
├── producer.py
├── http_server.py
├── test_claim_task.py
├── test_rabbitmq_connection.py
├── requirements.txt
├── .env                 # Local configuration; not committed
├── .gitignore
└── README.md
```

The structure may evolve as the application grows. Dedicated worker and router modules may be introduced as their responsibilities expand.

## 6. Getting Started

### Prerequisites

- Python 3
- Git
- PostgreSQL
- Redis
- RabbitMQ
- Linux, WSL, or another compatible development environment

### 6.1 Clone the repository

```bash
git clone https://github.com/DHIRAJ-6-8-7/Backend-and-Distributed-system.git

cd Backend-and-Distributed-system
```

### 6.2 Create a virtual environment

```bash
python3 -m venv .venv

source .venv/bin/activate
```

### 6.3 Install dependencies

```bash
python -m pip install --upgrade pip

python -m pip install -r requirements.txt
```

### 6.4 Configure environment variables

Create a local `.env` file in the project root.

Example:

```env
DB_HOST=localhost
DB_PORT=5432
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_NAME=taskflow

REDIS_URL=redis://localhost:6379/0

RABBITMQ_URL=amqp://guest:guest@localhost:5672/%2F
```

Use your own local credentials. The RabbitMQ URL above is an example for a local development setup.

**Security requirements:**

- Never commit `.env`.
- Never publish database credentials or secrets.
- Ensure `.env` is listed in `.gitignore`.
- Use a separate database for automated tests.
- Do not expose Redis, PostgreSQL, or RabbitMQ publicly without appropriate security configuration.
- Change default credentials when configuring services beyond local development.

### 6.5 Start the services

Start PostgreSQL, Redis, and RabbitMQ using your local service manager.

For Ubuntu / WSL:

```bash
sudo service postgresql start
sudo service redis-server start
sudo service rabbitmq-server start
```

Verify Redis:

```bash
redis-cli ping
```

Expected response:

```text
PONG
```

Verify RabbitMQ:

```bash
sudo rabbitmq-diagnostics ping
```

A successful response confirms that the RabbitMQ node is running and responding to the diagnostic ping.

Verify PostgreSQL connectivity using your configured database credentials.

### 6.6 Database migrations

The project uses Alembic to manage schema changes.

Inspect migration history:

```bash
alembic history
```

Check the current database revision:

```bash
alembic current
```

Apply available migrations:

```bash
alembic upgrade head
```

Create a migration after changing ORM models:

```bash
alembic revision --autogenerate -m "describe schema change"
```

Review generated migration files before applying them.

**Important:** The existing baseline migration was stamped against an already-created database during development. A fresh database may require a proper initial schema migration or bootstrap procedure before it can use the current migration history. Do not assume that the existing migration history alone creates every original table from scratch.

## 7. Running the Application

Activate the virtual environment and start the API:

```bash
uvicorn app.main:app --reload
```

Default local URLs:

| Resource | URL |
|---|---|
| API base | http://127.0.0.1:8000 |
| Swagger UI | http://127.0.0.1:8000/docs |
| ReDoc | http://127.0.0.1:8000/redoc |

The application requires valid database configuration. Redis is used for caching, with the current GET cache path designed to fall back to PostgreSQL when Redis is unavailable.

RabbitMQ must be available when creating tasks through the current asynchronous publishing flow.

### Running the worker

Open another terminal, activate the same virtual environment, and run:

```bash
python consumer.py
```

The consumer listens for messages from the task queue and processes received tasks.

Keep the worker running while testing asynchronous task creation.

## 8. API Reference

The task API is organized under:

```text
/api/v1/tasks
```

### Available endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/tasks` | Create and queue a task |
| GET | `/api/v1/tasks` | Retrieve tasks |
| GET | `/api/v1/tasks/{task_id}` | Retrieve a task by ID |
| PATCH | `/api/v1/tasks/{task_id}` | Partially update a task |
| PUT | `/api/v1/tasks/{task_id}` | Replace a task |
| DELETE | `/api/v1/tasks/{task_id}` | Delete a task |

The list endpoint supports the implemented filtering, sorting, and pagination options.

Request validation and response serialization are handled through Pydantic models.

For exact request fields, query parameters, and response schemas, use the interactive Swagger documentation at `/docs`.

### Asynchronous task creation

The POST endpoint currently creates a database record and publishes a message to RabbitMQ.

A successful request returns:

```http
202 Accepted
```

Example request:

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn distributed systems",
    "completed": false,
    "age": 21
  }'
```

Example response:

```json
{
  "id": 13,
  "title": "Learn distributed systems",
  "completed": false,
  "age": 21
}
```

The task ID is used in the RabbitMQ message so that the worker can retrieve and process the corresponding task.

**Important reliability limitation:** The current implementation commits the task to PostgreSQL before publishing the RabbitMQ message. If publishing fails after the database commit, the task can remain in PostgreSQL without being queued. The Transactional Outbox Pattern is a planned improvement, not yet implemented.

### Other example requests

Retrieve a task:

```bash
curl "http://127.0.0.1:8000/api/v1/tasks/1"
```

Partially update a task:

```bash
curl -X PATCH "http://127.0.0.1:8000/api/v1/tasks/1" \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

Delete a task:

```bash
curl -X DELETE "http://127.0.0.1:8000/api/v1/tasks/1"
```

The example task ID must exist for operations that require an existing task.

## 9. Database Engineering

### PostgreSQL

PostgreSQL serves as the primary persistent data store.

The current application uses SQLAlchemy ORM for database operations.

Key concepts explored:

- Relational database design.
- SQL queries.
- Declarative ORM models.
- Session lifecycle.
- Database dependency injection.
- Connection pooling.
- Database transactions.
- Schema migration workflows.
- Task status persistence.
- Database-backed task claiming.

### SQLAlchemy

The application separates ORM models from Pydantic request and response schemas.

This distinction helps keep database representation separate from API contracts.

### Alembic

Alembic manages schema changes over time.

Typical workflow:

```text
Modify ORM Model
       |
       v
Generate Migration
       |
       v
Review Migration
       |
       v
Apply Migration
       |
       v
Verify Database Schema
```

Useful commands:

```bash
alembic current
alembic history
alembic heads
alembic revision --autogenerate -m "description"
alembic upgrade head
alembic downgrade -1
alembic check
```

Generated migrations should always be reviewed before execution.

## 10. Redis Caching

Redis is integrated as a caching layer alongside PostgreSQL.

### Cache-aside strategy

The current GET-by-ID endpoint follows this flow:

1. Check Redis for the requested task.
2. If a cached value exists, return it.
3. Otherwise, retrieve the task from PostgreSQL.
4. Serialize the task response.
5. Store the result in Redis with a 300-second TTL.
6. Return the result.

### Cache invalidation

After successful database mutations:

- PATCH invalidates the corresponding task key.
- PUT invalidates the corresponding task key.
- DELETE invalidates the corresponding task key.
- POST creates a new task and does not normally require invalidating an existing detail key.

Example key:

```text
task:42
```

### Failure handling

The cache-read path handles Redis errors and falls back to PostgreSQL.

This keeps basic task retrieval available when Redis is temporarily unavailable, provided PostgreSQL remains healthy.

The current implementation is an educational cache-aside foundation. More advanced consistency, observability, and coordination mechanisms will be developed later.

## 11. RabbitMQ and Asynchronous Processing

RabbitMQ is integrated as the message broker for asynchronous task processing.

### Current message flow

```text
FastAPI
   |
   | Publish JSON message
   v
RabbitMQ
   |
   | Deliver message
   v
Consumer
   |
   | Retrieve and claim task
   v
PostgreSQL
   |
   | Process task and update status
   v
Completed
```

### Current implementation

- RabbitMQ connection and channel creation using Pika.
- Queue declaration using a durable queue.
- JSON message containing the task ID.
- Persistent message delivery properties.
- Publisher confirmation.
- Mandatory publishing.
- Consumer-side manual acknowledgement.
- Database-backed task claiming.
- Task status updates during processing.
- Separate worker process from the FastAPI application.

### Message acknowledgement

The consumer uses acknowledgements to tell RabbitMQ whether a message has been processed.

Manual acknowledgement helps prevent a message from being considered successfully processed before the consumer finishes its work.

If a consumer exits before acknowledging a delivered message, RabbitMQ can requeue the unacknowledged message.

### Current reliability limitations

The current implementation is a learning foundation, not a complete production-grade message-processing system.

The following improvements remain planned:

- Retry policies and backoff.
- Dead-letter exchanges and dead-letter queues.
- Recovery of tasks stuck in a processing state.
- More comprehensive idempotency and duplicate-delivery handling.
- Transactional Outbox Pattern to address the database/message dual-write problem.
- Structured logging and message-processing metrics.
- More comprehensive broker and worker failure testing.

A publisher confirmation indicates that RabbitMQ accepted responsibility for the published message. It does not make the PostgreSQL transaction and message publication atomic.

## 12. Automated Testing

The project uses pytest and FastAPI `TestClient`.

Run the complete test suite:

```bash
python -m pytest -v
```

Run task API tests:

```bash
python -m pytest -v tests/test_tasks.py
```

Run database configuration tests:

```bash
python -m pytest -v tests/test_database_config.py
```

Run an individual test:

```bash
python -m pytest -v tests/test_tasks.py::test_create_task
```

### RabbitMQ verification

Run the connection test:

```bash
python test_rabbitmq_connection.py
```

Run the task-claim test:

```bash
python test_claim_task.py
```

### Testing principles

- Verify HTTP status codes and response bodies.
- Verify database persistence.
- Test invalid and missing input.
- Test nonexistent resources.
- Verify filtering, sorting, and pagination.
- Verify partial and full updates.
- Verify deletion behaviour.
- Test message publishing and consumption.
- Verify task status transitions.
- Test duplicate task-claim behaviour.
- Keep test data isolated.
- Use a dedicated test database.
- Avoid destructive test operations against development or production databases.

### Redis verification

```bash
redis-cli ping
redis-cli GET task:1
redis-cli TTL task:1
```

Test Redis outage behaviour in a controlled local environment by temporarily stopping Redis and verifying that the GET endpoint can retrieve data from PostgreSQL.

### RabbitMQ verification

```bash
sudo rabbitmq-diagnostics ping
```

Test asynchronous processing by:

1. Starting PostgreSQL, Redis, and RabbitMQ.
2. Starting the FastAPI application.
3. Starting the consumer in another terminal.
4. Creating a task through Swagger or curl.
5. Checking the worker output.
6. Verifying the updated task status in PostgreSQL.

## 13. Development Roadmap

The project follows a progressive learning and implementation roadmap.

### Phase 1 — Backend Foundations

- [x] HTTP fundamentals
- [x] Python socket-based HTTP server
- [x] FastAPI and REST API design
- [x] Pydantic validation
- [x] CRUD operations
- [x] PostgreSQL integration
- [x] Filtering, sorting, and pagination
- [x] Automated API testing

### Phase 2 — Database Engineering and Caching

- [x] SQL and relational database fundamentals
- [x] SQLAlchemy ORM
- [x] Session management and dependency injection
- [x] Database connection pooling fundamentals
- [x] Alembic migration workflow
- [x] Redis fundamentals
- [x] Python Redis integration
- [x] Cache-aside implementation
- [x] Cache invalidation
- [x] Redis outage fallback verification
- [ ] Advanced transaction and isolation analysis
- [ ] Indexing and query-plan optimisation
- [ ] Cache metrics and observability

### Phase 3 — Asynchronous Processing

- [x] RabbitMQ architecture fundamentals
- [x] Message producers and consumers
- [x] Queue declaration and publishing
- [x] Publisher confirmations
- [x] Persistent messages and durable queues
- [x] Manual acknowledgements
- [x] Background worker integration
- [x] Basic task claiming and status updates
- [x] End-to-end asynchronous task processing
- [ ] Retry policies and backoff
- [ ] Dead-letter queues
- [ ] Stuck-task recovery
- [ ] Stronger idempotent processing
- [ ] Transactional Outbox Pattern
- [ ] Comprehensive failure handling and recovery

### Phase 4 — Operating Systems and Networking

- [ ] Linux processes and threads
- [ ] Signals and system calls
- [ ] File descriptors
- [ ] Sockets and network communication
- [ ] Inter-process communication
- [ ] Memory management
- [ ] Linux namespaces and cgroups
- [ ] Practical system-level debugging

### Phase 5 — Containerization and Deployment

- [ ] Docker fundamentals
- [ ] Dockerfiles and image building
- [ ] Docker Compose
- [ ] Multi-service deployment
- [ ] Nginx reverse proxy
- [ ] Load balancing
- [ ] Multiple API instances
- [ ] Service configuration and networking

### Phase 6 — Distributed Systems and Observability

- [ ] Prometheus metrics
- [ ] Grafana dashboards
- [ ] Structured logging
- [ ] Distributed tracing fundamentals
- [ ] Load testing with k6
- [ ] Performance benchmarking
- [ ] Replication and consistency
- [ ] Distributed coordination
- [ ] CAP theorem and consensus fundamentals
- [ ] Failure analysis and recovery
- [ ] Final architecture integration

A roadmap checkbox is marked complete only when the corresponding work has been implemented, tested, or assessed.

## 14. Engineering Principles

This project follows these engineering principles:

1. **Understand before implementing:** Learn the purpose, trade-offs, and limitations of each component.
2. **Build incrementally:** Introduce complexity only when the system needs it.
3. **Test behaviour:** Verify actual application behaviour instead of relying on assumptions.
4. **Protect data:** Separate test, development, and production environments.
5. **Measure before optimising:** Use query plans, benchmarks, and metrics.
6. **Design for failure:** Consider unavailable dependencies, timeouts, and partial failures.
7. **Maintain clear boundaries:** Separate API schemas, database models, and service responsibilities.
8. **Document decisions:** Record important design choices, debugging results, and lessons learned.
9. **Avoid premature complexity:** Prefer a simple working implementation before introducing distributed architecture.

## 15. Project Scope and Disclaimer

Taskflow is an actively evolving engineering and learning project.

Its purpose is to demonstrate practical understanding of backend development, databases, caching, message queues, networking, operating systems, and distributed-system concepts.

The project is not presented as a production-ready distributed platform. Planned components will be introduced, implemented, and verified progressively.

## 16. Author

**Dhiraj Shrestha**  
B.E. Computer Engineering  
IOE, Pulchowk Campus

**Focus areas:** Backend Engineering · Systems Programming · Distributed Systems

---

<p align="center">
  <sub>Built incrementally. Tested carefully. Designed to understand how real systems work.</sub>
</p>
