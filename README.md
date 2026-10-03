# Career GPT (MVP)

A starter project for an AI Career Guidance web app with:
- **Backend**: Flask + MySQL (JWT auth, profiles, careers, questionnaire, naive recommendations)
- **Frontend**: Simple HTML/CSS/JS for testing the API
- **DB**: MySQL schema and sample seed data

> AI model is deliberately **not** included yet. You can integrate it later (e.g., in `backend/routes/recommendations.py`).

## Quick Start

### 1) MySQL
- Create DB and tables:
  ```sql
  SOURCE db/schema.sql;
  SOURCE db/seed.sql;
  ```

### 2) Backend
- Create virtual env, install deps:
  ```bash
  cd backend
  python -m venv .venv
  . .venv/bin/activate  # Windows: .venv\Scripts\activate
  pip install -r requirements.txt
  cp .env.example .env  # then edit values to match your MySQL
  python app.py
  ```
- Health check: `GET http://127.0.0.1:5000/api/health`

### 3) Frontend
- Open `frontend/index.html` in your browser.
- Sequence:
  1. Register → Login
  2. Seed careers + Seed questionnaire
  3. Fill profile (KCSE mean grade + interests) → Save
  4. Get Recommendations

## Where to add AI later
- Replace the naive logic in `backend/routes/recommendations.py` with:
  - A trained model loaded from `models/` or a service endpoint.
  - Use questionnaire responses + KCSE + interests as features.

## Notes
- Security hardening and validation are still minimal — for MVP only.
