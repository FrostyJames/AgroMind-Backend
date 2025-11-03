# 🌾 AgroMind API Documentation

**Version:** 1.0.0  
**Framework:** FastAPI  
**Description:** The AgroMind Backend API powers crop, farm, and climate management features, integrating AI for crop health recommendations.

---

## Base URLs


- `https://agromind-backend-2v1j.onrender.com/`

---

## Authentication

Most endpoints are open, but user-specific actions use JWT authentication.  
To access protected routes, include a bearer token:

Authorization: Bearer <access_token>

Tokens are obtained from `/auth/login`.

---

## Endpoints Overview

| Category | Prefix | Description |
|-----------|--------|-------------|
| Authentication | `/auth` | Register, login, and get current user |
| Farms | `/farms` | CRUD operations for farm data |
| Crops | `/crops` | CRUD operations and AI crop analysis |
| Recommendations | `/recommendations` | Get AI-based crop health insights |
| Tasks | `/tasks` | Manage farm task list |
| Alerts | `/alerts` | Fetch real-time climate alerts |
| AI | `/ai` | AI endpoints (used for internal crop analysis) |
| Activities | `/activities` | Farm-related activity logging (internal) |

---

## Authentication Routes

### `POST /auth/register`
Register a new user.

**Body Parameters:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword"
}
```
Response:
``` json
{
  "message": "User registered",
  "user_id": 1,
  "email": "john@example.com"
}
```

### `POST /auth/login`
Authenticate user and receive access token.

**Body (Form Data):**
``` makefile
username: john@example.com
password: securepassword
```
**Response:**
```json
{
  "access_token": "<JWT_TOKEN>",
  "token_type": "bearer"
}
```
### `GET /auth/me`

Retrieve currently logged-in user details.

**Headers:**
``` makefile
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com"
}
```
## Farm Routes
### `POST /farms`

Create a new farm record.

Request:
```json
{
  "name": "Green Valley Farm",
  "location": "Nandi County",
  "size": "50 acres"
}
```

Response:
```json
{
  "id": 1,
  "name": "Green Valley Farm",
  "location": "Nandi County",
  "size": "50 acres"
}
```
### `GET /farms`

Retrieve all farm records.

Response:
```json
[
  {
    "id": 1,
    "name": "Green Valley Farm",
    "location": "Nandi County",
    "size": "50 acres"
  }
]
```
### `GET /farms/{farm_id}`

Retrieve a specific farm by ID.

Response:
```json
{
  "id": 1,
  "name": "Green Valley Farm",
  "location": "Nandi County",
  "size": "50 acres"
}
```
### `PUT /farms/{farm_id}`

Update a farm’s details.

Request:
```json
{
  "name": "Green Valley Farm Updated",
  "location": "Nandi County",
  "size": "55 acres"
}
```

Response:
```json
{
  "id": 1,
  "name": "Green Valley Farm Updated",
  "location": "Nandi County",
  "size": "55 acres"
}
```
### `DELETE /farms/{farm_id}`

Delete a farm record.

Response:
```json
{ "detail": "Farm with ID 1 deleted successfully." }
```
## Crop Routes
### `POST /crops`

Create a new crop and trigger AI health analysis.

Request:
```json
{
  "name": "Maize",
  "growth_stage": "Vegetative",
  "farm_id": 1
}
```

Response:
```json
{
  "id": 1,
  "name": "Maize",
  "growth_stage": "Vegetative",
  "health_score": 91.0,
  "advice": "Maintain proper watering at this stage."
}
```
### `GET /crops`

Retrieve all crops.

Response:
```json
[
  {
    "id": 1,
    "name": "Maize",
    "growth_stage": "Vegetative",
    "health_score": 91.0
  }
]
```
### `GET /crops/{crop_id}`

Retrieve a crop by ID.

Response:
```json
{
  "id": 1,
  "name": "Maize",
  "growth_stage": "Vegetative",
  "health_score": 91.0
}
```
### `DELETE /crops/{crop_id}`

Delete a crop by ID.

Response:
```json
{ "detail": "Crop with ID 1 deleted successfully." }
```
## Recommendation Routes
### `POST /recommendations`

Get AI-generated health insights for a crop.

Request:
```json
{
  "crop_name": "Maize",
  "growth_stage": "Flowering"
}
```

Response:
```json
{
  "health_score": 82.5,
  "advice": "Add nitrogen fertilizer to improve yield."
}
```
## Task Routes
### `POST /tasks`

Add a new task to the farm.

Request:
```json
{
  "crop": "Maize",
  "date": "2025-11-02",
  "activity": "Weeding"
}
```

Response:
```json
{
  "message": "Task added",
  "task": {
    "crop": "Maize",
    "date": "2025-11-02",
    "activity": "Weeding"
  }
}
```
### `GET /tasks`

Retrieve all tasks.

Response:
```json
[
  {
    "crop": "Maize",
    "date": "2025-11-02",
    "activity": "Weeding"
  }
]
```
## Alerts Routes
### `GET /alerts`

Retrieve live weather alerts for Nandi County using OpenWeather API.

Response Example (if alerts available):
```json
[
  {
    "sender_name": "Kenya Meteorological Department",
    "event": "Heavy Rainfall Warning",
    "description": "Expect heavy rains in Nandi County for the next 24 hours."
  }
]
```

If no alerts are available:
```json
[]
```
### AI & Activities Routes

These are internal routes used by the system’s AI and logging services.
They integrate with the OpenAI API for analysis and track farm-related activities.
## Data Models (Schemas)
User
```json
{
  "id": int,
  "name": string,
  "email": string,
  "hashed_password": string
}
```
Farm
```json
{
  "id": int,
  "name": string,
  "location": string,
  "size": string
}
```

Crop
```json
{
  "id": int,
  "name": string,
  "growth_stage": string,
  "health_score": float,
  "advice": string
}
```
Task
```json
{
  "crop": string,
  "date": string,
  "activity": string
}
```
Recommendation
```json
{
  "crop_name": string,
  "growth_stage": string,
  "health_score": float,
  "advice": string
}
```