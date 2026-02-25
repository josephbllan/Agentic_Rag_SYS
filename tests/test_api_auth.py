"""Tests for API authentication (JWT creation, validation, login flow)"""
import pytest
from datetime import timedelta
from unittest.mock import patch

from api.security.jwt_handler import (
    create_access_token,
    get_user,
    authenticate_user,
    User,
)


class TestTokenCreation:
    def test_create_token_returns_string(self):
        """Verifies that creating an access token produces a non-empty string."""
        token = create_access_token({"sub": "admin"})
        assert isinstance(token, str)
        assert len(token) > 10

    def test_custom_expiry(self):
        """Verifies that a token with a custom expiry delta is created successfully."""
        token = create_access_token({"sub": "admin"}, expires_delta=timedelta(minutes=1))
        assert isinstance(token, str)


class TestGetUser:
    def test_existing_user(self):
        """Checks that retrieving an existing user returns a valid User with correct roles."""
        user = get_user("admin")
        assert user is not None
        assert user.username == "admin"
        assert "admin" in user.roles

    def test_missing_user(self):
        """Confirms that looking up a non-existent user returns None."""
        assert get_user("nonexistent") is None


class TestAuthenticateUser:
    def test_correct_credentials(self):
        """Verifies that valid credentials return the authenticated user object."""
        user = authenticate_user("admin", "secret")
        assert user is not None
        assert user.username == "admin"

    def test_wrong_password(self):
        """Confirms that an incorrect password causes authentication to return None."""
        assert authenticate_user("admin", "wrong") is None

    def test_nonexistent_user(self):
        """Confirms that authenticating a non-existent user returns None."""
        assert authenticate_user("ghost", "secret") is None
