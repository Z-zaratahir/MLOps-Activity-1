from app import app


def test_health():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {
        "application_version": "1.0.0",
        "model_version": "model-7",
        "git_commit": "unknown",
        "status": "healthy",
    }


def test_prediction():
    client = app.test_client()

    response = client.post("/predict", json={"value": 5})

    assert response.status_code == 200
    data = response.get_json()
    assert data["input"] == 5.0
    assert data["prediction"] == 10.0
    assert data["application_version"] == "1.0.0"
    assert data["model_version"] == "model-7"


def test_prediction_rejects_missing_value():
    client = app.test_client()

    response = client.post("/predict", json={})

    assert response.status_code == 400
    assert response.get_json()["error"] == "JSON body must contain a numeric value"


def test_prediction_rejects_non_numeric_value():
    client = app.test_client()

    response = client.post("/predict", json={"value": "five"})

    assert response.status_code == 400
    assert response.get_json()["error"] == "value must be numeric"