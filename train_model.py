"""
Gym Equipment Usage Prediction - Final Model Training Script
------------------------------------------------------------
Predicts crowd level (Low / Medium / High) for gym machines.

This model is optimized to avoid overfitting and is ready
for FastAPI integration.

Author: Final Year Project
"""

import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

import os

MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)
# =========================
# 1. LOAD DATA
# =========================
df = pd.read_excel("gym_machine_usage_10000_balanced.xlsx")

# Convert time
df['start_time'] = pd.to_datetime(df['start_time'], format='%I:%M %p')
df['start_hour'] = df['start_time'].dt.hour

# Convert date → day number
df['date'] = pd.to_datetime(df['date'])
df['day_of_week_num'] = df['date'].dt.dayofweek

# =========================
# 2. FEATURE SELECTION
# =========================
categorical_cols = [
    'workout_plan',
    'workout_day',
    'muscle_group',
    'machine_name'
]

numerical_cols = [
    'start_hour',
    'duration_min',
    'day_of_week_num'
]

X_cat = df[categorical_cols]
X_num = df[numerical_cols]

y = df['crowd_level']


# =========================
# 3. ENCODING
# =========================
onehot_encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)

X_cat_encoded = onehot_encoder.fit_transform(X_cat)

label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

X_cat_df = pd.DataFrame(
    X_cat_encoded,
    columns=onehot_encoder.get_feature_names_out(categorical_cols)
)

X_final = pd.concat([X_num.reset_index(drop=True), X_cat_df], axis=1)


# =========================
# 4. TRAIN-TEST SPLIT
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X_final,
    y_encoded,
    test_size=0.2,
    random_state=42,
    stratify=y_encoded
)


# =========================
# 5. MODEL TRAINING (ANTI-OVERFITTING)
# =========================
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=15,
    min_samples_leaf=5,
    min_samples_split=10,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)


# =========================
# 6. EVALUATION
# =========================
y_pred = model.predict(X_test)

print("\nAccuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))


# =========================
# 7. SAVE MODEL & ENCODERS
# =========================
joblib.dump(model, os.path.join(MODEL_DIR, "gym_model.pkl"))
joblib.dump(onehot_encoder, os.path.join(MODEL_DIR, "onehot_encoder.pkl"))
joblib.dump(label_encoder, os.path.join(MODEL_DIR, "label_encoder.pkl"))
joblib.dump(X_final.columns.tolist(), os.path.join(MODEL_DIR, "feature_columns.pkl"))
joblib.dump(categorical_cols, os.path.join(MODEL_DIR, "categorical_cols.pkl"))
joblib.dump(numerical_cols, os.path.join(MODEL_DIR, "numerical_cols.pkl"))

print("\n✅ Model training complete.")
print("✅ Files saved:")
print("   - gym_model.joblib")
print("   - onehot_encoder.joblib")
print("   - label_encoder.joblib")
print("   - feature_columns.joblib")
