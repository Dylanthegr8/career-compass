# backend/recommender.py 
import pandas as pd
from functools import lru_cache
import re


df = pd.DataFrame()
model = None
field_enc = None


def grade_to_points(grade: str) -> int:
    mapping = {
        'A': 84, 'A-': 77, 'B+': 70, 'B': 63, 'B-': 56,
        'C+': 49, 'C': 42, 'C-': 35, 'D+': 28, 'D': 21, 'D-': 14, 'E': 7
    }
    return mapping.get(grade.strip().upper(), 0)


PUBLIC_UNIVERSITIES = [
    "University of Nairobi", "UoN",
    "Jomo Kenyatta University of Agriculture and Technology", "JKUAT",
    "Kenyatta University", "KU",
    "Moi University", "Moi",
    "Egerton University", "Egerton",
    "Maseno University", "Maseno",
    "Technical University of Kenya", "TUK",
    "Masinde Muliro University of Science and Technology", "MMUST",
    "University of Eldoret", "Eldoret",
    "Dedan Kimathi University of Technology", "DeKUT", "Dedan Kimathi",
    "South Eastern Kenya University", "SEKU",
    "Murang'a University of Technology", "Murang'a",
    "Machakos University",
    "Pwani University",
    "Karatina University",
    "Multimedia University of Kenya", "Multimedia",
    "Co-operative University of Kenya", "Cooperative",
    "Meru University of Science and Technology", "MUST",
    "Kisii University",
    "Laikipia University",
    "Chuka University",
    "Garissa University",
    "Taita Taveta University",
    "Kirinyaga University",
    "Tharaka University",
    "Embu University",
    "Rongo University",
    "Bomet University College",
    "Tom Mboya University",
    "Turkana University College",
    "Kaimosi Friends University",
    "Alupe University",
    "Koitaleel Samoei University College",
    "University of Kabianga", "Kabianga"
]

PUBLIC_PATTERN = "|".join([re.escape(name) for name in PUBLIC_UNIVERSITIES])


FIELD_TAXONOMY = {
    "medicine": {
        "keywords": ["medicine", "mbchb", "surgery", "nursing", "clinical", "dental", "pharmacy", "laboratory", "optometry", "physiotherapy", "radiography", "biomedical", "health", "nutrition", "public health", "medical"],
        "cluster": "Cluster 15–18",
        "min_grade": "B+",
        "example_jobs": "Doctor, Surgeon, Pharmacist, Nurse, Dentist, Clinical Officer"
    },
    "engineering": {
        "keywords": ["engineering", "civil", "mechanical", "electrical", "chemical", "aerospace", "mechatronics", "automotive", "marine", "geospatial", "surveying", "architectural", "structural", "quantity surveying"],
        "cluster": "Cluster 7–10",
        "min_grade": "B",
        "example_jobs": "Civil Engineer, Electrical Engineer, Mechanical Engineer, Architect"
    },
    "law": {
        "keywords": ["law", "llb", "legal", "jurisprudence", "advocate"],
        "cluster": "Cluster 3",
        "min_grade": "B",
        "example_jobs": "Advocate, Judge, Magistrate, Corporate Lawyer"
    },
    "computer science": {
        "keywords": ["computer science", "software engineering", "data science", "artificial intelligence", "cybersecurity", "information systems", "informatics", "computer technology", "ict", "it "],
        "cluster": "Cluster 11",
        "min_grade": "B-",
        "example_jobs": "Software Engineer, Data Scientist, Cybersecurity Expert, AI Specialist"
    },
    "business": {
        "keywords": ["business", "commerce", "accounting", "finance", "marketing", "management", "procurement", "entrepreneurship", "actuarial", "economics", "bba"],
        "cluster": "Cluster 19–21",
        "min_grade": "C+",
        "example_jobs": "Accountant, CEO, Financial Analyst, Marketer, Entrepreneur"
    },
    "education": {
        "keywords": ["education", "teaching", "ecde", "special education", "bed arts", "bed science", "pte"],
        "cluster": "Cluster 22–23",
        "min_grade": "C+",
        "example_jobs": "Teacher, Lecturer, Principal, Education Officer"
    },
    "architecture": {
        "keywords": ["architecture", "architectural", "interior design", "landscape", "urban planning", "quantity surveying"],
        "cluster": "Cluster 6",
        "min_grade": "B",
        "example_jobs": "Architect, Interior Designer, Urban Planner"
    },
    "agriculture": {
        "keywords": ["agriculture", "horticulture", "agribusiness", "animal health", "veterinary", "food science", "agricultural engineering", "agricultural education"],
        "cluster": "Cluster 24–25",
        "min_grade": "C",
        "example_jobs": "Agricultural Officer, Veterinarian, Agribusiness Manager"
    },
    "arts": {
        "keywords": ["journalism", "communication", "film", "music", "performing arts", "graphic design", "fashion", "linguistics", "design", "media"],
        "cluster": "Cluster 26–27",
        "min_grade": "C",
        "example_jobs": "Journalist, Graphic Designer, PR Specialist, Filmmaker"
    },
    "hospitality": {
        "keywords": ["hospitality", "hotel", "tourism", "culinary", "event management", "food service"],
        "cluster": "Cluster 28",
        "min_grade": "C-",
        "example_jobs": "Hotel Manager, Chef, Event Planner, Tourism Officer"
    },
    "environmental science": {
        "keywords": ["environmental", "forestry", "wildlife", "conservation", "climate", "waste management"],
        "cluster": "Cluster 13–14",
        "min_grade": "C+",
        "example_jobs": "Environmental Scientist, Forester, Conservationist"
    }
}


