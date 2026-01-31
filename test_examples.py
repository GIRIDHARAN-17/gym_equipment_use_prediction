"""
Example inputs for testing different crowd level predictions.

These examples are based on typical gym usage patterns:
- Low: Early morning, less popular machines, weekdays
- Medium: Midday, moderate times, less popular equipment
- High: Evening peak hours, popular machines, weekends
"""

# Example inputs that should predict LOW crowd level
LOW_EXAMPLES = [
    {
        "name": "Early Morning Cardio (Low)",
        "machine_name": "Elliptical",
        "workout_day": "Tuesday",
        "workout_plan": "Cardio",
        "muscle_group": "Legs",
        "start_hour": 6,  # Very early morning
        "duration_min": 30
    },
    {
        "name": "Mid-Morning Less Popular Machine (Low)",
        "machine_name": "Rowing Machine",
        "workout_day": "Wednesday",
        "workout_plan": "Endurance",
        "muscle_group": "Full Body",
        "start_hour": 10,  # Mid-morning
        "duration_min": 20
    },
    {
        "name": "Early Afternoon Weekday (Low)",
        "machine_name": "Stationary Bike",
        "workout_day": "Thursday",
        "workout_plan": "Cardio",
        "muscle_group": "Legs",
        "start_hour": 14,  # 2 PM
        "duration_min": 25
    }
]

# Example inputs that should predict MEDIUM crowd level
MEDIUM_EXAMPLES = [
    {
        "name": "Midday Popular Machine (Medium)",
        "machine_name": "Treadmill",
        "workout_day": "Monday",
        "workout_plan": "Cardio",
        "muscle_group": "Legs",
        "start_hour": 12,  # Noon
        "duration_min": 30
    },
    {
        "name": "Afternoon Strength Training (Medium)",
        "machine_name": "Bench Press",
        "workout_day": "Wednesday",
        "workout_plan": "Strength",
        "muscle_group": "Chest",
        "start_hour": 15,  # 3 PM
        "duration_min": 45
    },
    {
        "name": "Late Morning Moderate (Medium)",
        "machine_name": "Cable Machine",
        "workout_day": "Friday",
        "workout_plan": "Strength",
        "muscle_group": "Arms",
        "start_hour": 11,  # 11 AM
        "duration_min": 40
    }
]

# Example inputs that should predict HIGH crowd level
HIGH_EXAMPLES = [
    {
        "name": "Evening Peak Hour Popular Machine (High)",
        "machine_name": "Treadmill",
        "workout_day": "Monday",
        "workout_plan": "Cardio",
        "muscle_group": "Legs",
        "start_hour": 18,  # 6 PM - peak hour
        "duration_min": 30
    },
    {
        "name": "Weekend Evening (High)",
        "machine_name": "Bench Press",
        "workout_day": "Saturday",
        "workout_plan": "Strength",
        "muscle_group": "Chest",
        "start_hour": 19,  # 7 PM
        "duration_min": 45
    },
    {
        "name": "Friday Evening Popular Equipment (High)",
        "machine_name": "Treadmill",
        "workout_day": "Friday",
        "workout_plan": "Cardio",
        "muscle_group": "Legs",
        "start_hour": 17,  # 5 PM
        "duration_min": 30
    }
]

def print_examples():
    """Print all example inputs in a formatted way."""
    print("=" * 80)
    print("EXAMPLE INPUTS FOR TESTING CROWD LEVEL PREDICTIONS")
    print("=" * 80)
    
    print("\n" + "=" * 80)
    print("LOW CROWD LEVEL EXAMPLES (Expected: Low)")
    print("=" * 80)
    for i, example in enumerate(LOW_EXAMPLES, 1):
        print(f"\n{i}. {example['name']}")
        print(f"   Machine: {example['machine_name']}")
        print(f"   Day: {example['workout_day']}")
        print(f"   Plan: {example['workout_plan']}")
        print(f"   Muscle Group: {example['muscle_group']}")
        print(f"   Hour: {example['start_hour']}:00")
        print(f"   Duration: {example['duration_min']} minutes")
    
    print("\n" + "=" * 80)
    print("MEDIUM CROWD LEVEL EXAMPLES (Expected: Medium)")
    print("=" * 80)
    for i, example in enumerate(MEDIUM_EXAMPLES, 1):
        print(f"\n{i}. {example['name']}")
        print(f"   Machine: {example['machine_name']}")
        print(f"   Day: {example['workout_day']}")
        print(f"   Plan: {example['workout_plan']}")
        print(f"   Muscle Group: {example['muscle_group']}")
        print(f"   Hour: {example['start_hour']}:00")
        print(f"   Duration: {example['duration_min']} minutes")
    
    print("\n" + "=" * 80)
    print("HIGH CROWD LEVEL EXAMPLES (Expected: High)")
    print("=" * 80)
    for i, example in enumerate(HIGH_EXAMPLES, 1):
        print(f"\n{i}. {example['name']}")
        print(f"   Machine: {example['machine_name']}")
        print(f"   Day: {example['workout_day']}")
        print(f"   Plan: {example['workout_plan']}")
        print(f"   Muscle Group: {example['muscle_group']}")
        print(f"   Hour: {example['start_hour']}:00")
        print(f"   Duration: {example['duration_min']} minutes")
    
    print("\n" + "=" * 80)
    print("HOW TO USE:")
    print("=" * 80)
    print("1. Copy the values from any example above")
    print("2. Enter them in the web form at http://localhost:5000")
    print("3. Click 'Get Prediction' to see the crowd level")
    print("\nNote: Actual predictions depend on your trained model.")
    print("If all predictions are 'High', there may be a model bias issue.")
    print("=" * 80)

if __name__ == "__main__":
    print_examples()
