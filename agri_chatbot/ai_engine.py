# ai_engine.py (Groq – FINAL FIXED)
import os
from groq import Groq
from typing import Dict

# Load Groq API key
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("Set GROQ_API_KEY environment variable before running.")

# Create Groq client
client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """
You are AgriSage — an expert agriculture assistant.
Provide clear, practical, actionable guidance for farmers.
Keep responses concise, factual, and helpful.
"""

def answer_with_ai(question: str, context: Dict = None) -> str:
    """
    Chat completion using latest Groq models.
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",   # ⭐ Working model
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question}
        ],
        temperature=0.4,
        max_tokens=500
    )

    # IMPORTANT FIX: use .content instead of ["content"]
    return response.choices[0].message.content.strip()
