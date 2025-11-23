# ml_engine.py
import os
import joblib
import numpy as np

MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")

MODEL_FILES = {
    "crop_price": "crop_price.pkl",
    "yield": "yield_model.pkl",
    "pest_risk": "pest_risk.pkl",
    "fertilizer_need": "fertilizer_need.pkl",
    "rainfall_risk": "rainfall_risk.pkl"
}

def load_model(task):
    file_name = MODEL_FILES.get(task)
    if not file_name:
        return None
    
    path = os.path.join(MODEL_DIR, file_name)
    
    if os.path.exists(path):
        try:
            return joblib.load(path)
        except Exception:
            return None
    return None


def predict_with_ml(task: str, features: dict):
    """
    Main function your Flask app needs.
    Handles both real models and fallback heuristics.
    """

    model = load_model(task)

    # -------------------------
    # If a real trained model exists
    # -------------------------
    if model:
        try:
            # Use feature ordering from the model if available
            if hasattr(model, "feature_names_in_"):
                ordered = [features.get(k, 0) for k in model.feature_names_in_]
                X = np.array(ordered).reshape(1, -1)
            else:
                # fallback: sort input keys (consistent but simple)
                sorted_keys = sorted(features.keys())
                ordered = [features.get(k, 0) for k in sorted_keys]
                X = np.array(ordered).reshape(1, -1)

            prediction = model.predict(X)
            return {
                "task": task,
                "prediction": float(prediction[0]),
                "used_model": True
            }
        except Exception as e:
            # If model fails, continue to heuristics
            pass

    # --------------------------------
    # FALLBACK HEURISTICS (dummy logic)
    # --------------------------------
    if task == "crop_price":
        month = features.get("month", 6)
        demand = features.get("demand_index", 1.0)
        avg_yield = features.get("avg_yield", 1.0)
        price = 100 * (1 + 0.05 * (12 - abs(6 - month))) * demand / max(0.5, avg_yield)
        return {"task": task, "prediction": round(price, 2), "used_model": False}

    if task == "yield":
        rainfall = features.get("rainfall_mm", 500)
        fertilizer = features.get("fertilizer_kg_per_ha", 100)
        soil_idx = features.get("soil_index", 1.0)
        yield_est = 0.002 * rainfall + 0.01 * fertilizer * soil_idx
        return {"task": task, "prediction": round(yield_est, 2), "used_model": False}

    if task == "pest_risk":
        humidity = features.get("humidity", 60)
        temp = features.get("temperature_c", 28)
        recent = features.get("recent_pests", 0)
        risk = min(1.0, max(0.02, (humidity/100) * (temp/35) + 0.1*recent))
        return {"task": task, "prediction": round(risk, 2), "used_model": False}

    if task == "fertilizer_need":
        deficit = features.get("nitrogen_deficit_kg", 20)
        stage = features.get("crop_stage", 2)
        need = deficit * (1 + 0.1 * (3 - stage))
        return {"task": task, "prediction": round(max(0, need), 2), "used_model": False}

    if task == "rainfall_risk":
        recent = features.get("recent_7days_mm", 40)
        prob = min(0.99, max(0.01, recent / 100))
        return {"task": task, "prediction": round(prob, 2), "used_model": False}

    # Unknown task
    return {
        "task": task,
        "error": "Unknown task",
        "used_model": False
    }
