from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import joblib
import numpy as np
import traceback

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# Load the model you saved earlier (ensure crop_model.pkl exists in the same folder)
MODEL_PATH = "crop_model.pkl"
model = None

def load_model():
    global model
    model = joblib.load(MODEL_PATH)
    print("Model loaded from", MODEL_PATH)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json if request.is_json else request.form.to_dict()
        # Extract values - ensure numeric conversion
        required = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
        missing = [k for k in required if k not in data or data[k] == ""]
        if missing:
            return jsonify({"success": False, "error": f"Missing inputs: {', '.join(missing)}"}), 400

        # Convert to float
        vals = []
        for k in required:
            try:
                vals.append(float(data[k]))
            except Exception:
                return jsonify({"success": False, "error": f"Invalid value for {k}: {data[k]}"}), 400

        # Model expects shape (1,7)
        arr = np.array(vals).reshape(1, -1)
        prediction = model.predict(arr)  # returns an array of predicted labels
        predicted_label = str(prediction[0])

        return jsonify({"success": True, "prediction": predicted_label})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    load_model()
    # Use host=0.0.0.0 only if you want external access; localhost is sufficient for local dev
    app.run(host="127.0.0.1", port=5000, debug=True)
