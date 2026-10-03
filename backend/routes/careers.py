from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from db import db
from models import Career

careers_bp = Blueprint("careers", __name__)

@careers_bp.route("/", methods=["GET"])
@jwt_required(optional=True)
def list_careers():
    q = request.args.get("q")
    query = Career.query
    if q:
        like = f"%{q.strip()}%"
        query = query.filter(Career.title.ilike(like))
    items = query.order_by(Career.title.asc()).limit(200).all()
    return jsonify([{
        "id": c.id,
        "title": c.title,
        "min_grade": c.min_grade,
        "subjects_required": c.subjects_required,
        "pathways": c.pathways,
    } for c in items])

@careers_bp.route("/seed", methods=["POST"])
def seed():
    # Seed a small catalog for demo. Remove in prod.
    demo = [
        dict(title="Software Engineer", min_grade="B", subjects_required="Math, Physics, Comp", pathways="BSc Computer Science; Diploma in IT", description="Builds software systems."),
        dict(title="Nurse", min_grade="C+", subjects_required="Biology, Chemistry", pathways="BSc Nursing; Diploma in Nursing", description="Provides healthcare services."),
        dict(title="Civil Engineer", min_grade="B+", subjects_required="Math, Physics", pathways="BSc Civil Engineering", description="Designs infrastructure."),
        dict(title="Teacher (Education Arts)", min_grade="C+", subjects_required="English/Kiswahili, History", pathways="BEd Arts; Diploma in Education", description="Teaches in schools."),
    ]
    for d in demo:
        if not Career.query.filter_by(title=d["title"]).first():
            db.session.add(Career(**d))
    db.session.commit()
    return jsonify(message="seeded")