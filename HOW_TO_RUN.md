# How to Run the Gym Equipment Usage Prediction System

## Quick Start Guide

### Step 1: Install Dependencies

Make sure you have Python 3.8+ installed, then install required packages:

```bash
pip install pandas scikit-learn joblib openpyxl
```

Or if you have a `requirements.txt`:
```bash
pip install -r requirements.txt
```

### Step 2: Train the Model

Run the training script:

```bash
python train_model.py
```

**What this does:**
- Loads the Excel dataset (`gym_machine_usage_10000_balanced.xlsx`)
- Preprocesses the data (extracts hour, day of week)
- Trains a RandomForestClassifier
- Saves the model and encoders to the `models/` folder

**Expected output:**
- Accuracy score
- Classification report
- Model files saved in `models/` directory:
  - `gym_model.pkl`
  - `onehot_encoder.pkl`
  - `label_encoder.pkl`
  - `feature_columns.pkl`

### Step 3: Verify Model Files

Check that the `models/` folder contains:
```
models/
├── gym_model.pkl
├── onehot_encoder.pkl
├── label_encoder.pkl
└── feature_columns.pkl
```

## Troubleshooting

### Error: `sparse` parameter not found

**Problem:** You're using an older version of scikit-learn that uses `sparse` instead of `sparse_output`.

**Solution:** Update scikit-learn:
```bash
pip install --upgrade scikit-learn
```

Or if the code shows `sparse_output=False` (which is correct for newer versions), make sure your scikit-learn is up to date:
```bash
pip install scikit-learn>=1.2.0
```

### Error: File not found

**Problem:** The Excel file `gym_machine_usage_10000_balanced.xlsx` is not in the current directory.

**Solution:** Make sure the Excel file is in the same folder as `train_model.py`, or update the path in the script.

### Error: Module not found

**Problem:** Missing Python packages.

**Solution:** Install all dependencies:
```bash
pip install pandas scikit-learn joblib openpyxl
```

## Running in Virtual Environment (Recommended)

1. Create virtual environment:
```bash
python -m venv venv
```

2. Activate it:
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **Linux/Mac:**
     ```bash
     source venv/bin/activate
     ```

3. Install dependencies:
```bash
pip install pandas scikit-learn joblib openpyxl
```

4. Run training:
```bash
python train_model.py
```

## What Happens After Training?

Once training is complete, you'll have:
- ✅ Trained ML model ready for predictions
- ✅ Encoders for preprocessing new data
- ✅ Feature column names for consistency

You can then use these model files in your application or API to make predictions!
