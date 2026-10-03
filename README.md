# Career Compass 🎓

**Career Compass** is an AI-assisted career guidance and university course recommendation platform designed to help students make more informed decisions about their academic and career pathways.

The system combines academic information, career preferences, machine-learning models, and generative AI to provide personalized career recommendations and interactive guidance.

---

## 🚀 Overview

Choosing a university course and career path can be challenging, particularly when students are unsure how their academic performance, interests, and career goals align with available opportunities.

Career Compass addresses this problem by providing a centralized platform where students can:

* Create and manage their profiles
* Provide academic and career-related information
* Receive personalized career recommendations
* Explore recommended career pathways
* Interact with an AI-powered career chatbot
* Submit feedback
* Access personalized recommendations through a web interface

The project was developed as a university software engineering project with a focus on combining **web development, machine learning, databases, and generative AI** to address a real-world education and career guidance problem.

---

## ✨ Key Features

### 👤 User Management

* User registration and login
* User authentication
* Profile management
* Personalized user experience

### 🎯 Career Recommendations

* Academic and profile-based career recommendations
* Machine-learning powered prediction
* Career recommendation models
* Field and career classification

### 🤖 AI Career Assistant

* Interactive career guidance chatbot
* Generative AI integration
* AI-assisted responses to career-related questions

### 📊 Recommendations & Analytics

* Personalized recommendations
* Recommendation results interface
* Analytics functionality for administrators

### 💬 Feedback

* User feedback functionality
* Feedback management through the platform

### 🛠️ Administration

* Administrative functionality
* User and system management
* Analytics dashboard

---

## 🏗️ System Architecture

The project is divided into two main components:

```text
Career Compass
│
├── Frontend
│   ├── HTML
│   ├── CSS
│   ├── JavaScript
│   └── Assets
│
└── Backend
    ├── Flask Application
    ├── Authentication
    ├── Database Layer
    ├── Recommendation Engine
    ├── Machine Learning Models
    ├── AI Chatbot
    └── API Routes
```

---

## 💻 Technology Stack

### Frontend

* HTML5
* CSS3
* JavaScript

### Backend

* Python
* Flask

### Database

* SQLite

### Machine Learning

* Python
* Scikit-learn
* Pickle-based trained models

### Generative AI

* Google Gemini API

### Development Tools

* Jupyter Notebook
* Git
* GitHub

---

## 🧠 Machine Learning

Career Compass incorporates trained machine-learning models to support career and field recommendations.

The backend includes trained model artifacts such as:

```text
best_career_model.pkl
field_predictor.pkl
field_encoder.pkl
label_encoder.pkl
```

The project also includes a Jupyter Notebook used during the machine-learning development and experimentation process:

```text
Kenya_KCSE_Career_Advisor_Final.ipynb
```

The recommendation system uses academic and career-related information to generate relevant career pathways for students.

---

## 🤖 Generative AI Integration

The platform incorporates Google's Gemini API to provide AI-assisted career guidance and chatbot functionality.

The AI component is designed to complement the recommendation system by allowing users to interact with the platform and ask career-related questions in a conversational manner.

API credentials should be stored securely using environment variables rather than being committed to the repository.

---

## 📁 Project Structure

```text
career-compass/
│
├── backend/
│   ├── routes/
│   ├── app.py
│   ├── admin.py
│   ├── auth.py
│   ├── chatbot.py
│   ├── config.py
│   ├── database.py
│   ├── db.py
│   ├── gemini_client.py
│   ├── models.py
│   ├── recommender.py
│   ├── train_dataset.py
│   ├── requirements.txt
│   ├── best_career_model.pkl
│   ├── field_encoder.pkl
│   ├── field_predictor.pkl
│   └── label_encoder.pkl
│
├── frontend/
│   ├── assets/
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── profile.html
│   ├── recommendations.html
│   ├── chat.html
│   ├── analytics.html
│   ├── feedback.html
│   └── admin.html
│
└── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/career-compass.git
cd career-compass
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

On macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r backend/requirements.txt
```

### 4. Configure environment variables

Create a `.env` file for sensitive configuration such as API credentials.

Example:

```text
GEMINI_API_KEY=your_api_key_here
```

**Do not commit your `.env` file or API keys to GitHub.**

### 5. Run the application

From the project directory:

```bash
python backend/app.py
```

The application should then be available through the local development server configured by the Flask application.

---

## 🔐 Security Considerations

For production deployment, the following should be handled securely:

* API keys should be stored in environment variables.
* Database credentials should not be committed to source control.
* User data should be protected and validated.
* Production applications should use a production-grade database.
* Authentication credentials should be securely hashed and managed.
* Sensitive configuration files should be excluded using `.gitignore`.

---

## 🎓 Project Context

Career Compass was developed as an academic project focused on applying software engineering and artificial intelligence to career and university-course guidance.

The project brings together multiple areas of computing, including:

* Software engineering
* Web application development
* Database management
* Machine learning
* Generative AI
* System design
* User authentication
* Data analysis

The project was designed with the goal of providing students with a technology-assisted approach to exploring potential academic and career pathways.

---

## 🔮 Future Improvements

Potential improvements include:

* Expanding the career and university course dataset
* Improving recommendation accuracy through additional training data
* Adding more comprehensive career pathway information
* Developing a mobile application
* Implementing a production-grade database
* Adding advanced analytics and reporting
* Improving authentication and authorization
* Deploying the platform to a cloud environment
* Adding automated testing and CI/CD
* Improving accessibility and responsive design

---

## 👨‍💻 Developer

**Dylan Matibe**

Bachelor of Business Information Technology
Strathmore University

Interested in **Software Engineering, Business Intelligence, Data, Artificial Intelligence, and Technology Solutions**.

---

## 📄 License

This project was developed for academic and educational purposes.
