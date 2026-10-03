# routes/feedback.py

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Feedback
from db import db

feedback_bp = Blueprint("feedback", __name__)

@feedback_bp.route("/", methods=["POST"])
@jwt_required()
def give_feedback():
    uid = int(get_jwt_identity())
    data = request.get_json() or {}
    career_id = data.get("career_id")
    rating = int(data.get("rating", 0))
    comment = data.get("comment", "")

    if not career_id or not rating:
        return jsonify(error="career_id and rating required"), 400

    fb = Feedback(student_id=uid, career_id=career_id, rating=rating, comment=comment)
    db.session.add(fb)
    db.session.commit()
    return jsonify(message="feedback saved"), 201
