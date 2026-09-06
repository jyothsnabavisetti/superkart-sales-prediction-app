
from flask import Flask, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

MODEL_PATH = "superkart_model.joblib"

# Load serialized preprocessing + model pipeline
model = joblib.load(MODEL_PATH)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "SuperKart Sales Prediction API is running",
        "status": "success"
    })


@app.route("/v1/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "error": "JSON request body is required"
            }), 400

        input_data = pd.DataFrame([data])

        prediction = model.predict(input_data)

        return jsonify({
            "Predicted_Product_Store_Sales_Total": float(prediction[0])
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400


@app.route("/v1/predictbatch", methods=["POST"])
def predict_batch():
    try:
        if "file" not in request.files:
            return jsonify({
                "error": "CSV file is required"
            }), 400

        file = request.files["file"]

        data = pd.read_csv(file)

        predictions = model.predict(data)

        data["Predicted_Product_Store_Sales_Total"] = predictions

        return jsonify({
            "status": "success",
            "predictions": data.to_dict(orient="records")
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
