# app.py
import os
from flask import Flask, request, jsonify, send_from_directory
from ai_engine import answer_with_ai
from ml_engine import predict_with_ml
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder="static", static_url_path="/static")


@app.route("/")
def index():
    return send_from_directory("static", "chatbot.html")


@app.route("/api/ask", methods=["POST"])
def api_ask():
    data = request.json or {}
    question = data.get("question", "").strip()
    context = data.get("context", {})

    if not question:
        return jsonify({"error": "No question provided"}), 400

    try:
        answer = answer_with_ai(question, context=context)
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/predict", methods=["POST"])
def api_predict():
    payload = request.json or {}
    task = payload.get("task")
    features = payload.get("features", {})

    if not task:
        return jsonify({"error": "No task specified"}), 400

    try:
        result = predict_with_ml(task, features)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"\n🚀 AgriSage running at http://localhost:{port}\n")
    app.run(host="0.0.0.0", port=port, debug=True)
#$env:GROQ_API_KEY="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"