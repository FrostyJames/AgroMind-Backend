from fastapi import APIRouter
import requests

router = APIRouter(prefix="/alerts", tags=["Alerts"])

OPENWEATHER_API_KEY = "4fe45097e86fbd3d1d6f82aa14fe74b4"
LAT, LON = -0.2, 35.1  # Nandi County coordinates

@router.get("/")
def get_climate_alerts():
    url = (
        f"https://api.openweathermap.org/data/2.5/onecall?"
        f"lat={LAT}&lon={LON}&exclude=minutely,hourly,daily&appid={OPENWEATHER_API_KEY}"
    )
    res = requests.get(url)
    data = res.json()
    return data.get("alerts", [])