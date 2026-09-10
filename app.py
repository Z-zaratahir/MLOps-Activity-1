import os

from flask import Flask, jsonify, request


app = Flask(__name__)

APPLICATION_VERSION = os.getenv("APPLICATION_VERSION", "1.0.0")
MODEL_VERSION = os.getenv("MODEL_VERSION", "model-7")
GIT_COMMIT = os.getenv("GIT_COMMIT", "unknown")


@app.get("/")
def home():
    return jsonify({"service": "mlops-cd-demo", "status": "running"})


@app.get("/health")
def health():
    return jsonify(
        {
            "application_version": APPLICATION_VERSION,
            "model_version": MODEL_VERSION,
            "git_commit": GIT_COMMIT,
            "status": "healthy",
        }
    )


@app.post("/predict")
def predict():
    data = request.get_json(silent=True)
    if not isinstance(data, dict) or "value" not in data:
        return jsonify({"error": "JSON body must contain a numeric value"}), 400

    try:
        value = float(data["value"])
    except (TypeError, ValueError):
        return jsonify({"error": "value must be numeric"}), 400

    return jsonify(
        {
            "input": value,
            "prediction": value * 2,
            "application_version": APPLICATION_VERSION,
            "model_version": MODEL_VERSION,
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)