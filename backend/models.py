# backend/db/models.py
from datetime import datetime
from database import db  

class TimestampMixin:
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class User(db.Model, TimestampMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="student")
    profile = db.relationship("StudentProfile", backref="user", uselist=False)

class StudentProfile(db.Model, TimestampMixin):
    __tablename__ = "student_profiles"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    full_name = db.Column(db.String(120))
    kcse_mean_grade = db.Column(db.String(5))
    county = db.Column(db.String(100))
    interests = db.Column(db.Text)

class Career(db.Model, TimestampMixin):
    __tablename__ = "careers"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    min_grade = db.Column(db.String(5))
    subjects_required = db.Column(db.Text)
    pathways = db.Column(db.Text)

class QuestionnaireItem(db.Model, TimestampMixin):
    __tablename__ = "questionnaire_items"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    dimension = db.Column(db.String(50))

class QuestionnaireResponse(db.Model, TimestampMixin):
    __tablename__ = "questionnaire_responses"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("questionnaire_items.id"), nullable=False)
    score = db.Column(db.Integer, nullable=False)

class Recommendation(db.Model, TimestampMixin):
    __tablename__ = "recommendations"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    career_id = db.Column(db.Integer, db.ForeignKey("careers.id"), nullable=False)
    rationale = db.Column(db.Text)

class Feedback(db.Model, TimestampMixin):
    __tablename__ = "feedback"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    career_id = db.Column(db.Integer, db.ForeignKey("careers.id"), nullable=True)
    recommendation_id = db.Column(db.Integer, db.ForeignKey("recommendations.id"), nullable=True)
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text)

    user = db.relationship("User", backref="feedbacks")
    career = db.relationship("Career", backref="feedbacks")
    recommendation = db.relationship("Recommendation", backref="feedbacks")