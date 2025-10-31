import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from openai import OpenAI
from app.config import settings
from app.services.ai_service import analyze_crop_health
from unittest.mock import patch, MagicMock 
import json

# ---------------- TESTS ---------------- #

@patch("app.services.ai_service.client")
def test_analyze_crop_health_valid_json(mock_client):
    """✅ Should return valid parsed JSON when OpenAI responds correctly."""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content=json.dumps({
        "health_score": 90,
        "advice": "Healthy crop."
    })))]
    mock_client.chat.completions.create.return_value = mock_response

    result = analyze_crop_health("maize", "flowering")
    assert result["health_score"] == 90
    assert result["advice"] == "Healthy crop."


@patch("app.services.ai_service.client")
def test_analyze_crop_health_invalid_json(mock_client):
    """⚠️ Should handle invalid JSON from AI gracefully."""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="INVALID JSON"))]
    mock_client.chat.completions.create.return_value = mock_response

    result = analyze_crop_health("beans", "seedling")
    assert result["health_score"] == 75.0
    assert "invalid format" in result["advice"].lower()


@patch("app.services.ai_service.client")
def test_analyze_crop_health_quota_error(mock_client):
    """🚫 Should return fallback advice when quota or 429 error occurs."""
    mock_client.chat.completions.create.side_effect = Exception("insufficient_quota")
    result = analyze_crop_health("rice", "harvest")
    assert result["health_score"] == 78.0
    assert "fallback" in result["advice"].lower()


@patch("app.services.ai_service.client")
def test_analyze_crop_health_general_error(mock_client):
    """💥 Should handle general API errors gracefully."""
    mock_client.chat.completions.create.side_effect = Exception("network down")
    result = analyze_crop_health("tomato", "germination")
    assert result["health_score"] == 50.0
    assert "unavailable" in result["advice"].lower()