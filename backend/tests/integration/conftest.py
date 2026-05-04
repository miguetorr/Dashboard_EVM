"""Fixtures compartidas para tests de integración."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import create_app

# SQLite en memoria para tests — no requiere PostgreSQL
SQLALCHEMY_TEST_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_TEST_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Habilitar soporte de FK en SQLite (desactivado por defecto)
@event.listens_for(engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


@pytest.fixture(autouse=True)
def setup_db():
    """Crea todas las tablas antes de cada test y las destruye después."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db():
    """Sesión de base de datos para tests."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db):
    """TestClient de FastAPI con la DB de prueba inyectada."""
    app = create_app()

    def _override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as c:
        yield c


@pytest.fixture
def sample_project(client):
    """Crea un proyecto de ejemplo y retorna su JSON de respuesta."""
    response = client.post(
        "/api/v1/projects",
        json={"name": "Proyecto Test", "description": "Descripción de prueba"},
    )
    assert response.status_code == 201
    return response.json()


@pytest.fixture
def sample_activity(client, sample_project):
    """Crea una actividad de ejemplo y retorna su JSON de respuesta."""
    project_id = sample_project["id"]
    response = client.post(
        f"/api/v1/projects/{project_id}/activities",
        json={
            "name": "Actividad Test",
            "bac": 10000,
            "planned_percentage": 60,
            "actual_percentage": 40,
            "actual_cost": 7000,
        },
    )
    assert response.status_code == 201
    return response.json()
