# AgroMind-Backend API
## AI-Powered Crop & Farm Management System
AgroMind is a backend API built with FastAPI, providing intelligent tools for farmers to manage crops, monitor farm data, and receive AI-powered insights on crop health and climate alerts.
## Features
🌾 Crop Management — Add, retrieve, update, and delete crop data.

🧠 AI Crop Health Analysis — Integrated with an AI service to analyze crop conditions and give recommendations.

🧑‍🌾 Farm Management — Manage farms and their associated crops.

⚡ Task Tracking — Record farming activities like planting, watering, or harvesting.

☀️ Climate Alerts — Get real-time weather and climate alerts from the OpenWeather API.

🔐 Authentication — Secure registration and login using JWT tokens.

📘 Interactive Documentation — Swagger & ReDoc auto-generated API documentation.

## Tech Stack
Framework: FastAPI

Database: SQLAlchemy + SQLite

Authentication: OAuth2 + JWT

AI Integration: OpenAI

Docs: Swagger & ReDoc

## Live link
https://agromind-backend-2v1j.onrender.com/
## AI API Endpoints
| Endpoint            | Method | Description                                            |
| ------------------- | ------ | ------------------------------------------------------ |
| `/recommendations/` | `POST` | Analyze crop health and get AI recommendations         |
| `/crops/`           | `POST` | Create a crop and automatically get an AI health score |
| `/alerts/`          | `GET`  | Retrieve climate alerts for the farm region            |

Example AI request:
``` bash
{
  "crop_name": "Maize",
  "growth_stage": "Flowering"
}

```
Example AI response:
``` bash
{
  "health_score": 84.3,
  "advice": "Crop health is good. Maintain consistent   watering."
}

``` 
## Testing
The backend routes and services were tested using pytest, with FastAPI’s TestClient for API endpoints and unittest.mock for mocking external requests (e.g., OpenWeather API).

Note: Some tests require environment variables (like OPENAI_API_KEY, SECRET_KEY, and DATABASE_URL) to be set. If these are missing in your environment, tests may fail with validation errors. These do not indicate a problem with the project itself — the application works correctly when the environment variables are provided.

### Running the tests
1. Install the test dependencies (if not already installed):
```bash
pip install pytest requests
```

2. From the project root, run all tests:
```bash
pytest
```
3. To run a specific test file (e.g., test_alert_route.py):
```bash
pytest tests/test_alert_route.py
```

4. (Optional) Show detailed output:
```bash
pytest -v
```

This setup allows you to verify that the routes and services behave as expected in a controlled environment.