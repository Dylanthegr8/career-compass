# backend/db/database.py
from flask_sqlalchemy import SQLAlchemy

# This is the main db instance used everywhere
db = SQLAlchemy()

def init_db(app):
    """
    Initialize the database with the Flask app
    Creates: backend/db/career_compass.db
    """
    import os
    
    
    db_dir = os.path.join(os.path.dirname(__file__))
    db_path = os.path.join(db_dir, "career_compass.db")
    
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        print("Database ready: backend/db/career_compass.db")
        print("Tables: users, student_profiles, careers, recommendations, etc.")