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

Docs: Auto-generated with FastAPI (Swagger & ReDoc)

## Installation and Setup
### 1. Clone the repository
``` bash
git clone https://github.com/your-username/agromind-backend.git
cd agromind-backend
```
### 2. Create a virtual environment
``` bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```
### 3. Install dependencies
``` bash
pip install -r requirements.txt
```
### 4. Run the FastAPI server
``` bash
uvicorn app.main:app --reload
```
### 5. Access the API
Base URL: http://localhost:8000

Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc

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