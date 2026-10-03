# backend/admin.py
from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template
from database import db
from models import User, StudentProfile, Feedback
from functools import wraps
from datetime import date

admin_bp = Blueprint('admin_bp', __name__, template_folder='../templates')

# ────────────────────── ADMIN LOGIN REQUIRED DECORATOR ──────────────────────
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return jsonify({"error": "Admin login required"}), 401
        return f(*args, **kwargs)
    return decorated_function

# ────────────────────── ADMIN LOGIN PAGE ──────────────────────
@admin_bp.route('/admin/login')
def admin_login_page():
    return render_template('admin_login.html')  # We'll create this in a sec

@admin_bp.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # CHANGE THIS TO YOUR REAL ADMIN CREDENTIALS
    ADMIN_EMAIL = "admin@careercompass.co.ke"
    ADMIN_PASS  = "admin123"   # Change this! Or better: store in .env

    if email == ADMIN_EMAIL and password == ADMIN_PASS:
        session['admin_logged_in'] = True
        return jsonify({"success": True, "redirect": "/admin.html"})
    
    return jsonify({"error": "Invalid credentials"}), 401

@admin_bp.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return jsonify({"success": True})

# ────────────────────── REAL ADMIN STATS FROM DATABASE ──────────────────────
@admin_bp.route('/api/admin/stats')
@admin_required
def admin_stats():
    try:
        total_users = User.query.count()
        total_feedback = Feedback.query.count()

        today = date.today()
        active_today = db.session.query(User).filter(
            db.func.date(User.updated_at) == today
        ).count()

        kcse_2024 = StudentProfile.query.filter(
            StudentProfile.kcse_mean_grade.isnot(None)
        ).count()

        recent_users = db.session.query(
            User.id, 
            StudentProfile.full_name, 
            User.email, 
            StudentProfile.kcse_mean_grade
        ).outerjoin(StudentProfile, User.id == StudentProfile.user_id)\
         .order_by(User.created_at.desc())\
         .limit(10).all()

        recent_list = []
        for u in recent_users:
            recent_list.append({
                "name": u.full_name or "Anonymous",
                "email": u.email or "N/A",
                "grade": u.kcse_mean_grade or "Not set",
                "year": "2024"
            })

        return jsonify({
            "total_users": total_users,
            "total_feedback": total_feedback,
            "active_today": active_today,
            "kcse_2024": kcse_2024,
            "recent_users": recent_list
        })

    except Exception as e:
        print("Admin stats error:", e)
        return jsonify({"error": str(e)}), 500