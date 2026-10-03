# backend/gemini_client.py
import google.generativeai as genai
import os
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY") or "AU"
genai.configure(api_key=API_KEY)


model = genai.GenerativeModel("models/gemini-2.5-flash")

def get_gemini_reply(message: str) -> str:
    """Send message to Gemini and return the response."""
    try:
        response = model.generate_content(message)
        return response.text if response.text else "🤖 I didn't understand that."
    except Exception as e:
        print("Gemini Error:", e)
        return "⚠️ Error contacting Gemini. Please try again later."
