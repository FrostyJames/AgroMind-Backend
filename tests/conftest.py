# tests/conftest.py
import os
import sys
import pytest

@pytest.fixture(scope="session", autouse=True)
def set_test_env():
    """
    Automatically sets environment variables for the test session.
    Any test that imports app.config.settings will see these values.
    """
    os.environ["OPENAI_API_KEY"] = "fake_key"
    os.environ["SECRET_KEY"] = "test_secret"
    os.environ["DATABASE_URL"] = "sqlite:///test.db"
    os.environ["OPENWEATHER_API_KEY"] = "test_api_key"

    # Ensure settings.py reloads so new env vars are picked up
    if "app.config.settings" in sys.modules:
        del sys.modules["app.config.settings"]
