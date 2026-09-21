"""Shared pytest fixtures.

Environment variables are set before importing the app so ``database.py``
picks up an isolated SQLite file instead of the developer's ``groups.db``.
"""

import os
import tempfile

os.environ["ENVIRONMENT"] = "DEV"
os.environ.setdefault("SECRET_KEY", "test-secret")
os.environ.setdefault("ADMIN_PASSWORD", "test-password")
os.environ.setdefault("LOG_LEVEL", "WARNING")

with tempfile.NamedTemporaryFile(prefix="open-groups-test-", suffix=".db", delete=False) as handle:
    db_path = handle.name
os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"

import pytest
from fastapi.testclient import TestClient

import main
from database import Base, _sync_engine


@pytest.fixture(autouse=True)
def _reset_state():
    """Fresh schema and cleared lockouts for every test."""
    Base.metadata.drop_all(_sync_engine)
    Base.metadata.create_all(_sync_engine)
    main.lockout_data.clear()
    yield
    Base.metadata.drop_all(_sync_engine)


@pytest.fixture()
def client():
    with TestClient(main.app) as test_client:
        yield test_client


@pytest.fixture()
def auth(client):
    response = client.post("/api/admin/login", json={"password": "test-password"})
    assert response.status_code == 200, response.text
    return {"Authorization": f"Bearer {response.json()['token']}"}
