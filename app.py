from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from db import get_db, close_db, init_db
from routes.profiles import profiles_bp
from routes.recommendations import recs_bp
from routes.chatbot import chatbot_bp   # ✅ Correct chatbot route import
import os

# -----------------------------
# 1️⃣ Create Flask App
# -----------------------------
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# -----------------------------
# 2️⃣ Register Blueprints
# -----------------------------
app.register_blueprint(profiles_bp, url_prefix="/api/profiles")
app.register_blueprint(recs_bp, url_prefix="/api/recommendations")
app.register_blueprint(chatbot_bp, url_prefix="/api/chatbot")  # ✅ Chatbot endpoint

# -----------------------------
# 3️⃣ Database Setup and Teardown
# -----------------------------
app.teardown_appcontext(close_db)

@app.cli.command("init-db")
def init_db_command():
    """Initialize the database."""
    init_db()
    print("✅ Database initialized!")

# -----------------------------
# 4️⃣ Health Check Endpoint
# -----------------------------
@app.route("/api/health")
def health():
    return jsonify({"status": "OK"})

# -----------------------------
# 5️⃣ Serve Frontend Files
# -----------------------------
@app.route("/")
def serve_home():
    frontend_path = os.path.join(os.path.dirname(__file__), "../frontend")
    return send_from_directory(frontend_path, "home.html")

@app.route("/<path:filename>")
def serve_static_files(filename):
    frontend_path = os.path.join(os.path.dirname(__file__), "../frontend")
    return send_from_directory(frontend_path, filename)

# -----------------------------
# 6️⃣ Custom 404 Error Page
# -----------------------------
@app.errorhandler(404)
def page_not_found(e):
    frontend_path = os.path.join(os.path.dirname(__file__), "../frontend")
    if os.path.exists(os.path.join(frontend_path, "404.html")):
        return send_from_directory(frontend_path, "404.html"), 404
    return jsonify({"error": "Page Not Found"}), 404

# -----------------------------
# 7️⃣ Run the Server
# -----------------------------
if __name__ == "__main__":
    # Initialize database if missing
    if not os.path.exists("career.db"):
        with app.app_context():
            init_db()

    # Run the server on all network interfaces (so others can connect via your IP)
    app.run(host="0.0.0.0", port=5000, debug=True)
