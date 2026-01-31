"""
Quick script to check if the model is biased towards predicting 'High'
"""

import pandas as pd
import joblib
import os

# Load the dataset to check distribution
df = pd.read_excel("gym_machine_usage_10000_balanced.xlsx")

print("=" * 60)
print("DATASET CROWD LEVEL DISTRIBUTION")
print("=" * 60)
print(df['crowd_level'].value_counts())
print(f"\nTotal samples: {len(df)}")
print(f"Distribution percentage:")
print(df['crowd_level'].value_counts(normalize=True) * 100)
print()

# Load label encoder to see class mapping
MODEL_DIR = "models"
label_encoder = joblib.load(os.path.join(MODEL_DIR, "label_encoder.pkl"))

print("=" * 60)
print("LABEL ENCODER MAPPING")
print("=" * 60)
print(f"Classes: {label_encoder.classes_}")
print(f"Class to index mapping:")
for i, cls in enumerate(label_encoder.classes_):
    print(f"  {cls} -> {i}")
print()

# Check if dataset is actually balanced
print("=" * 60)
print("BALANCE CHECK")
print("=" * 60)
counts = df['crowd_level'].value_counts()
if counts.max() / counts.min() > 1.5:
    print("⚠️ Dataset appears imbalanced!")
    print(f"   Max count: {counts.max()}")
    print(f"   Min count: {counts.min()}")
    print(f"   Ratio: {counts.max() / counts.min():.2f}")
else:
    print("✅ Dataset appears balanced")
