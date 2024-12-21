// Show Login and Signup Page functions
function showSignup() {
    document.getElementById('login-page').classList.remove('active');
    document.getElementById('signup-page').classList.add('active');
}

function showLogin() {
    document.getElementById('signup-page').classList.remove('active');
    document.getElementById('login-page').classList.add('active');
}

// Function to send data to the Flask backend and fetch prediction
async function predictCharge() {
    // Get input values from the form
    const age = document.getElementById('age').value.trim();
    const bmi = document.getElementById('bmi').value.trim();
    const sex = document.getElementById('sex').value.trim();
    const smoker = document.getElementById('smoker').value.trim();
    const region = document.getElementById('region').value.trim();
    const children = document.getElementById('children').value.trim();

    // Basic input validation
    if (!age || !bmi || !sex || !smoker || !region || !children) {
        displayResult('Please fill in all fields before submitting.', true);
        return;
    }

    // Prepare payload for Flask API
    const data = {
        age: parseInt(age, 10),
        bmi: parseFloat(bmi),
        sex: sex.toLowerCase().trim(), // Standardize case for backend consistency
        smoker: smoker.toLowerCase().trim(),
        region: region.toLowerCase().trim(),
        children: parseInt(children, 10),
    };

    try {
        // Call Flask backend API
        const response = await fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        // Check response status
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Unknown error occurred.');
        }

        const result = await response.json();

        // Display prediction
        if (result.prediction !== undefined) {
            displayResult(`Predicted Premium: <strong>${result.prediction.toFixed(2)}</strong>`, false);
        } else {
            displayResult('No prediction returned by server.', true);
        }
    } catch (error) {
        displayResult(`Error in predicting premium: ${error.message}`, true);
        console.error('Error:', error);
    }
}

// Function to display result or error messages
function displayResult(message, isError = false) {
    const resultElement = document.getElementById('result');
    resultElement.innerHTML = `<p class="${isError ? 'error' : 'success'}">${message}</p>`;
    resultElement.style.display = 'block'; // Ensure the result is visible
}

// Handle navigation after login or signup
document.getElementById('loginForm').onsubmit = function (event) {
    event.preventDefault();
    navigateToPredictionPage();
};

document.getElementById('signupForm').onsubmit = function (event) {
    event.preventDefault();
    navigateToPredictionPage();
};

// Function to navigate to the prediction page
function navigateToPredictionPage() {
    document.getElementById('login-page').classList.remove('active');
    document.getElementById('signup-page').classList.remove('active');
    document.getElementById('prediction-page').classList.add('active');
}

// Move cat with pointer
document.addEventListener('mousemove', function (e) {
    const cat = document.getElementById('cat');
    cat.style.left = `${e.pageX}px`;
    cat.style.top = `${e.pageY}px`;
});
