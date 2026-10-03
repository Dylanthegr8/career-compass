from flask import Blueprint, request, jsonify
from recommender import recommend_careers

recs_bp = Blueprint("recommendations", __name__)

@recs_bp.route("/recommend", methods=["POST"])
def get_recommendations():
    try:
        data = request.get_json()
        grade = data.get("grade")
        field = data.get("field")
        level = data.get("level", "Degree")

        if not grade or not field:
            return jsonify({"success": False, "error": "Grade and field are required."}), 400

        result = recommend_careers(grade, field, level)
        return jsonify(result)
    except Exception as e:
        print("Error in /recommend:", e)
        return jsonify({"success": False, "error": str(e)}), 500
