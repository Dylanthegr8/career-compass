# backend/chatbot.py
from flask import Blueprint, request, jsonify
from gemini_client import get_gemini_reply

chatbot_bp = Blueprint("chatbot_bp", __name__)


user_sessions = {}


career_data = {
    "technology": {
        "desc": "Technology drives innovation in Kenya — from fintech to mobile apps and AI.",
        "req": "B plain and above in KCSE with strong Math and English.",
        "unis": ["Strathmore University", "JKUAT", "KU", "University of Nairobi"],
        "jobs": ["Software Developer", "Data Scientist", "Network Engineer", "Cybersecurity Analyst"],
        "salary": "KSh 100,000 - 500,000+ per month."
    },
    "medicine": {
        "desc": "Medicine focuses on health and patient care. It’s among the most respected fields in Kenya.",
        "req": "A or A- in KCSE with strong Biology, Chemistry, and English.",
        "unis": ["UoN", "Moi University", "Egerton University", "Kabarak University"],
        "jobs": ["Doctor", "Pharmacist", "Surgeon", "Clinical Officer"],
        "salary": "KSh 150,000 - 500,000+ per month."
    },
    "law": {
        "desc": "Law focuses on justice and advocacy — preparing students for roles in the legal system.",
        "req": "B or higher in KCSE, strong in English and History.",
        "unis": ["UoN", "Strathmore", "KU", "MKU"],
        "jobs": ["Lawyer", "Judge", "Legal Officer", "Advocate"],
        "salary": "KSh 80,000 - 300,000+ per month."
    },
    "engineering": {
        "desc": "Engineering shapes the future — from civil and electrical to software and mechanical.",
        "req": "B or B+ in KCSE with strong Physics and Math.",
        "unis": ["UoN", "JKUAT", "Dedan Kimathi University", "Moi University"],
        "jobs": ["Civil Engineer", "Electrical Engineer", "Mechanical Engineer", "Software Engineer"],
        "salary": "KSh 120,000 - 400,000+ per month."
    }
}

