import pytest
from app.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'URL Shortener API'

def test_shorten_valid_url(client):
    response = client.post("/api/shorten", json={"url": "https://example.com"})
    assert response.status_code == 201
    data = response.get_json()
    assert "short_code" in data
    assert "short_url" in data

def test_shorten_invalid_url(client):
    response = client.post("/api/shorten", json={"url": "invalid-url"})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

def test_redirect_and_click_count(client):
    # shortening the URL
    res = client.post("/api/shorten", json={"url": "https://example.com"})
    short_code = res.get_json()["short_code"]

    # Simulating multiple accesses
    for _ in range(3):
        redirect_res = client.get(f"/{short_code}")
        assert redirect_res.status_code == 302

    # Analytics check
    stats_res = client.get(f"/api/stats/{short_code}")
    data = stats_res.get_json()
    assert stats_res.status_code == 200
    assert data["clicks"] == 3
    assert data["url"] == "https://example.com"
    assert "created_at" in data

# for non-existing short code
def test_stats_invalid_code(client):
    response = client.get("/api/stats/nonexistent123")
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data
