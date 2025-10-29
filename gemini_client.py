# backend/gemini_client.py
import google.generativeai as genai

# Configure API key
genai.configure(api_key="YOUR_GEMINI_API_KEY")  # replace with your actual key

# Select the Gemini model
model = genai.GenerativeModel("models/gemini-2.5-flash")

def get_gemini_reply(message: str) -> str:
    """
    Send message to Gemini and return the response.
    """
    try:
        response = model.generate_content(message)
        return response.text if response.text else "🤖 I didn't understand that."
    except Exception as e:
        print("Gemini Error:", e)
        return "⚠️ Error contacting Gemini. Please try again later."
