// API Base URL
const API_BASE_URL = '/api';

// DOM Elements
const form = document.getElementById('predictionForm');
const predictBtn = document.getElementById('predictBtn');
const btnText = document.getElementById('btnText');
const btnLoader = document.getElementById('btnLoader');
const resultBox = document.getElementById('result');
const errorBox = document.getElementById('error');
const crowdLevelSpan = document.getElementById('crowdLevel');
const suggestionSpan = document.getElementById('suggestion');
const errorMessage = document.getElementById('errorMessage');

// Form submission handler
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Hide previous results/errors
    resultBox.style.display = 'none';
    errorBox.style.display = 'none';
    
    // Get form data
    const formData = {
        machine_name: document.getElementById('machine_name').value,
        workout_day: document.getElementById('workout_day').value,
        workout_plan: document.getElementById('workout_plan').value,
        muscle_group: document.getElementById('muscle_group').value,
        start_hour: parseInt(document.getElementById('start_hour').value),
        duration_min: parseInt(document.getElementById('duration_min').value)
    };
    
    // Validate form data
    if (!validateForm(formData)) {
        return;
    }
    
    // Show loading state
    setLoading(true);
    
    try {
        // Make API request
        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Display result
            displayResult(data.crowd_level, data.suggestion);
        } else {
            // Display error
            displayError(data.error || 'Prediction failed. Please try again.');
        }
    } catch (error) {
        console.error('Error:', error);
        displayError('Network error. Please check if the server is running.');
    } finally {
        setLoading(false);
    }
});

// Validate form data
function validateForm(data) {
    if (!data.machine_name) {
        displayError('Machine name is required.');
        return false;
    }
    
    if (!data.workout_day) {
        displayError('Workout day is required.');
        return false;
    }
    
    if (!data.workout_plan) {
        displayError('Workout plan is required.');
        return false;
    }
    
    if (!data.muscle_group) {
        displayError('Muscle group is required.');
        return false;
    }
    
    if (isNaN(data.start_hour) || data.start_hour < 0 || data.start_hour > 23) {
        displayError('Start hour must be between 0 and 23.');
        return false;
    }
    
    if (isNaN(data.duration_min) || data.duration_min < 1 || data.duration_min > 300) {
        displayError('Duration must be between 1 and 300 minutes.');
        return false;
    }
    
    return true;
}

// Display prediction result
function displayResult(crowdLevel, suggestion) {
    crowdLevelSpan.textContent = crowdLevel;
    crowdLevelSpan.className = `crowd-level ${crowdLevel}`;
    suggestionSpan.textContent = suggestion;
    
    resultBox.style.display = 'block';
    resultBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Display error message
function displayError(message) {
    errorMessage.textContent = message;
    errorBox.style.display = 'block';
    errorBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Set loading state
function setLoading(loading) {
    if (loading) {
        predictBtn.disabled = true;
        btnText.style.display = 'none';
        btnLoader.style.display = 'block';
    } else {
        predictBtn.disabled = false;
        btnText.style.display = 'block';
        btnLoader.style.display = 'none';
    }
}

// Load dropdown options on page load
async function loadOptions() {
    try {
        const response = await fetch(`${API_BASE_URL}/options`);
        const data = await response.json();
        
        if (data.success) {
            // Populate machine name dropdown
            const machineSelect = document.getElementById('machine_name');
            data.machines.forEach(machine => {
                const option = document.createElement('option');
                option.value = machine;
                option.textContent = machine;
                machineSelect.appendChild(option);
            });
            
            // Populate workout plan dropdown
            const workoutPlanSelect = document.getElementById('workout_plan');
            data.workout_plans.forEach(plan => {
                const option = document.createElement('option');
                option.value = plan;
                option.textContent = plan;
                workoutPlanSelect.appendChild(option);
            });
            
            // Populate muscle group dropdown
            const muscleGroupSelect = document.getElementById('muscle_group');
            data.muscle_groups.forEach(group => {
                const option = document.createElement('option');
                option.value = group;
                option.textContent = group;
                muscleGroupSelect.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error loading options:', error);
        // Options will remain empty, user can still type if needed
    }
}

// Check API health and load options on page load
window.addEventListener('DOMContentLoaded', async () => {
    // Load dropdown options
    await loadOptions();
    
    // Check API health
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();
        
        if (!data.model_loaded) {
            displayError('Warning: Model not loaded. Please ensure the model is trained.');
        }
    } catch (error) {
        console.error('Health check failed:', error);
        displayError('Warning: Unable to connect to server. Please ensure Flask is running.');
    }
});