# OFF-TOPIC FILTER 
OFF_TOPIC_TRIGGERS = [
    # ═══════════════════════════════════════════════════════════════════════════════
    # WEATHER 
    # ═══════════════════════════════════════════════════════════════════════════════
    "weather", "rain", "temperature", "forecast", "cloudy", "sunny", "hot", "cold",
    "nairobi weather", "mombasa weather", "kisumu weather", "nakuru weather",
    "thunderstorm", "lightning", "humidity", "windy", "barometer", "meteo","weather", 
    "rain", "temperature", "forecast", "cloudy", "sunny", "hot", "cold",
    "raining", "hapa nje", "leo baridi", "jua kali", "mvua", "mawingu",

    # ═══════════════════════════════════════════════════════════════════════════════
    # POLITICS (Kenya + global)
    # ═══════════════════════════════════════════════════════════════════════════════
    "ruto", "raila", "gachagua", "mudavadi", "wetangula", "orengo", "gachagua",
    "election", "politics", "government", "mp", "senator", "vote", "azimio", "uda",
    "kenya kwanza", "handshake", "impeachment", "parliament", "national assembly",
    "president", "deputy president", "constitution", "bill", "referendum",
    "biden", "trump", "putin", "modi", "xi jinping", "ukraine", "gaza", "israel","ruto", 
    "raila", "election", "politics", "government", "mp", "senator", "vote",
    "azimio", "uda", "president", "kenya kwanza", "odm", "gachagua", "riggy g",
    "sakaja", "johnson sakaja", "impeach", "impeachment", "bbc", "citizen tv",
    "breaking news", "latest news", "trending", "viral", "shocking",

    # ═══════════════════════════════════════════════════════════════════════════════
    # PHONES / GADGETS / TECH REVIEWS / CARS
    # ═══════════════════════════════════════════════════════════════════════════════
    "iphone", "samsung", "pixel", "huawei", "tecno", "infinix", "itEL", "oppo", "vivo",
    "phone", "smartphone", "specs", "review", "gadget", "unboxing", "benchmark",
    "battery life", "camera quality", "ram", "storage", "processor", "chipset",
    "laptop", "macbook", "dell", "hp", "lenovo", "surface", "gaming laptop",
    "headphones", "airpods", "earbuds", "smartwatch", "apple watch", "fitbit",
    "car", "toyota", "mercedes", "subaru", "range rover", "prado", "harrier",
    "bmw", "audi", "land cruiser", "nissan", "honda", "fuel consumption",
    "tyres", "engine", "transmission", "buy car", "used car", "new car", "iphone", 
    "samsung", "pixel", "xiaomi", "oppo", "tecno", "infinix", "realme",
    "phone", "specs", "review", "gadget", "buy phone", "buy car", "which phone",
    "best phone", "camera", "battery life", "charger", "airpods", "earbuds",
    "toyota", "mercedes", "subaru", "car", "range rover", "land cruiser", "prado",
    "mazda", "nissan", "bmw", "audi", "harrier", "vitz", "which car",

    # ═══════════════════════════════════════════════════════════════════════════════
    # ENTERTAINMENT / CELEBRITIES / MUSIC / MOVIES / SPORTS
    # ═══════════════════════════════════════════════════════════════════════════════
    "celebrity", "gossip", "beyonce", "rihanna", "drake", "taylor swift", "ariana grande",
    "movie", "netflix", "series", "film", "hollywood", "bollywood", "oscars",
    "bien", "sauti sol", "willy paul", "akon", "burna boy", "diamond", "zuchu",
    "harmonize", "rayvanny", "emaarufu", "koffi olomide", "fally ipupa",
    "gengetone", "bahati", "size 8", "guardian angel", "nandy", "marioo",
    "premier league", "man united", "chelsea", "arsenal", "liverpool", "mancity",
    "messi", "ronaldo", "mbappe", "neymar", "haaland", "salah", "de bruyne",
    "afc leopards", "gor mahia", "world cup", "euros", "champions league",
    "wwe", "undertaker", "john cena", "roman reigns", "undertaker",
    "big brother", "bbnaija", "bBNaija", "reality show", "tiktok", "instagram", 
    "iphone", "samsung", "pixel", "xiaomi", "oppo", "tecno", "infinix", "realme",
    "phone", "specs", "review", "gadget", "buy phone", "buy car", "which phone",
    "best phone", "camera", "battery life", "charger", "airpods", "earbuds",
    "toyota", "mercedes", "subaru", "car", "range rover", "land cruiser", "prado",
    "mazda", "nissan", "bmw", "audi", "harrier", "vitz", "which car", "messi", "ronaldo",
    "neymar", "mbappe", "man u", "manchester united", "arsenal",
    "chelsea", "liverpool", "barcelona", "real madrid", "champions league",
    "premier league", "who won", "world cup", "afcon", "bet", "sportpesa", "odibets",
    "betika", "mcheza", "betting tips", "jackpot", "football", "gor mahia", "afc leopards",

    # ═══════════════════════════════════════════════════════════════════════════════
    # MATH / CALCULATIONS / GENERAL KNOWLEDGE / TRIVIA
    # ═══════════════════════════════════════════════════════════════════════════════
    "math", "mathematics", "calculate", "calc", "solve", "equation", "algebra",
    "geometry", "trigonometry", "calculus", "derivative", "integral", "matrix",
    "2 + 2", "x +", "+ x", "find x", "what is", "how many", "how much",
    "capital of", "who invented", "when was", "where is", "define", "meaning",
    "population of", "tallest",  "richest",
    "trivia", "quiz", "riddle", "puzzle", "brain teaser", "sudoku",    "math", 
    "calculate", "solve", "equation", "algebra", "geometry", "find x",
    "2 + 2", "x +", "+ x", "capital of","population", "define", "meaning",  "distance",
      "height", "weight","joke", 
    "tell me a joke", "funny", "meme", "lol", "lmao", "haha", "hahaha",
    "good morning", "good night", "how are you", "what is your name", "are you human",
    "sing for me", "rap", "dance", "bored", "entertain me", "bby", "babe", "love you",

    # ═══════════════════════════════════════════════════════════════════════════════
    # NEWS / CURRENT EVENTS / RANDOM
    # ═══════════════════════════════════════════════════════════════════════════════
    "news", "breaking news", "what happened", "latest news", "headlines",
    "covid", "coronavirus", "pandemic", "vaccine", "stock market", "shares",
    "bitcoin", "crypto", "doge", "ethereum", "nfts", "cooking", "recipe",
    "restaurant", "food", "bet", "sportpesa", "betika", "odibets", "flashscore""jesus", 
    "allah", "prayer", "church", "mosque", "pastor", "prophet", "sheikh",
    "tithe", "offering", "heaven", "hell", "sin", "muslim", "christian", "bible", "quran","weed", 
    "bhang", "marijuana", "cocaine", "drugs", "how to make money fast",
    "hack", "hacking", "free money", "nudes", "sexting", "porn", "sex", "escort",
    "call girl", "sugar mummy", "sugar daddy", "blesser", "bleaching", "guns", "bomb"
]

