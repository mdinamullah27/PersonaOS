# PersonaOS

**AI Digital Twin Platform - Enterprise Backend**

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Overview

PersonaOS is an enterprise AI Digital Twin platform designed to support:

- Local LLMs and AI agents
- RAG (Retrieval-Augmented Generation)
- Vector Databases
- Multi-Agent Systems
- Long-Term Memory
- Document Intelligence

This repository contains the **Phase 1 Backend Foundation** - a production-ready, scalable backend architecture built with Clean Architecture principles.

---

## Architecture

### Design Principles

- **Feature-Based Modular Monolith** architecture
- **Clean Architecture** with clear layer separation
- **Repository Pattern** for data access
- **Service Layer** for business logic
- **Dependency Injection** throughout
- **SOLID principles** adherence

### Folder Structure

```
backend/
├── app/
│   ├── core/           # Framework-level utilities
│   │   ├── config.py   # Pydantic Settings
│   │   ├── security.py # JWT + password hashing
│   │   ├── logging.py  # Structured logging
│   │   ├── exceptions.py
│   │   ├── responses.py
│   │   ├── constants.py
│   │   ├── dependencies.py
│   │   └── middleware.py
│   │
│   ├── db/             # Database layer
│   │   ├── engine.py   # Async SQLAlchemy engine
│   │   ├── session.py  # Session factory
│   │   ├── base.py     # Base model
│   │   ├── mixins.py   # UUID, Timestamps, SoftDelete
│   │   └── dependencies.py
│   │
│   ├── modules/        # Feature modules
│   │   ├── auth/       # Authentication & authorization
│   │   ├── users/      # User management
│   │   ├── workspace/  # Workspace management
│   │   ├── documents/  # Document handling
│   │   ├── chat/       # Chat functionality
│   │   ├── memory/     # Long-term memory
│   │   ├── persona/    # Persona management
│   │   ├── search/     # Search functionality
│   │   └── analytics/  # Analytics & metrics
│   │
│   ├── ai/             # AI subsystem (Phase 2+)
│   ├── integrations/   # External services
│   ├── workers/        # Background tasks
│   └── shared/         # Shared utilities
│
├── tests/              # Test suite
├── alembic/            # Database migrations
├── docker/             # Docker configuration
├── main.py             # Application entry point
├── pyproject.toml      # Dependencies & config
└── docker-compose.yml  # Docker services
```

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Framework | FastAPI 0.115+ |
| Python | 3.12+ |
| Validation | Pydantic v2 |
| Database | PostgreSQL (asyncpg) |
| ORM | SQLAlchemy 2.3 (async) |
| Migrations | Alembic |
| Cache | Redis |
| Auth | PyJWT + bcrypt |
| Logging | structlog |
| Testing | Pytest |
| Linting | Ruff, Black, Mypy |

---

## Development Setup

### Prerequisites

- Python 3.12+
- PostgreSQL 16+
- Redis 7+
- Docker & Docker Compose (recommended)

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd PersonaOS/backend

# Start all services
docker-compose up -d

# The API will be available at http://localhost:8000
# API docs at http://localhost:8000/docs (DEBUG mode)
```

### Option 2: Local Development

```bash
# Clone the repository
git clone <repository-url>
cd PersonaOS/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -e ".[dev]"

# Copy environment file
cp .env.example .env

# Update DATABASE_URL and REDIS_URL in .env if needed

# Run the application
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_NAME` | Application name | PersonaOS |
| `APP_VERSION` | Application version | 0.1.0 |
| `DEBUG` | Debug mode | false |
| `ENVIRONMENT` | Environment type | development |
| `SECRET_KEY` | JWT signing key | (change in production) |
| `JWT_EXPIRE_MINUTES` | JWT token expiry | 30 |
| `DATABASE_URL` | PostgreSQL connection | postgresql+asyncpg://personaos:personaos@localhost:5432/personaos |
| `REDIS_URL` | Redis connection | redis://localhost:6379/0 |
| `CORS_ORIGINS` | Allowed CORS origins | ["http://localhost:3000"] |
| `LOG_LEVEL` | Logging level | INFO |
| `LOG_FORMAT` | Log format (json/console) | console |

---

## API Endpoints

### Health Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/ready` | Readiness check (includes dependency checks) |
| GET | `/version` | Version information |

### Authentication (v1)

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/auth/login` | User login |
| POST | `/api/v1/auth/register` | User registration |
| POST | `/api/v1/auth/refresh` | Refresh access token |
| POST | `/api/v1/auth/logout` | User logout |
| GET | `/api/v1/auth/me` | Get current user |

### Users (v1)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/users/` | List users |
| GET | `/api/v1/users/me` | Get current user profile |
| GET | `/api/v1/users/{user_id}` | Get user by ID |
| PATCH | `/api/v1/users/me` | Update current user |

---

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test category
pytest -m unit
pytest -m integration

# Run specific test file
pytest tests/test_security.py
```

---

## Code Quality

```bash
# Linting
ruff check .

# Formatting
black .

# Type checking
mypy .

# Run all checks
pre-commit run --all-files
```

---

## Database Migrations

```bash
# Generate new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one step
alembic downgrade -1

# View migration history
alembic history
```

---

## Docker Services

| Service | Description | Port |
|---------|-------------|------|
| `postgres` | PostgreSQL database | 5432 |
| `redis` | Redis cache | 6379 |
| `backend` | FastAPI application | 8000 |

### Useful Commands

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Rebuild after changes
docker-compose up -d --build
```

---

## Future Roadmap

### Phase 2: Core Features
- [ ] Complete authentication flow
- [ ] Workspace management
- [ ] Document upload and processing
- [ ] Chat conversations
- [ ] User roles and permissions

### Phase 3: AI Infrastructure
- [ ] LLM provider integration
- [ ] RAG pipeline
- [ ] Vector database integration
- [ ] Embeddings service
- [ ] Memory system

### Phase 4: Advanced Features
- [ ] Multi-agent systems
- [ ] Advanced analytics
- [ ] Third-party integrations
- [ ] Background task processing
- [ ] Real-time websockets

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Support

For support, email support@personaos.dev or open an issue on GitHub.
