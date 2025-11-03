import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import MagicMock, patch
from datetime import timedelta, datetime
from jose import jwt, JWTError

# Import the functions to test
from app.services import auth_service  # adjust import if your file name is different

# Patch settings to avoid env dependency
@patch("app.services.auth_service.settings")
def test_password_hashing_and_verification(mock_settings):
    mock_settings.SECRET_KEY = "test_secret"
    
    password = "my_password"
    hashed = auth_service.get_password_hash(password)
    assert hashed != password
    assert auth_service.verify_password(password, hashed) is True
    assert auth_service.verify_password("wrong", hashed) is False


@patch("app.services.auth_service.settings")
def test_create_access_token_contains_email(mock_settings):
    mock_settings.SECRET_KEY = "test_secret"
    
    data = {"sub": "user@example.com"}
    token = auth_service.create_access_token(data)
    decoded = jwt.decode(token, mock_settings.SECRET_KEY, algorithms=["HS256"])
    
    assert decoded["sub"] == "user@example.com"
    assert "exp" in decoded


def test_authenticate_user_success_and_failure():
    # Mock a user object
    class MockUser:
        email = "user@example.com"
        password = auth_service.get_password_hash("secret")

    # Mock DB session
    mock_db = MagicMock()
    mock_db.query().filter().first.side_effect = [MockUser(), None]

    # Successful authentication
    user = auth_service.authenticate_user(mock_db, "user@example.com", "secret")
    assert user is not None
    assert user.email == "user@example.com"

    # Failed authentication (wrong password)
    user = auth_service.authenticate_user(mock_db, "user@example.com", "wrong")
    assert user is None

    # Failed authentication (nonexistent user)
    user = auth_service.authenticate_user(mock_db, "missing@example.com", "secret")
    assert user is None


@patch("app.services.auth_service.settings")
def test_register_user_success_and_duplicate(mock_settings):
    mock_settings.SECRET_KEY = "test_secret"

    # Mock DB session
    mock_db = MagicMock()
    mock_db.query().filter().first.side_effect = [None, MagicMock()]  # first call: no user, second: user exists
    mock_db.add = MagicMock()
    mock_db.commit = MagicMock()
    mock_db.refresh = MagicMock()

    # Successful registration
    user = auth_service.register_user(mock_db, "Test", "new@example.com", "password")
    assert user.email == "new@example.com"
    assert mock_db.add.called
    assert mock_db.commit.called
    assert mock_db.refresh.called

    # Duplicate email
    with pytest.raises(Exception):
        auth_service.register_user(mock_db, "Test", "duplicate@example.com", "password")


@patch("app.services.auth_service.settings")
def test_get_current_user_success_and_failure(mock_settings):
    mock_settings.SECRET_KEY = "test_secret"

    # Mock DB session
    class MockUser:
        email = "user@example.com"

    mock_db = MagicMock()
    mock_db.query().filter().first.side_effect = [MockUser(), None]

    # Create a valid token
    token = auth_service.create_access_token({"sub": "user@example.com"})

    # Success
    user = auth_service.get_current_user(db=mock_db, token=token)
    assert user.email == "user@example.com"

    # Invalid token
    with pytest.raises(Exception):
        auth_service.get_current_user(db=mock_db, token="invalidtoken")
