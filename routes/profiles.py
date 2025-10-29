from flask import Blueprint, request, jsonify

profiles_bp = Blueprint("profiles", __name__)

@profiles_bp.route("/temporary", methods=["POST"])
def temp_profile():
    """
    Accepts KCSE grade and interests, and returns recommendations.
    No login required.
    """
    data = request.get_json(force=True)
    kcse_grade = data.get("kcse_grade", "").strip().upper()
    interests = data.get("interests", "").strip().lower()

    if not kcse_grade or not interests:
        return jsonify({"error": "KCSE grade and interests are required."}), 400

    # Store data in request context (optional, not persistent)
    request.kcse_grade = kcse_grade
    request.interests = interests

    # Forward to recommendations
    from .recommendations import get_recommendations_for_temp_profile
    recs = get_recommendations_for_temp_profile(kcse_grade, interests)

    return jsonify({"recommendations": recs}), 200
