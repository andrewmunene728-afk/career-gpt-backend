from flask import Blueprint
from db import get_db

recs_bp = Blueprint("recommendations", __name__)

def get_recommendations_for_temp_profile(kcse_grade, interests):
    """
    Generate recommendations for non-logged-in users
    """
    db = get_db()
    profile_grade = kcse_grade.upper()
    interests = interests.lower()

    # Fetch all careers
    careers = db.execute("SELECT * FROM careers").fetchall()

    # Grade priority order
    grade_order = ["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "E"]

    def grade_meets_requirement(user_grade, required_grade):
        if user_grade not in grade_order or required_grade not in grade_order:
            return False
        return grade_order.index(user_grade) <= grade_order.index(required_grade)

    # Filter careers
    results = []
    for c in careers:
        if grade_meets_requirement(profile_grade, c["required_grade"]):
            if interests in c["field"].lower() or interests in c["title"].lower():
                results.append({
                    "title": c["title"],
                    "field": c["field"],
                    "description": c["description"]
                })

    # If no matches, return general careers
    if not results:
        results = [{"title": c["title"], "field": c["field"], "description": c["description"]} for c in careers]

    return results
