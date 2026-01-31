"""
Flask Backend for Gym Equipment Usage Prediction

Loads trained ML model and provides API endpoint for predictions.
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import joblib
import pandas as pd
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env (if present)
load_dotenv()
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Secret key and runtime configuration from environment
app.secret_key = os.getenv("SECRET_KEY", "change-me")
HOST = os.getenv("FLASK_HOST", "0.0.0.0")
PORT = int(os.getenv("FLASK_PORT", 5000))
DEBUG = os.getenv("FLASK_DEBUG", "1") in ("1", "true", "True")

# Model paths (configurable via environment variables)
MODEL_DIR = os.getenv("MODEL_DIR", "models")
MODEL_FILE = os.getenv("MODEL_FILE", "gym_model.pkl")
MODEL_PATH = os.path.join(MODEL_DIR, MODEL_FILE)
ONEHOT_ENCODER_PATH = os.path.join(MODEL_DIR, os.getenv("ONEHOT_ENCODER_FILE", "onehot_encoder.pkl"))
LABEL_ENCODER_PATH = os.path.join(MODEL_DIR, os.getenv("LABEL_ENCODER_FILE", "label_encoder.pkl"))
FEATURE_COLUMNS_PATH = os.path.join(MODEL_DIR, os.getenv("FEATURE_COLUMNS_FILE", "feature_columns.pkl"))
CATEGORICAL_COLS_PATH = os.path.join(MODEL_DIR, os.getenv("CATEGORICAL_COLS_FILE", "categorical_cols.pkl"))
NUMERICAL_COLS_PATH = os.path.join(MODEL_DIR, os.getenv("NUMERICAL_COLS_FILE", "numerical_cols.pkl"))

# Global variables for loaded models
model = None
onehot_encoder = None
label_encoder = None
feature_columns = None
categorical_cols = None
numerical_cols = None


def load_models():
    """Load all trained models and encoders."""
    global model, onehot_encoder, label_encoder, feature_columns, categorical_cols, numerical_cols
    
    try:
        print("Loading models...")
        model = joblib.load(MODEL_PATH)
        onehot_encoder = joblib.load(ONEHOT_ENCODER_PATH)
        label_encoder = joblib.load(LABEL_ENCODER_PATH)
        feature_columns = joblib.load(FEATURE_COLUMNS_PATH)
        categorical_cols = joblib.load(CATEGORICAL_COLS_PATH)
        numerical_cols = joblib.load(NUMERICAL_COLS_PATH)
        print("✅ All models loaded successfully!")
        return True
    except FileNotFoundError as e:
        print(f"❌ Error: Model file not found - {e}")
        print("Please run train_model.py first to train the model.")
        return False
    except Exception as e:
        print(f"❌ Error loading models: {e}")
        return False


def predict_crowd_level(machine_name, workout_day, workout_plan, muscle_group, start_hour, duration_min):
    """
    Make prediction using the loaded model.
    
    Args:
        machine_name: Name of the gym machine
        workout_day: Day of the week (Monday-Sunday)
        workout_plan: Type of workout plan
        muscle_group: Target muscle group
        start_hour: Hour of the day (0-23)
        duration_min: Duration in minutes
    
    Returns:
        dict: Prediction result with crowd_level and suggestion
    """
    try:
        # Convert date to day of week number
        day_mapping = {
            'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3,
            'Friday': 4, 'Saturday': 5, 'Sunday': 6
        }
        day_of_week_num = day_mapping.get(workout_day, 0)
        
        # Prepare categorical features - CRITICAL: Use exact same column order as training
        # Create DataFrame with values in the exact order of categorical_cols
        categorical_values = [workout_plan, workout_day, muscle_group, machine_name]
        categorical_data = pd.DataFrame([categorical_values], columns=categorical_cols)
        
        # Debug: Check if values exist in encoder
        print(f"\n🔍 Categorical Input Check:")
        print(f"   Input values: {dict(zip(categorical_cols, categorical_values))}")
        for idx, col in enumerate(categorical_cols):
            value = categorical_data[col].iloc[0]
            if hasattr(onehot_encoder, 'categories_'):
                # Check if value is in the encoder's known categories
                if idx < len(onehot_encoder.categories_):
                    known_cats = onehot_encoder.categories_[idx]
                    if value not in known_cats:
                        print(f"   ⚠️ WARNING: '{value}' not in {col} categories!")
                        print(f"      Known categories: {list(known_cats)[:10]}...")
                    else:
                        print(f"   ✅ '{value}' found in {col}")
        
        # Encode categorical features
        categorical_encoded = onehot_encoder.transform(categorical_data)
        categorical_df = pd.DataFrame(
            categorical_encoded,
            columns=onehot_encoder.get_feature_names_out(categorical_cols)
        )
        
        # Debug: Check how many features were created
        print(f"   One-hot encoded features: {len(categorical_df.columns)}")
        print(f"   Active features (non-zero): {(categorical_df.iloc[0] != 0).sum()}")
        
        # Prepare numerical features
        numerical_data = pd.DataFrame([{
            'start_hour': start_hour,
            'duration_min': duration_min,
            'day_of_week_num': day_of_week_num
        }])
        
        # Combine features - ensure same order as training (numerical first, then categorical)
        X_final = pd.concat([numerical_data.reset_index(drop=True), categorical_df], axis=1)
        
        # Ensure columns are in the same order as training
        # Check if all required columns exist
        missing_cols = set(feature_columns) - set(X_final.columns)
        if missing_cols:
            print(f"⚠️ Warning: Missing columns: {missing_cols}")
            # Fill missing columns with zeros
            for col in missing_cols:
                X_final[col] = 0
        
        # Reorder columns to match training order exactly
        X_final = X_final.reindex(columns=feature_columns, fill_value=0)
        
        # Debug: Print feature info
        print(f"\n🔍 Feature Debug:")
        print(f"   Numerical features: {numerical_data.to_dict('records')[0]}")
        print(f"   Categorical columns count: {len(categorical_df.columns)}")
        print(f"   Total features: {len(X_final.columns)}")
        print(f"   Expected features: {len(feature_columns)}")
        
        # Make prediction with probabilities for debugging
        prediction_encoded = model.predict(X_final)[0]
        prediction_proba = model.predict_proba(X_final)[0]
        
        # Get label encoder classes to see mapping
        label_classes = label_encoder.classes_
        
        # Debug: Print prediction details
        print(f"\n🔍 Prediction Debug:")
        print(f"   Encoded prediction: {prediction_encoded}")
        print(f"   Label classes: {label_classes}")
        print(f"   Prediction probabilities: {dict(zip(label_classes, prediction_proba))}")
        
        crowd_level = label_encoder.inverse_transform([prediction_encoded])[0]
        
        # Generate suggestion
        suggestions = {
            "Low": "Free now - Machine is available!",
            "Medium": "Moderately busy – try after 15 minutes",
            "High": "Busy – return after 30–45 minutes"
        }
        suggestion = suggestions.get(crowd_level, "Unable to determine availability")
        
        return {
            "success": True,
            "crowd_level": crowd_level,
            "suggestion": suggestion,
            "probabilities": dict(zip(label_classes.tolist(), prediction_proba.tolist()))
        }
    
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"\n❌ Prediction Error: {str(e)}")
        print(f"   Traceback: {error_details}")
        return {
            "success": False,
            "error": str(e)
        }


@app.route('/')
def index():
    """Serve the main prediction page."""
    return render_template('index.html')


@app.route('/api/predict', methods=['POST'])
def predict():
    """
    API endpoint for making predictions.
    
    Expected JSON:
    {
        "machine_name": "Treadmill",
        "workout_day": "Monday",
        "workout_plan": "Cardio",
        "muscle_group": "Legs",
        "start_hour": 18,
        "duration_min": 30
    }
    """
    if model is None:
        return jsonify({
            "success": False,
            "error": "Model not loaded. Please ensure models are trained."
        }), 500
    
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['machine_name', 'workout_day', 'workout_plan', 
                          'muscle_group', 'start_hour', 'duration_min']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "success": False,
                    "error": f"Missing required field: {field}"
                }), 400
        
        # Validate workout_day
        valid_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 
                     'Friday', 'Saturday', 'Sunday']
        if data['workout_day'] not in valid_days:
            return jsonify({
                "success": False,
                "error": f"Invalid workout_day. Must be one of: {valid_days}"
            }), 400
        
        # Validate start_hour
        if not (0 <= data['start_hour'] <= 23):
            return jsonify({
                "success": False,
                "error": "start_hour must be between 0 and 23"
            }), 400
        
        # Validate duration_min
        if not (1 <= data['duration_min'] <= 300):
            return jsonify({
                "success": False,
                "error": "duration_min must be between 1 and 300"
            }), 400
        
        # Make prediction
        result = predict_crowd_level(
            machine_name=data['machine_name'],
            workout_day=data['workout_day'],
            workout_plan=data['workout_plan'],
            muscle_group=data['muscle_group'],
            start_hour=int(data['start_hour']),
            duration_min=int(data['duration_min'])
        )
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 500
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Prediction failed: {str(e)}"
        }), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None,
        "timestamp": datetime.now().isoformat()
    })


@app.route('/api/options', methods=['GET'])
def get_options():
    """
    Get available options for dropdowns from the dataset.
    """
    try:
        # Load dataset to get unique values
        df = pd.read_excel(os.getenv("DATA_FILE", "gym_machine_usage_10000_balanced.xlsx"))
        
        # Get unique values for each category
        machines = sorted(df['machine_name'].unique().tolist())
        workout_plans = sorted(df['workout_plan'].unique().tolist())
        muscle_groups = sorted(df['muscle_group'].unique().tolist())
        
        return jsonify({
            "success": True,
            "machines": machines,
            "workout_plans": workout_plans,
            "muscle_groups": muscle_groups
        })
    except Exception as e:
        # Fallback to common options if dataset can't be loaded
        return jsonify({
            "success": True,
            "machines": [
                "Treadmill", "Elliptical", "Stationary Bike", "Rowing Machine",
                "Bench Press", "Leg Press", "Cable Machine", "Smith Machine",
                "Dumbbells", "Barbell", "Pull-up Bar", "Lat Pulldown",
                "Leg Curl", "Leg Extension", "Chest Press", "Shoulder Press"
            ],
            "workout_plans": [
                "Cardio", "Strength", "Endurance", "Flexibility",
                "HIIT", "Circuit Training", "Powerlifting", "Bodybuilding"
            ],
            "muscle_groups": [
                "Legs", "Chest", "Back", "Arms", "Shoulders",
                "Core", "Full Body", "Cardio", "Glutes", "Biceps", "Triceps"
            ]
        })


if __name__ == '__main__':
    # Load models on startup
    if load_models():
        print(f"\n🚀 Starting Flask server on {HOST}:{PORT} (debug={DEBUG})...")
        print(f"📱 Open http://localhost:{PORT} in your browser")
        app.run(debug=DEBUG, host=HOST, port=PORT)
    else:
        print("\n❌ Failed to load models. Server not started.")
        print("Please run 'python train_model.py' first to train the model.")
