from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
import subprocess
import sys

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def run_script(script_name):
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode != 0:
            return {
                "success": False,
                "script": script_name,
                "error": result.stderr,
                "output": result.stdout
            }

        return {
            "success": True,
            "script": script_name,
            "output": result.stdout
        }

    except Exception as e:
        return {
            "success": False,
            "script": script_name,
            "error": str(e)
        }


@app.route("/")
def home():
    return jsonify({"message": "PathGuardAI Backend Running"})


@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    save_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(save_path)

    return jsonify({
        "status": "File uploaded successfully",
        "path": save_path
    })


@app.route("/outputs/<path:filename>")
def serve_outputs(filename):
    return send_from_directory("../outputs", filename)


@app.route("/predict")
def predict():
    result = run_script("predict.py")
    status_code = 200 if result["success"] else 500
    return jsonify(result), status_code


@app.route("/criticality")
def criticality():
    result = run_script("criticality.py")
    status_code = 200 if result["success"] else 500
    return jsonify(result), status_code


@app.route("/simulate")
def simulate():
    result = run_script("simulation.py")
    status_code = 200 if result["success"] else 500
    return jsonify(result), status_code


@app.route("/route")
def route():
    result = run_script("routing.py")
    status_code = 200 if result["success"] else 500
    return jsonify(result), status_code


@app.route("/resilience")
def resilience():
    result = run_script("resilience_score.py")
    status_code = 200 if result["success"] else 500
    return jsonify(result), status_code


@app.route("/recommendation")
def recommendation():
    result = run_script("recommendation.py")
    status_code = 200 if result["success"] else 500
    return jsonify(result), status_code


@app.route("/resilience-data")
def resilience_data():
    return send_from_directory("../outputs", "resilience.json")


if __name__ == "__main__":
    app.run(debug=False)