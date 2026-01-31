# Test Input Examples for Crowd Level Predictions

Use these example inputs to test different crowd level predictions in your web application.

## 🟢 LOW Crowd Level Examples

### Example 1: Early Morning Cardio
- **Machine Name:** Elliptical
- **Workout Day:** Tuesday
- **Workout Plan:** Cardio
- **Muscle Group:** Legs
- **Start Hour:** 6 (6:00 AM)
- **Duration:** 30 minutes

### Example 2: Mid-Morning Less Popular Machine
- **Machine Name:** Rowing Machine
- **Workout Day:** Wednesday
- **Workout Plan:** Endurance
- **Muscle Group:** Full Body
- **Start Hour:** 10 (10:00 AM)
- **Duration:** 20 minutes

### Example 3: Early Afternoon Weekday
- **Machine Name:** Stationary Bike
- **Workout Day:** Thursday
- **Workout Plan:** Cardio
- **Muscle Group:** Legs
- **Start Hour:** 14 (2:00 PM)
- **Duration:** 25 minutes

---

## 🟡 MEDIUM Crowd Level Examples

### Example 1: Midday Popular Machine
- **Machine Name:** Treadmill
- **Workout Day:** Monday
- **Workout Plan:** Cardio
- **Muscle Group:** Legs
- **Start Hour:** 12 (12:00 PM / Noon)
- **Duration:** 30 minutes

### Example 2: Afternoon Strength Training
- **Machine Name:** Bench Press
- **Workout Day:** Wednesday
- **Workout Plan:** Strength
- **Muscle Group:** Chest
- **Start Hour:** 15 (3:00 PM)
- **Duration:** 45 minutes

### Example 3: Late Morning Moderate
- **Machine Name:** Cable Machine
- **Workout Day:** Friday
- **Workout Plan:** Strength
- **Muscle Group:** Arms
- **Start Hour:** 11 (11:00 AM)
- **Duration:** 40 minutes

---

## 🔴 HIGH Crowd Level Examples

### Example 1: Evening Peak Hour (Most Common)
- **Machine Name:** Treadmill
- **Workout Day:** Monday
- **Workout Plan:** Cardio
- **Muscle Group:** Legs
- **Start Hour:** 18 (6:00 PM)
- **Duration:** 30 minutes

### Example 2: Weekend Evening
- **Machine Name:** Bench Press
- **Workout Day:** Saturday
- **Workout Plan:** Strength
- **Muscle Group:** Chest
- **Start Hour:** 19 (7:00 PM)
- **Duration:** 45 minutes

### Example 3: Friday Evening
- **Machine Name:** Treadmill
- **Workout Day:** Friday
- **Workout Plan:** Cardio
- **Muscle Group:** Legs
- **Start Hour:** 17 (5:00 PM)
- **Duration:** 30 minutes

---

## 📝 Quick Reference

### Patterns for LOW Crowd:
- ⏰ Early morning hours (6-8 AM)
- ⏰ Mid-afternoon (2-3 PM)
- 🏋️ Less popular machines (Rowing Machine, Stationary Bike, Elliptical)
- 📅 Weekdays (Tuesday-Thursday)

### Patterns for MEDIUM Crowd:
- ⏰ Midday hours (11 AM - 3 PM)
- 🏋️ Moderate popularity machines
- 📅 Weekdays

### Patterns for HIGH Crowd:
- ⏰ Evening peak hours (5-8 PM)
- ⏰ Weekend afternoons/evenings
- 🏋️ Popular machines (Treadmill, Bench Press)
- 📅 Monday evenings, Friday evenings, Weekends

---

## 🧪 Testing Instructions

1. Open your web application: `http://localhost:5000`
2. Select an example from above
3. Fill in the form with the example values
4. Click "Get Prediction"
5. Check if the predicted crowd level matches the expected level

**Note:** If all predictions show "High" regardless of input, there may be:
- Model bias (imbalanced training data)
- Feature encoding issue
- Model needs retraining with balanced data

---

## 🔍 Troubleshooting

If you're getting "High" for all inputs:

1. **Check the model training data balance:**
   ```python
   python check_model_bias.py
   ```

2. **Retrain the model with class balancing:**
   - Modify `train_model.py` to use `class_weight='balanced'` in RandomForestClassifier
   - Retrain: `python train_model.py`

3. **Check console output** when making predictions - it shows:
   - Prediction probabilities
   - Feature encoding details
   - Any warnings about missing categories
