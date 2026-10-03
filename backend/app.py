# backend/app.py 
import sys
import os
from datetime import date
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify, session, redirect
from flask_cors import CORS
from chatbot import chatbot_bp
from auth import register_user, login_user, logout_user, get_current_user
from database import db, init_db
from models import User, StudentProfile
import pandas as pd
import joblib
import json


app = Flask(__name__, static_folder="../frontend", static_url_path="")
app.secret_key = "career_compass_kenya_2025_secure_254"
CORS(app, supports_credentials=True)

init_db(app)
app.register_blueprint(chatbot_bp, url_prefix="/chat")


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
try:
    df = pd.read_csv(os.path.join(BASE_DIR, "final_trained_dataset_perfect.csv"))
    model = joblib.load(os.path.join(BASE_DIR, "field_predictor.pkl"))
    field_enc = joblib.load(os.path.join(BASE_DIR, "field_encoder.pkl"))
    import recommender
    recommender.df = df
    recommender.model = model
    recommender.field_enc = field_enc
    print(f"SUCCESS: {len(df):,} courses loaded!")
except Exception as e:
    print("Recommender failed:", e)
    import recommender
    recommender.df = pd.DataFrame()

# Routes
@app.route("/")
def index():
    return redirect("/home.html")

@app.route("/<path:path>")
def serve(path):
    return app.send_static_file(path)

# Auth
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = request.get_json()
        success, msg = register_user(data.get("name"), data.get("email"), data.get("password"))
        return jsonify({"success": success, "message": msg})
    return app.send_static_file("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.get_json()
        email = data.get("email").strip().lower()  
        password = data.get("password")

        success, msg = login_user(email, password)

        if success:
            
            user = User.query.filter_by(email=email).first()

            if user and user.email == "admin@careercompass.ke":
                return jsonify({
                    "success": True,
                    "message": "Welcome Admin!",
                    "redirect": "/admin.html"
                })
            else:
                return jsonify({
                    "success": True,
                    "message": "Login successful!",
                    "redirect": "/home.html"
                })
        else:
            return jsonify({"success": False, "message": msg})

    return app.send_static_file("login.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/login.html")

@app.route("/home.html")
def home():
    if not get_current_user():
        return redirect("/login.html")
    return app.send_static_file("home.html")

# ADMIN — FULLY WORKING
@app.route("/admin.html")
def admin_page():
    user = get_current_user()
    if not user or user.email != "admin@careercompass.ke":
        return redirect("/login.html")
    return app.send_static_file("admin.html")

@app.route("/admin")
def admin_redirect():
    return redirect("/admin.html")

@app.route("/api/admin/stats")
def admin_stats():
    user = get_current_user()
    if not user or user.email != "admin@careercompass.ke":
        return jsonify({"error": "Forbidden"}), 403

    total_users = User.query.count()
    total_feedback = 0
    if os.path.exists("feedback.log"):
        with open("feedback.log", "r", encoding="utf-8") as f:
            total_feedback = len(f.readlines())

    active_today = User.query.filter(db.func.date(User.created_at) == date.today()).count()

    recent = User.query.order_by(User.id.desc()).limit(15).all()
    users_list = []
    for u in recent:
        p = u.profile
        users_list.append({
            "name": p.full_name if p and p.full_name else "Anonymous",
            "email": u.email,
            "grade": p.kcse_mean_grade if p and p.kcse_mean_grade else "—"
        })

    return jsonify({
        "total_users": total_users,
        "total_feedback": total_feedback,
        "active_today": active_today,
        "recent_users": users_list
    })

# API endpoints
@app.route("/api/recommend", methods=["POST"])
def recommend():
    try:
        result = recommender.recommend_careers(
            grade=request.json.get("grade"),
            field=request.json.get("field"),
            level=request.json.get("level", "Degree")
        )
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route("/api/feedback", methods=["POST"])
def feedback():
    try:
        with open("feedback.log", "a", encoding="utf-8") as f:
            f.write(json.dumps(request.json) + "\n")
        return jsonify({"success": True})
    except:
        return jsonify({"success": False}), 500

if __name__ == '__main__':
    print("\n" + "="*80)
    print("     CAREER COMPASS KENYA ")
    print("   Register → http://127.0.0.1:5000/register.html")
    print("     Login: admin@careercompass.ke / admin123")
    print("     Admin URL → http://127.0.0.1:5000/admin.html")
    print("="*80 + "\n")
    app.run(debug=True, port=5000)