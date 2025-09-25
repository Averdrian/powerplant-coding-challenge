
import sys
import json
import pytest

#Append to pythonpath src so we can import app
from pathlib import Path
SRC_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(SRC_DIR))


from app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client
        
        
def load_json(filename) -> dict:
    test_payload_dir = Path(__file__).resolve().parents[3]
    file_path = test_payload_dir / f"example_payloads/{filename}"
    
    with file_path.open() as f:
        return json.load(f)

def test_energy_production(client):
    
    payload = load_json("payload3.json")
    expected_response = load_json("response3.json")
    
    response = client.post(
        "/productionplan",
        data = json.dumps(payload),
        content_type = "application/json"
    )
    
    assert response.status_code == 200
    assert sorted(response.get_json(), key=lambda x: x["name"]) == sorted(expected_response, key=lambda x: x["name"])
    
    
