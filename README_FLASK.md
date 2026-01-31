# Gym Equipment Usage Prediction - Flask Web Application

A simple web application to predict gym equipment crowd levels using a trained Machine Learning model.

## Features

- 🎯 Simple web interface for predictions
- 🤖 Machine Learning powered predictions
- 📊 Real-time crowd level prediction (Low/Medium/High)
- 💡 Smart suggestions based on predicted crowd level
- 🎨 Modern, responsive UI

## Prerequisites

1. Python 3.8 or higher
2. Trained ML model (run `python train_model.py` first)
3. Model files in the `models/` directory

## Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Train the model (if not already done):**
   ```bash
   python train_model.py
   ```

   This will create model files in the `models/` directory:
   - `gym_model.pkl`
   - `onehot_encoder.pkl`
   - `label_encoder.pkl`
   - `feature_columns.pkl`
   - `categorical_cols.pkl`
   - `numerical_cols.pkl`

## Running the Application

1. **Start the Flask server:**
   ```bash
   python app.py
   ```

2. **Open your browser and navigate to:**
   ```
   http://localhost:5000
   ```

3. **Fill in the form:**
   - Machine Name (e.g., "Treadmill")
   - Workout Day (Monday-Sunday)
   - Workout Plan (e.g., "Cardio")
   - Muscle Group (e.g., "Legs")
   - Start Hour (0-23, where 0=Midnight, 12=Noon, 18=6 PM)
   - Duration in minutes (1-300)

4. **Click "Get Prediction"** to see the crowd level and suggestion!

## Project Structure

```
gym_equipment/
├── app.py                 # Flask backend application
├── train_model.py        # ML model training script
├── models/               # Trained model files (created after training)
│   ├── gym_model.pkl
│   ├── onehot_encoder.pkl
│   ├── label_encoder.pkl
│   ├── feature_columns.pkl
│   ├── categorical_cols.pkl
│   └── numerical_cols.pkl
├── templates/
│   └── index.html        # Frontend HTML
├── static/
│   ├── style.css         # Styling
│   └── script.js         # JavaScript for API calls
└── requirements.txt      # Python dependencies
```

## API Endpoints

### `GET /`
Serves the main prediction page.

### `POST /api/predict`
Makes a prediction based on user input.

**Request Body (JSON):**
```json
{
    "machine_name": "Treadmill",
    "workout_day": "Monday",
    "workout_plan": "Cardio",
    "muscle_group": "Legs",
    "start_hour": 18,
    "duration_min": 30
}
```

**Response (JSON):**
```json
{
    "success": true,
    "crowd_level": "High",
    "suggestion": "Busy – return after 30–45 minutes"
}
```

### `GET /api/health`
Health check endpoint to verify model is loaded.

**Response (JSON):**
```json
{
    "status": "healthy",
    "model_loaded": true,
    "timestamp": "2024-01-01T12:00:00"
}
```

## Troubleshooting

### Model not loaded error

**Problem:** Server starts but model files are not found.

**Solution:**
1. Make sure you've run `python train_model.py` first
2. Check that the `models/` directory exists and contains all `.pkl` files
3. Verify the file paths in `app.py` match your directory structure

### Port already in use

**Problem:** Port 5000 is already in use.

**Solution:** Change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Use different port
```

### CORS errors

**Problem:** CORS errors when making API requests.

**Solution:** The app already includes `flask-cors`. If issues persist, check that `CORS(app)` is enabled in `app.py`.

## Example Predictions

- **Low Crowd:** "Free now - Machine is available!"
- **Medium Crowd:** "Moderately busy – try after 15 minutes"
- **High Crowd:** "Busy – return after 30–45 minutes"

## Development

To run in development mode with auto-reload:
```bash
python app.py
```

The Flask app runs with `debug=True` by default, which enables:
- Auto-reload on code changes
- Detailed error messages
- Debug mode

## Notes

- The model uses RandomForestClassifier for predictions
- Predictions are based on historical gym usage patterns
- All inputs are validated before making predictions
- The frontend uses vanilla JavaScript (no frameworks required)

## License

This project is for educational/academic purposes.
