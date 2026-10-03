
import os
import pandas as pd
import numpy as np
import joblib
import random
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Use native XGBoost for compatibility
import xgboost as xgb

SEED = 42
np.random.seed(SEED)
random.seed(SEED)

DATA_DIR = os.path.dirname(__file__)
ORIGINAL_CSV = os.path.join(DATA_DIR, "final_trained_dataset.csv")
FINAL_CSV    = os.path.join(DATA_DIR, "final_trained_dataset_perfect.csv")
MODEL_PATH   = os.path.join(DATA_DIR, "field_predictor.pkl")
ENCODER_PATH = os.path.join(DATA_DIR, "field_encoder.pkl")

print("XGBoost version:", xgb.__version__)

df = pd.read_csv(ORIGINAL_CSV, low_memory=False)
print(f"Original rows: {len(df)}")
df.columns = [c.strip().lower() for c in df.columns]

keep_cols = [
    'kcse_grade','kcse_mean','predicted_field','program_type','program_name',
    'university','cutoff_points','career_title','is_public',
    'math','english','kisw','physics','chemistry','biology','geography',
    'cre','history','agriculture','business','home_sci','computer',
    'recommended_university','recommended_program_name','recommended_program_type',
    'recommended_career_title','recommended_cutoff_points'
]
df = df[keep_cols].copy()

# cost
cost_map = {
    'public':  {'Degree':120000,'Diploma':80000,'Certificate':45000},
    'private': {'Degree':250000,'Diploma':150000,'Certificate':80000}
}
def get_cost(r):
    typ = 'public' if r['is_public'] else 'private'
    lvl = r['program_type'].split()[0]
    base = cost_map[typ].get(lvl,100000)
    return int(base * random.uniform(0.85,1.15))
df['cost'] = df.apply(get_cost, axis=1)

# helb
df['helb_eligibility'] = np.where(df['is_public'],'Yes','No')

# capacity
capacity_map = {'Degree':200,'Diploma':120,'Certificate':80}
df['capacity'] = df['program_type'].apply(lambda x: capacity_map.get(x.split()[0],100))

# cluster_subjects
cluster_dict = {
    'Bachelor of Science (Civil Engineering)':'MAT A,PHY,CHE,BIO/GROUP III/IV/V',
    'Bachelor of Science (Computer Science)':'MAT A,PHY,Any GROUP III,2nd GROUP II/III/IV/V',
    'Bachelor of Commerce':'ENG/KIS,MAT A/B,Any GROUP II/III,GROUP II/III/IV/V',
    'Bachelor of Laws':'ENG/KIS,MAT A/B,Any GROUP II/III,GROUP II/III/IV/V',
    'BSc Agriculture':'MAT A/B,BIO,CHE,PHY/GROUP III/IV/V',
    'BSc Hospitality Management':'ENG/KIS,MAT A/B,Any GROUP II,GROUP III/IV/V',
    'Diploma in ICT':'MAT A,ENG,Any GROUP II,GROUP III',
    'Certificate in Computer Applications':'ENG,Any GROUP II,Any GROUP III,Any GROUP IV/V'
}
def get_cluster(p):
    for k, v in cluster_dict.items():
        if k.lower() in p.lower(): return v
    return ''
df['cluster_subjects'] = df['program_name'].apply(get_cluster)

# enrich to 10 000 rows
n_needed = 10000 - len(df)
if n_needed > 0:
    synth = df.sample(n=n_needed, replace=True, random_state=SEED).copy()
    num_cols = ['kcse_mean','cutoff_points','cost','capacity',
                'math','english','kisw','physics','chemistry','biology',
                'geography','cre','history','agriculture','business',
                'home_sci','computer']
    for c in num_cols:
        noise = np.random.normal(0,1.5,size=n_needed)
        synth[c] = synth[c].astype(float) + noise
        synth[c] = synth[c].clip(lower=0)
    df = pd.concat([df, synth], ignore_index=True)
print(f"After enrichment → {len(df)} rows")

# prepare features
subject_cols = ['math','english','kisw','physics','chemistry','biology',
                'geography','cre','history','agriculture','business',
                'home_sci','computer']
X = df[subject_cols].fillna(0).astype(float)
y = df['predicted_field']

le = LabelEncoder()
y_enc = le.fit_transform(y)

X_train, X_val, y_train, y_val = train_test_split(
    X, y_enc, test_size=0.2, stratify=y_enc, random_state=SEED
)

# TRAIN with native xgb.train (compatible with your version)
dtrain = xgb.DMatrix(X_train, label=y_train)
dval = xgb.DMatrix(X_val, label=y_val)

params = {
    'max_depth': 7,
    'eta': 0.08,
    'subsample': 0.9,
    'colsample_bytree': 0.9,
    'objective': 'multi:softmax',
    'num_class': len(le.classes_),
    'eval_metric': 'mlogloss'
}

model = xgb.train(
    params,
    dtrain,
    num_boost_round=300,
    evals=[(dval, 'val')],
    early_stopping_rounds=30,
    verbose_eval=False
)

# validation accuracy
y_pred = model.predict(dval).astype(int)
val_acc = (y_pred == y_val).mean()
print(f"Validation accuracy: {val_acc:.4%}")

# save
joblib.dump(model, MODEL_PATH)
joblib.dump(le,   ENCODER_PATH)
print(f"Model saved → {MODEL_PATH}")
print(f"Encoder saved → {ENCODER_PATH}")

# final CSV
final_cols = [
    'kcse_grade','kcse_mean','predicted_field','program_type','program_name',
    'university','cutoff_points','career_title','is_public','cost',
    'helb_eligibility','capacity','cluster_subjects',
    'math','english','kisw','physics','chemistry','biology','geography',
    'cre','history','agriculture','business','home_sci','computer',
    'recommended_university','recommended_program_name','recommended_program_type',
    'recommended_career_title','recommended_cutoff_points'
]
df = df.reindex(columns=final_cols)
df.to_csv(FINAL_CSV, index=False)
print(f"Perfect dataset written → {FINAL_CSV}")