def is_off_topic(message: str) -> bool:
    msg = message.lower().strip()
    
    # Whitelist
    if any(word in msg for word in ["kcse", "scored", "grade", "interested in", "bsc", "bachelor", 
                                    "diploma", "nursing", "pharmacy", "engineering", "law", "cybersecurity", 
                                    "usiu", "moi", "uon", "strathmore", "jkuat", "tuk", "requirements", 
                                    "scholarships", "campus life", "job opportunities"]):
        return False
    
   
    return any(trigger in msg for trigger in OFF_TOPIC_TRIGGERS)

REFUSAL_MESSAGE = (
    "Sorry! I'm your career coach  I only help with KCSE grades, university courses, "
    "jobs, resumes, interviews, skills, and scholarships in Kenya.\n\n"
    "Kindly ask me something about your future!"
)
# ─────────────────────────────────────────────────────────────────────────────

def get_local_answer(msg: str):
    msg = msg.lower()
    for key, data in career_data.items():
        if key in msg:
            return (
                f"{key.title()}\n\n"
                f"{data['desc']}\n\n"
                f"Requirements: {data['req']}\n"
                f"Universities: {', '.join(data['unis'])}\n"
                f"Careers: {', '.join(data['jobs'])}\n"
                f"Salary Range: {data['salary']}\n\n"
                "Would you like to know related diploma or degree options?"
            )
    return None

@chatbot_bp.route("/", methods=["POST"])
def chatbot():
    data = request.get_json()
    message = data.get("message", "").strip()
    user_id = data.get("user_id", "guest")

    if not message:
        return jsonify({"reply": "Please type a message first."})

    if user_id not in user_sessions:
        user_sessions[user_id] = {}
    session = user_sessions[user_id]

    # Capture user's name
    if "name is" in message.lower():
        name = message.split("is")[-1].strip().capitalize()
        session["name"] = name
        return jsonify({"reply": f"Nice to meet you, {name}! What’s your KCSE grade?"})

    # Capture KCSE grade
    grades = ["a", "a-", "b+", "b", "b-", "c+", "c", "c-", "d+", "d"]
    if message.lower() in grades:
        session["grade"] = message.upper()
        return jsonify({"reply": f"Got it! You scored {session['grade']}. What field interests you — Medicine, Law, Engineering, or Technology?"})

    # BLOCK ONLY OFF-TOPIC MESSAGES
    if is_off_topic(message):
        return jsonify({"reply": REFUSAL_MESSAGE})

    # Check local database first
    local_reply = get_local_answer(message)
    if local_reply:
        return jsonify({"reply": local_reply})

    # Use Gemini AI for everything else
    reply = get_gemini_reply(message)
    return jsonify({"reply": reply})