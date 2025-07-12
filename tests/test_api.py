import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import REQUIRED_CSV_COLUMN, REQUIRED_JSON_FIELD
import pandas as pd
import io
import json

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_match_single_success():
    response = client.post("/match", json={"query": "Buro AG"})
    assert response.status_code == 200
    data = response.json()
    assert data["top_match"]["entity"] == "Büro AG"
    assert data["top_match"]["confidence"] > 0.8

def test_match_single_empty():
    response = client.post("/match", json={"query": ""})
    assert response.status_code == 400 or response.status_code == 422

def test_match_batch_csv():
    df = pd.DataFrame({REQUIRED_CSV_COLUMN: ["Buro AG", "Buro GmbH"]})
    content = df.to_csv(index=False).encode()
    files = {"file": ("test.csv", content, "text/csv")}
    response = client.post("/match/batch", files=files)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["match"] is not None

def test_match_batch_json():
    df = pd.DataFrame({REQUIRED_JSON_FIELD: ["Buro AG", "Buro GmbH"]})
    json_str = df.to_json()
    content = json_str.encode()
    files = {"file": ("test.json", content, "application/json")}
    response = client.post("/match/batch", files=files)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["match"] is not None

def test_match_batch_invalid_file():
    files = {"file": ("test.txt", b"irrelevant", "text/plain")}
    response = client.post("/match/batch", files=files)
    assert response.status_code == 400 