import os
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("⚠️ GOOGLE_API_KEY not found in .env")

# -----------------------------
# Initialize Gemini AI
# -----------------------------
genai.configure(api_key=API_KEY)
# Use a stable Gemini model
model = genai.GenerativeModel("models/gemini-2.5-flash")

# -----------------------------
# Blueprint
# -----------------------------
chatbot_bp = Blueprint("chatbot_bp", __name__)

# -----------------------------
# In-memory session store
# -----------------------------
user_sessions = {}

# -----------------------------
# Local Kenyan career database (fallback)
# -----------------------------
career_data = {
    "technology": {
        "desc": "Technology drives innovation in Kenya — from fintech to mobile apps and AI.",
        "req": "B plain and above in KCSE with strong Math and English.",
        "unis": ["Strathmore University", "JKUAT", "KU", "University of Nairobi"],
        "jobs": ["Software Developer", "Data Scientist", "Network Engineer", "Cybersecurity Analyst"],
        "salary": "KSh 100,000 - 500,000+ per month."
    },
    "medicine": {
        "desc": "Medicine focuses on health and patient care. It’s among the most respected fields in Kenya.",
        "req": "A or A- in KCSE with strong Biology, Chemistry, and English.",
        "unis": ["UoN", "Moi University", "Egerton University", "Kabarak University"],
        "jobs": ["Doctor", "Pharmacist", "Surgeon", "Clinical Officer"],
        "salary": "KSh 150,000 - 500,000+ per month."
    },
    "law": {
        "desc": "Law focuses on justice and advocacy — preparing students for roles in the legal system.",
        "req": "B or higher in KCSE, strong in English and History.",
        "unis": ["UoN", "Strathmore", "KU", "MKU"],
        "jobs": ["Lawyer", "Judge", "Legal Officer", "Advocate"],
        "salary": "KSh 80,000 - 300,000+ per month."
    },
    "engineering": {
        "desc": "Engineering shapes the future — from civil and electrical to software and mechanical.",
        "req": "B or B+ in KCSE with strong Physics and Math.",
        "unis": ["UoN", "JKUAT", "Dedan Kimathi University", "Moi University"],
        "jobs": ["Civil Engineer", "Electrical Engineer", "Mechanical Engineer", "Software Engineer"],
        "salary": "KSh 120,000 - 400,000+ per month."
    }
}

# -----------------------------
# Helper Functions
# -----------------------------
def get_local_answer(msg: str):
    """Search the local Kenyan database for relevant info."""
    msg = msg.lower()
    for key, data in career_data.items():
        if key in msg:
            return (
                f"✅ *{key.title()}*\n\n"
                f"{data['desc']}\n\n"
                f"📘 Requirements: {data['req']}\n"
                f"🏫 Universities: {', '.join(data['unis'])}\n"
                f"💼 Careers: {', '.join(data['jobs'])}\n"
                f"💰 Salary Range: {data['salary']}\n\n"
                "Would you like to know related diploma or degree options?"
            )
    return None


def build_prompt(session: dict, message: str) -> str:
    """Build a structured prompt for Gemini AI."""
    user_context = (
        f"User name: {session.get('name', 'unknown')}, "
        f"KCSE grade: {session.get('grade', 'unknown')}."
    )
    return (
        f"You are Career GPT, a friendly Kenyan career advisor. "
        f"Use clear, human-like language with relevant Kenyan examples.\n\n"
        f"{user_context}\n\n"
        f"User: {message}"
    )

# -----------------------------
# Chatbot Endpoint
# -----------------------------
@chatbot_bp.route("/", methods=["POST"])
def chatbot():
    """Handles user chat messages."""
    data = request.get_json()
    message = data.get("message", "").strip()
    user_id = data.get("user_id", "guest")

    if not message:
        return jsonify({"reply": "Please type a message first."})

    # Track user session
    if user_id not in user_sessions:
        user_sessions[user_id] = {}
    session = user_sessions[user_id]

    # -----------------------------
    # Step 1: Capture user's name
    # -----------------------------
    if "name is" in message.lower():
        name = message.split("is")[-1].strip().capitalize()
        session["name"] = name
        return jsonify({"reply": f"Nice to meet you, {name}! What’s your KCSE grade?"})

    # -----------------------------
    # Step 2: Capture KCSE grade
    # -----------------------------
    grades = ["a", "a-", "b+", "b", "b-", "c+", "c", "c-", "d+", "d"]
    if message.lower() in grades:
        session["grade"] = message.upper()
        return jsonify({
            "reply": f"Got it! You scored {session['grade']}. What field interests you — Medicine, Law, Engineering, or Technology?"
        })

    # -----------------------------
    # Step 3: Try local fallback data
    # -----------------------------
    local_reply = get_local_answer(message)
    if local_reply:
        return jsonify({"reply": local_reply})

    # -----------------------------
    # Step 4: Use Gemini AI for open-ended questions
    # -----------------------------
    try:
        prompt = build_prompt(session, message)
        response = model.generate_content(prompt)
        reply = response.text.strip() if response and response.text else "Hmm, I didn’t get that. Could you rephrase?"
        return jsonify({"reply": reply})

    except Exception as e:
        print("Gemini Error:", e)
        fallback = get_local_answer(message)
        if fallback:
            return jsonify({"reply": fallback})
        return jsonify({
            "reply": (
                "⚠️ The AI service is currently unavailable. "
                "Please try again in a few moments or ask about specific fields like Technology, Medicine, or Law."
            )
        })
