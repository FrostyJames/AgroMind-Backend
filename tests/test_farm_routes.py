import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from fastapi.testclient import TestClient
from fastapi import status
from unittest.mock import patch, MagicMock
from app.main import app
from app.schemas.farm_schema import FarmCreate, FarmResponse
from unittest.mock import patch, ANY


client = TestClient(app)

# Sample data
sample_farm = {
    "id": 1,
    "name": "Sunny Acres",
    "location": "Kenya",
    "size_hectares": 10,
    "crops": []
}

farm_payload = {
    "name": "Sunny Acres",
    "location": "Kenya",
    "size_hectares": 10
}


# ------------------ TEST CREATE FARM ------------------
@patch("app.services.farm_service.create_farm")
def test_create_farm(mock_create):
    mock_create.return_value = sample_farm
    response = client.post("/farms/", json=farm_payload)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == sample_farm["name"]
    assert data["location"] == sample_farm["location"]
    assert data["size_hectares"] == sample_farm["size_hectares"]
    mock_create.assert_called_once()

# ------------------ TEST LIST FARMS ------------------
@patch("app.services.farm_service.get_farms")
def test_list_farms(mock_get):
    mock_get.return_value = [sample_farm]
    response = client.get("/farms/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == sample_farm["name"]
    assert data[0]["location"] == sample_farm["location"]
    mock_get.assert_called_once()


# ------------------ TEST GET FARM BY ID ------------------
@patch("app.services.farm_service.get_farm_by_id")
def test_get_farm_success(mock_get):
    mock_get.return_value = sample_farm
    response = client.get("/farms/1")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sample_farm["id"]
    assert data["name"] == sample_farm["name"]
    mock_get.assert_called_once_with(ANY, 1)

@patch("app.services.farm_service.get_farm_by_id")
def test_get_farm_not_found(mock_get):
    mock_get.return_value = None
    response = client.get("/farms/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Farm not found"}

# ------------------ TEST UPDATE FARM ------------------
@patch("app.services.farm_service.update_farm")
@patch("app.services.farm_service.get_farm_by_id")
def test_update_farm(mock_get, mock_update):
    mock_get.return_value = sample_farm
    updated_farm = {**sample_farm, "size_hectares": 12.0}
    mock_update.return_value = updated_farm

    update_payload = {
        "name": sample_farm["name"],
        "location": sample_farm["location"],
        "size_hectares": 12
    }

    response = client.put("/farms/1", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["size_hectares"] == 12
    mock_get.assert_called_once()
    mock_update.assert_called_once()

# ------------------ TEST DELETE FARM ------------------
@patch("app.services.farm_service.delete_farm")
@patch("app.services.farm_service.get_farm_by_id")
def test_delete_farm(mock_get, mock_delete):
    mock_get.return_value = sample_farm
    mock_delete.return_value = None

    response = client.delete("/farms/1")
    assert response.status_code == 200
    assert response.json() == {"detail": "Farm with ID 1 deleted successfully."}
    mock_get.assert_called_once()
    mock_delete.assert_called_once()
