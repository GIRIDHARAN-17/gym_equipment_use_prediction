"""
Test script to check model predictions and see what's happening.
"""

import joblib
import pandas as pd
import os

# Load models
MODEL_DIR = "models"
model = joblib.load(os.path.join(MODEL_DIR, "gym_model.pkl"))
onehot_encoder = joblib.load(os.path.join(MODEL_DIR, "onehot_encoder.pkl"))
label_encoder = joblib.load(os.path.join(MODEL_DIR, "label_encoder.pkl"))
feature_columns = joblib.load(os.path.join(MODEL_DIR, "feature_columns.pkl"))
categorical_cols = joblib.load(os.path.join(MODEL_DIR, "categorical_cols.pkl"))
numerical_cols = joblib.load(os.path.join(MODEL_DIR, "numerical_cols.pkl"))

print("=" * 60)
print("MODEL INFORMATION")
print("=" * 60)
print(f"Label Encoder Classes: {label_encoder.classes_}")
print(f"Number of classes: {len(label_encoder.classes_)}")
print(f"Categorical columns: {categorical_cols}")
print(f"Numerical columns: {numerical_cols}")
print(f"Total feature columns: {len(feature_columns)}")
print()

# Test with different inputs
test_cases = [
    {
        "name": "Low crowd scenario (early morning, weekday)",
        "machine_name": "Treadmill",
        "workout_day": "Monday",
        "workout_plan": "Cardio",
        "muscle_group": "Legs",
        "start_hour": 6,  # Early morning
        "duration_min": 30
    },
    {
        "name": "Medium crowd scenario (midday)",
        "machine_name": "Bench Press",
        "workout_day": "Wednesday",
        "workout_plan": "Strength",
        "muscle_group": "Chest",
        "start_hour": 12,  # Noon
        "duration_min": 45
    },
    {
        "name": "High crowd scenario (evening peak)",
        "machine_name": "Treadmill",
        "workout_day": "Monday",
        "workout_plan": "Cardio",
        "muscle_group": "Legs",
        "start_hour": 18,  # Evening peak
        "duration_min": 30
    }
]

print("=" * 60)
print("TESTING PREDICTIONS")
print("=" * 60)

for test in test_cases:
    print(f"\n📋 Test: {test['name']}")
    print(f"   Input: {test}")
    
    # Day mapping
    day_mapping = {
        'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3,
        'Friday': 4, 'Saturday': 5, 'Sunday': 6
    }
    day_of_week_num = day_mapping.get(test['workout_day'], 0)
    
    # Prepare categorical features
    categorical_data = pd.DataFrame([{
        'workout_plan': test['workout_plan'],
        'workout_day': test['workout_day'],
        'muscle_group': test['muscle_group'],
        'machine_name': test['machine_name']
    }])
    
    # Encode categorical features
    categorical_encoded = onehot_encoder.transform(categorical_data)
    categorical_df = pd.DataFrame(
        categorical_encoded,
        columns=onehot_encoder.get_feature_names_out(categorical_cols)
    )
    
    # Prepare numerical features
    numerical_data = pd.DataFrame([{
        'start_hour': test['start_hour'],
        'duration_min': test['duration_min'],
        'day_of_week_num': day_of_week_num
    }])
    
    # Combine features
    X_final = pd.concat([numerical_data.reset_index(drop=True), categorical_df], axis=1)
    X_final = X_final[feature_columns]
    
    # Make prediction
    prediction_encoded = model.predict(X_final)[0]
    prediction_proba = model.predict_proba(X_final)[0]
    crowd_level = label_encoder.inverse_transform([prediction_encoded])[0]
    
    print(f"   ✅ Prediction: {crowd_level}")
    print(f"   📊 Probabilities:")
    for label, prob in zip(label_encoder.classes_, prediction_proba):
        print(f"      {label}: {prob:.4f} ({prob*100:.2f}%)")

print("\n" + "=" * 60)
print("If all predictions are 'High', the model may be biased.")
print("Check the training data distribution and model performance.")
print("=" * 60)
