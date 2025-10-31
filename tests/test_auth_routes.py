import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch

# Patch Settings if needed (similar to alert_route tests)
with patch("app.config.settings.Settings") as MockSettings:
    MockSettings.return_value.SECRET_KEY = "test_secret"
    MockSettings.return_value.DATABASE_URL = "sqlite:///test.db"
    from app.routes import auth_routes

# Create temporary FastAPI app
app = FastAPI()
app.include_router(auth_routes.router)
client = TestClient(app)


# ------------------- Fixtures -------------------
@pytest.fixture
def mock_db_session():
    """Return a mocked SQLAlchemy session"""
    db = MagicMock()
    yield db


@pytest.fixture
def mock_user():
    """Return a fake User object"""
    user = MagicMock()
    user.id = 1
    user.name = "Test User"
    user.email = "test@example.com"
    user.hashed_password = "$2b$12$KIX/YOURHASHEDPW"
    return user


# ------------------- Tests -------------------

def test_register_user_success(mock_db_session, mock_user):
    """Test successful user registration"""
    # Patch get_user_by_email to return None (email not registered)
    with patch("app.routes.auth_routes.get_user_by_email", return_value=None), \
         patch("app.routes.auth_routes.hash_password", return_value="hashed_pw"), \
         patch("app.routes.auth_routes.User", return_value=mock_user):

        response = client.post(
            "/auth/register",
            params={"name": "Test User", "email": "test@example.com", "password": "password123"}
        )

    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "User registered"
    assert data["email"] == "test@example.com"
    assert data["user_id"] == 1


def test_register_user_email_exists(mock_db_session, mock_user):
    """Test registration with existing email"""
    with patch("app.routes.auth_routes.get_user_by_email", return_value=mock_user):
        response = client.post(
            "/auth/register",
            params={"name": "Test User", "email": "test@example.com", "password": "password123"}
        )

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_login_user_success(mock_db_session, mock_user):
    """Test successful login"""
    with patch("app.routes.auth_routes.authenticate_user", return_value=mock_user), \
         patch("app.routes.auth_routes.create_access_token", return_value="fake_token"):

        response = client.post(
            "/auth/login",
            data={"username": "test@example.com", "password": "password123"}
        )

    assert response.status_code == 200
    data = response.json()
    assert data["access_token"] == "fake_token"
    assert data["token_type"] == "bearer"


def test_login_user_invalid_credentials(mock_db_session):
    """Test login with invalid credentials"""
    with patch("app.routes.auth_routes.authenticate_user", return_value=None):
        response = client.post(
            "/auth/login",
            data={"username": "wrong@example.com", "password": "badpassword"}
        )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


def test_read_users_me_success(mock_user):
    """Test /me route returns current user info"""
    with patch("app.routes.auth_routes.get_current_user", return_value=mock_user):
        response = client.get("/auth/me")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Test User"
    assert data["email"] == "test@example.com"
