"""Tests for FastAPI API endpoints using TestClient.

Heavy ML modules are mocked before any project import so tests run fast.
"""
import sys
from unittest.mock import MagicMock

# Mock heavy ML modules before any project import touches them
for mod_name in [
    "clip", "sentence_transformers", "torch", "torchvision",
    "torchvision.transforms", "torchvision.models",
]:
    if mod_name not in sys.modules:
        sys.modules[mod_name] = MagicMock()

import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient

from api.main import app
from api.dependencies import get_search_engine
from api.security.jwt_handler import create_access_token
from api.security.token_blacklist import blacklist


# Override the search engine dependency with a mock for all tests
_mock_search_engine = MagicMock()
_mock_search_engine.text_to_image_search.return_value = [
    {"filename": "shoe1.jpg", "similarity_score": 0.9}
]
_mock_search_engine.image_to_image_search.return_value = []
_mock_search_engine.hybrid_search.return_value = []
_mock_search_engine.get_search_stats.return_value = {"total_searches": 0}
_mock_search_engine.vector_db.get_stats.return_value = {"total_vectors": 0}


def _override_search_engine():
    return _mock_search_engine


app.dependency_overrides[get_search_engine] = _override_search_engine


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def auth_headers():
    token = create_access_token({"sub": "admin", "roles": ["admin", "user"]})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def auth_token():
    return create_access_token({"sub": "admin", "roles": ["admin", "user"]})


@pytest.fixture
def user_headers():
    token = create_access_token({"sub": "demo", "roles": ["user"]})
    return {"Authorization": f"Bearer {token}"}


# ---------------------------------------------------------------------------
# Health endpoint (public)
# ---------------------------------------------------------------------------
class TestHealthEndpoint:
    def test_health_returns_200(self, client):
        resp = client.get("/api/v1/health")
        assert resp.status_code == 200


# ---------------------------------------------------------------------------
# Auth endpoints
# ---------------------------------------------------------------------------
class TestAuthEndpoints:
    def test_login_success(self, client):
        resp = client.post(
            "/api/v1/auth/login",
            data={"username": "admin", "password": "secret"},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert "access_token" in body
        assert body["token_type"] == "bearer"

    def test_login_failure(self, client):
        resp = client.post(
            "/api/v1/auth/login",
            data={"username": "admin", "password": "wrong"},
        )
        assert resp.status_code == 401

    def test_me_requires_auth(self, client):
        resp = client.get("/api/v1/auth/me")
        assert resp.status_code == 401

    def test_me_with_token(self, client, auth_headers):
        resp = client.get("/api/v1/auth/me", headers=auth_headers)
        assert resp.status_code == 200
        assert resp.json()["username"] == "admin"


# ---------------------------------------------------------------------------
# Logout & token blacklisting
# ---------------------------------------------------------------------------
class TestLogout:
    def test_logout_revokes_token(self, client, auth_token):
        headers = {"Authorization": f"Bearer {auth_token}"}
        resp = client.post("/api/v1/auth/logout", headers=headers)
        assert resp.status_code == 200

        resp2 = client.get("/api/v1/auth/me", headers=headers)
        assert resp2.status_code == 401

        blacklist.clear()


# ---------------------------------------------------------------------------
# Search endpoints (auth required)
# ---------------------------------------------------------------------------
class TestSearchEndpoints:
    def test_text_search_requires_auth(self, client):
        resp = client.post("/api/v1/search/text", json={"query": "shoes"})
        assert resp.status_code == 401

    def test_text_search_with_auth(self, client, auth_headers):
        resp = client.post(
            "/api/v1/search/text",
            json={"query": "red nike shoes", "limit": 5},
            headers=auth_headers,
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["success"] is True

    def test_image_search_requires_auth(self, client):
        resp = client.post("/api/v1/search/image", json={"image_path": "test.jpg"})
        assert resp.status_code == 401

    def test_hybrid_search_requires_auth(self, client):
        resp = client.post("/api/v1/search/hybrid", json={"query": "shoes"})
        assert resp.status_code == 401


# ---------------------------------------------------------------------------
# System endpoints
# ---------------------------------------------------------------------------
class TestSystemEndpoints:
    def test_system_status_requires_auth(self, client):
        resp = client.get("/api/v1/system/status")
        assert resp.status_code == 401

    def test_system_status_with_auth(self, client, auth_headers):
        resp = client.get("/api/v1/system/status", headers=auth_headers)
        assert resp.status_code == 200

    def test_rebuild_requires_admin(self, client, user_headers):
        resp = client.post("/api/v1/system/rebuild-index", headers=user_headers)
        assert resp.status_code == 403

    def test_rebuild_with_admin(self, client, auth_headers):
        resp = client.post("/api/v1/system/rebuild-index", headers=auth_headers)
        assert resp.status_code == 200
