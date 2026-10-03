# backend/auth.py
from flask import session, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database import db
from models import User, StudentProfile

def register_user(name, email, password):
    if User.query.filter_by(email=email).first():
        return False, "Email already registered!"
    
    hashed = generate_password_hash(password)
    user = User(email=email, password_hash=hashed)
    db.session.add(user)
    db.session.commit()

    profile = StudentProfile(user_id=user.id, full_name=name)
    db.session.add(profile)
    db.session.commit()

    return True, "Registered successfully!"

def login_user(email, password):
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password_hash, password):
        session['user_id'] = user.id
        session['user_email'] = user.email
        session['user_name'] = user.profile.full_name if user.profile else "Student"
        return True, "Login successful!"
    return False, "Invalid email or password"

def logout_user():
    session.clear()

def get_current_user():
    if 'user_id' in session:
        return User.query.get(session['user_id'])
    return None