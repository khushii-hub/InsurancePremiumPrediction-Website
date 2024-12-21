import logging
from flask import Flask, request, jsonify
import pickle
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),  # Save logs to a file
        logging.StreamHandler()         # Output logs to console
    ]
)

# Load the trained model and preprocessor
logging.info("Loading model and preprocessor...")
try:
    with open('xgb_model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
        logging.info("Model loaded successfully.")
    with open('preprocessor.pkl', 'rb') as preprocessor_file:
        preprocessor = pickle.load(preprocessor_file)
        logging.info("Preprocessor loaded successfully.")
except FileNotFoundError as e:
    logging.critical(f"File not found: {e}")
    raise SystemExit("Required files not found. Ensure 'xgb_model.pkl' and 'preprocessor.pkl' are in the same directory.")
except Exception as e:
    logging.critical(f"Error loading model or preprocessor: {e}")
    raise SystemExit("Failed to load model or preprocessor.")

# Define expected columns
expected_columns = ['age', 'bmi', 'children', 'sex', 'smoker', 'region']

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict insurance charges based on user input.
    """
    try:
        # Parse input JSON
        data = request.json
        logging.info(f"Received data: {data}")

        # Validate input keys
        missing_keys = [key for key in expected_columns if key not in data]
        if missing_keys:
            error_msg = f"Missing input fields: {missing_keys}"
            logging.warning(error_msg)
            return jsonify({"error": error_msg}), 400

        # Convert input to a DataFrame
        input_df = pd.DataFrame([data], columns=expected_columns)
        logging.debug(f"Input data as DataFrame: {input_df}")

        # Transform input data using preprocessor
        transformed_data = preprocessor.transform(input_df)
        logging.debug(f"Transformed data shape: {transformed_data.shape}")

        # Check for feature shape mismatch
        if transformed_data.shape[1] != model.n_features_in_:
            error_msg = f"Feature shape mismatch: expected {model.n_features_in_}, got {transformed_data.shape[1]}"
            logging.error(error_msg)
            return jsonify({"error": error_msg}), 400

        # Make prediction
        prediction = model.predict(transformed_data)
        logging.info(f"Prediction result: {prediction[0]}")

        return jsonify({"prediction": float(prediction[0])})

    except pd.errors.EmptyDataError as e:
        logging.error(f"Input DataFrame error: {e}")
        return jsonify({"error": "Invalid input data."}), 400
    except ValueError as e:
        logging.error(f"Value error during transformation or prediction: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
