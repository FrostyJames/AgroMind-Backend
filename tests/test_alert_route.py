import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import pytest

# Patch Settings BEFORE importing alert_route
with patch("app.config.settings.Settings") as MockSettings:
    # Configure fake values
    MockSettings.return_value.OPENAI_API_KEY = "fake_key"
    MockSettings.return_value.SECRET_KEY = "test_secret"
    MockSettings.return_value.DATABASE_URL = "sqlite:///test.db"

    # Now safe to import alert_route
    from app.routes import alert_route

    # Temporary FastAPI app for isolated route testing
    app = FastAPI()
    app.include_router(alert_route.router)
    client = TestClient(app)


@pytest.fixture
def mock_weather_response():
    """Fixture to simulate OpenWeather API response."""
    return {
        "alerts": [
            {
                "sender_name": "Kenya Meteorological Department",
                "event": "Heavy Rain Warning",
                "description": "Expect heavy rainfall over the next 24 hours.",
            }
        ]
    }


@patch("app.routes.alert_route.requests.get")
def test_get_climate_alerts_returns_alerts(mock_get, mock_weather_response):
    mock_response = MagicMock()
    mock_response.json.return_value = mock_weather_response
    mock_get.return_value = mock_response

    response = client.get("/alerts/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["event"] == "Heavy Rain Warning"
    assert "description" in data[0]

    mock_get.assert_called_once()
    called_url = mock_get.call_args[0][0]
    assert "api.openweathermap.org/data/2.5/onecall" in called_url


@patch("app.routes.alert_route.requests.get")
def test_get_climate_alerts_handles_missing_alerts(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {}  # no alerts key
    mock_get.return_value = mock_response

    response = client.get("/alerts/")
    assert response.status_code == 200
    assert response.json() == []


@patch("app.routes.alert_route.requests.get")
def test_get_climate_alerts_handles_request_error(mock_get):
    mock_get.side_effect = Exception("Network Error")

    response = client.get("/alerts/")
    assert response.status_code == 500
