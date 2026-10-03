from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db
from models import User, StudentProfile

users_bp = Blueprint("users", __name__)

@users_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    uid = int(get_jwt_identity())
    user = User.query.get(uid)
    profile = user.profile
    return jsonify(
        id=user.id,
        email=user.email,
        role=user.role,
        profile={
            "full_name": profile.full_name,
            "kcse_mean_grade": profile.kcse_mean_grade,
            "county": profile.county,
            "interests": profile.interests,
        }
    )

@users_bp.route("/me", methods=["PUT"])
@jwt_required()
def update_me():
    uid = int(get_jwt_identity())
    data = request.get_json() or {}
    profile = StudentProfile.query.filter_by(user_id=uid).first()
    for key in ["full_name", "kcse_mean_grade", "county", "interests"]:
        if key in data:
            setattr(profile, key, data[key])
    db.session.commit()
    return jsonify(message="updated")