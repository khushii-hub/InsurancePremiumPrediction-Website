import requests

# URL of the Flask app
url = "http://127.0.0.1:5000/predict"

# Example input data (adjust as per your actual input)
input_data = {
    'age': 30,
    'bmi': 28.5,
    'children': 2,
    'sex': 'female',
    'smoker': 'yes',
    'region': 'southwest'
}

# Send the POST request to the Flask app
response = requests.post(url, json=input_data)

# Check the response content
print("Response Status Code:", response.status_code)
print("Response Text:", response.text)

if response.status_code == 200:
    try:
        print("Prediction:", response.json()['prediction'])
    except ValueError as e:
        print("Failed to decode JSON:", e)
else:
    print(f"Error {response.status_code}: {response.text}")
