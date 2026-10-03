# routes/admin.py

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Feedback
from db import db

admin_bp = Blueprint("admin", __name__)

def is_admin(user_id):
    user = User.query.get(user_id)
    return user and user.role == "admin"

@admin_bp.route("/users", methods=["GET"])
@jwt_required()
def list_users():
    uid = int(get_jwt_identity())
    if not is_admin(uid):
        return jsonify(error="forbidden"), 403

    users = User.query.all()
    return jsonify([
        {"id": u.id, "email": u.email, "role": u.role}
        for u in users
    ])

@admin_bp.route("/feedback", methods=["GET"])
@jwt_required()
def list_feedback():
    uid = int(get_jwt_identity())
    if not is_admin(uid):
        return jsonify(error="forbidden"), 403

    feedbacks = Feedback.query.all()
    return jsonify([
        {
            "id": f.id,
            "student_id": f.student_id,
            "career_id": f.career_id,
            "rating": f.rating,
            "comment": f.comment
        } for f in feedbacks
    ])
