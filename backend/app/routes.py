from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import numpy as np
import pandas as pd
import joblib
import os
from lightgbm import Booster
from dotenv import load_dotenv


# Load environment variables from .env
load_dotenv()

# Retrieve API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

print(GOOGLE_API_KEY)

app = Flask(
    __name__, 
    static_folder='../../frontend/static', 
    template_folder='../../frontend/templates'
)

CORS(app)

# Get the absolute path to the model
model_path = os.path.join(os.path.dirname(__file__), "../../model/lightgbm_model.txt")
model_path = os.path.abspath(model_path)

# Load the model
try:
    with open(model_path, "rb") as f:
        model = Booster(model_file=model_path)
except FileNotFoundError as e:
    print(f"Error loading model: {e}")

# homempage render route
@app.route('/')
def home():
    try:
        return render_template('index.html')
    except Exception as e:
        print(f"Error rendering form.html: {e}")
        return f"Error: {e}", 500

# prediction form render route
@app.route('/form')
def form_page():
    try:
        return render_template('form.html', google_api_key=GOOGLE_API_KEY)
    except Exception as e:
        print(f"Error rendering form.html: {e}")
        return f"Error: {e}", 500


# description page render route
@app.route('/description')
def description_page():
    try:
        return render_template('description.html')
    except Exception as e:
        print(f"Error rendering form.html: {e}")
        return f"Error: {e}", 500

# visualizations render route
@app.route('/visualizations')
def visualizations_page():
    try:
        return render_template('visualizations.html')
    except Exception as e:
        print(f"Error rendering form.html: {e}")
        return f"Error: {e}", 500

# api status checker route
@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        return jsonify({"status": "ok"})
    except Exception as e:
        print(f"Error rendering form.html: {e}")
        return f"Error: {e}", 500

# prediction api route
@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        # Parse form data
        form_data = request.json  # Ensure frontend sends JSON via fetch or axios
        address = form_data.get('address', '')
        house_size = int(form_data.get('houseSize', 0))
        lot_size = int(form_data.get('lotSize', 0))
        bedrooms = int(form_data.get('bedrooms', 0))
        bathrooms = int(form_data.get('bathrooms', 0))
        num_stories = int(form_data.get('numStories', 0))
        patios_porches = int(form_data.get('patiosPorches', 0))
        garage_spaces = int(form_data.get('garageSpaces', 0))
        appliances = int(form_data.get('appliances', 0))
        year_built = int(form_data.get('yearBuilt', 0))
        has_hoa = form_data.get('hasHoa', '') == 'yesHoa'  # Convert to boolean
        purchase_year = int(form_data.get('purchaseYear', 0))

        # Check for missing or invalid fields
        if not address or house_size <= 0 or lot_size <= 0 or purchase_year <= 0:
            return jsonify({"error": "Invalid input. Please fill all required fields."}), 400

        # Create input for model
        model_input = {
            "house_size": house_size,
            "lot_size": lot_size,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "num_stories": num_stories,
            "patios_porches": patios_porches,
            "garage_spaces": garage_spaces,
            "appliances": appliances,
            "year_built": year_built,
            "has_hoa": 1 if "Yes" else 0,
            "purchase_year": purchase_year
        }

        # # Convert input to model-compatible format (e.g., Pandas DataFrame or numpy array)
        input_df = pd.DataFrame([model_input])

        # Make prediction
        prediction = model.predict(input_df)[0]  # Assuming model is a LightGBM Booster

        # Return the result
        return jsonify({"prediction": round(prediction, 2), "address": address})
    

    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({"error": "An error occurred while processing your request."}), 500

if __name__ == '__main__':
    app.run(debug=True)

