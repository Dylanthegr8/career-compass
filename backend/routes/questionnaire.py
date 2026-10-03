from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db
from models import QuestionnaireItem, QuestionnaireResponse

questionnaire_bp = Blueprint("questionnaire", __name__)

@questionnaire_bp.route("/items", methods=["GET"])
def items():
    items = QuestionnaireItem.query.order_by(QuestionnaireItem.id.asc()).all()
    return jsonify([{"id": i.id, "text": i.text, "dimension": i.dimension} for i in items])

@questionnaire_bp.route("/items/seed", methods=["POST"])
def seed_items():
    demo = [
        ("I enjoy solving math or logic problems.", "STEM"),
        ("I like creating art, design, or content.", "ARTS"),
        ("I like organizing groups and leading initiatives.", "BUSINESS"),
        ("I care about helping people directly.", "HEALTH"),
        ("I enjoy tinkering with hardware/electronics.", "ENGINEERING"),
    ]
    for text, dim in demo:
        db.session.add(QuestionnaireItem(text=text, dimension=dim))
    db.session.commit()
    return jsonify(message="seeded")

@questionnaire_bp.route("/responses", methods=["POST"])
@jwt_required()
def submit_responses():
    uid = int(get_jwt_identity())
    data = request.get_json() or {}
    responses = data.get("responses", [])
    if not responses:
        return jsonify(error="responses required"), 400
    for r in responses:
        db.session.add(QuestionnaireResponse(user_id=uid, item_id=int(r["item_id"]), score=int(r["score"])))
    db.session.commit()
    return jsonify(message="saved")