def predict_best_field(points: int) -> str:
    if points >= 77: return "medicine"
    if points >= 70: return "engineering"
    if points >= 63: return "law"
    if points >= 56: return "computer science"
    if points >= 49: return "business"
    if points >= 42: return "education"
    if points >= 35: return "agriculture"
    if points >= 28: return "hospitality"
    if points >= 21: return "arts"
    return "environmental science"  

@lru_cache(maxsize=4096)
def recommend_careers(grade: str = None, field: str = None, level: str = "Degree") -> dict:
    global df
    if df.empty or grade is None:
        return {"success": False, "error": "System not ready or grade missing"}

    points = grade_to_points(grade)
    if points == 0:
        return {"success": False, "error": "Invalid KCSE grade"}

    data = df.copy()
    data['cutoff_points'] = pd.to_numeric(data['cutoff_points'], errors='coerce').fillna(999)
    data['cost'] = pd.to_numeric(data['cost'], errors='coerce').fillna(0).astype(int)

    
    if not field or field.lower() in ["any", "let ai predict", "let ai choose", "none", ""]:
        field = predict_best_field(points)

    field_key = field.lower().strip()
    if field_key not in FIELD_TAXONOMY:
        return {"success": False, "error": f"Field '{field}' not supported yet."}

    field_info = FIELD_TAXONOMY[field_key]
    keywords = field_info["keywords"]

    
    level_lower = level.lower()
    if "degree" in level_lower or "bachelor" in level_lower:
        level_filter = data['program_type'].str.contains(r"\bdegree\b|\bbachelor\b", case=False, na=False, regex=True)
    elif "diploma" in level_lower:
        level_filter = data['program_type'].str.contains(r"\bdiploma\b", case=False, na=False, regex=True)
    else:
        level_filter = data['program_type'].str.contains(r"\bcertificate\b|\bcert\b", case=False, na=False, regex=True)

    
    pattern = '|'.join([f"\\b{re.escape(k)}\\b" for k in keywords])
    matched = data[
        level_filter &
        data['program_name'].str.contains(pattern, case=False, na=False, regex=True)
    ].copy()

    if matched.empty:
        return {
            "success": True,
            "public": [],
            "private": [],
            "note": f"No {field.title()} programs found at {level} level. Try Diploma/Certificate or another field."
        }

    
    matched['is_public'] = matched['university'].str.contains(PUBLIC_PATTERN, case=False, na=False, regex=True)

    
    public = matched[
        matched['is_public'] & 
        (matched['cutoff_points'] <= points + 3)
    ]
    private = matched[~matched['is_public']]

    
    def score_row(row):
        score = 0
        reasons = []
        if row['helb_eligibility'] == 'Yes':
            score += 35
            reasons.append("HELB eligible")
        if row['is_public']:
            score += 30
            reasons.append("Public university")
        if row['cost'] <= 150000:
            score += 20
            reasons.append("Affordable cost")
        if row['is_public'] and row['cutoff_points'] <= points:
            score += 15
            reasons.append("You meet the cutoff")
        return score, ", ".join(reasons)

    
    public[['score', 'reason']] = public.apply(score_row, axis=1, result_type='expand')
    public = public.sort_values('score', ascending=False).head(10)
    
    private[['score', 'reason']] = private.apply(score_row, axis=1, result_type='expand')
    private = private.sort_values('score', ascending=False).head(10)

    def format_course(row):
        base = {
            "university": row['university'],
            "program_name": row['program_name'],
            "program_type": row['program_type'],
            "cost": f"KSh {row['cost']:,}",
            "helb": row['helb_eligibility'],
            "type": "Public University" if row['is_public'] else "Private University",
            "match": "Perfect Match" if row['score'] >= 80 else "Very Strong" if row['score'] >= 65 else "Good Fit",
            "reason": row['reason'] or "Strong overall match based on your profile"
        }
        if row['is_public'] and row['cutoff_points'] < 999:
            base["cutoff_points"] = f"{row['cutoff_points']:.1f}"
        return base

    return {
        "success": True,
        "field": field.title(),
        "grade_points": points,
        "recommended_for_you": field_info["example_jobs"],
        "public": [format_course(r) for _, r in public.iterrows()],
        "private": [format_course(r) for _, r in private.iterrows()],
        "total_options": len(public) + len(private),
        "note": "Only 100% relevant programs shown • Public unis = HELB eligible • Data: KUCCPS 2025 trends"
    }