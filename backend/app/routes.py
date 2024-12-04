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

# prediction routes
@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        form_data = request.json  
        # extract features
        zipcode = int(form_data.get("zipCode", 0))
        latitude = float(form_data.get("latitude", 0.0))
        longitude = float(form_data.get("longitude", 0.0))
        garage_spaces = int(form_data.get("garageSpaces", 0))
        has_hoa = 1 if form_data.get("hasHoa", "").lower() == "yes" else 0
        year_built = int(form_data.get("yearBuilt", 0))
        appliances = int(form_data.get("appliances", 0))
        lot_size = int(form_data.get("lotSize", 0))
        house_size = int(form_data.get("houseSize", 0))
        bathrooms = float(form_data.get("bathrooms", 0.0))
        bedrooms = int(form_data.get("bedrooms", 0))
        num_stories = int(form_data.get("numStories", 0))
        patios_porches = int(form_data.get("patiosPorches", 0))

        # derived features
        price_per_sqft = house_size / lot_size if lot_size > 0 else 0
        bath_bed_ratio = bathrooms / bedrooms if bedrooms > 0 else 0
        lot_living_ratio = lot_size / house_size if house_size > 0 else 0
        garage_bed_ratio = garage_spaces / bedrooms if bedrooms > 0 else 0
        lat_lon_interaction = latitude * longitude

        # create input for model
        model_input = pd.DataFrame([{
            "zipcode": zipcode,
            "latitude": latitude,
            "longitude": longitude,
            "garageSpaces": garage_spaces,
            "hasAssociation": has_hoa,
            "yearBuilt": year_built,
            "numOfAppliances": appliances,
            "numOfParkingFeatures": garage_spaces,  
            "numOfPatioAndPorchFeatures": patios_porches,
            "lotSizeSqFt": lot_size,
            "livingAreaSqFt": house_size,
            "numOfBathrooms": bathrooms,
            "numOfBedrooms": bedrooms,
            "numOfStories": num_stories,
            "PricePerSqFt": price_per_sqft,
            "BathBedRatio": bath_bed_ratio,
            "LotLivingRatio": lot_living_ratio,
            "GarageBedRatio": garage_bed_ratio,
            "LatLonInteraction": lat_lon_interaction
        }])

        input_df = pd.DataFrame([model_input])
        print(input_df)

        # Make prediction
        prediction = model.predict(model_input)[0]

        # Return response
        return jsonify({"prediction": round(prediction, 2)})

    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({"error": "An error occurred while processing your request."}), 500

if __name__ == '__main__':
    app.run(debug=True)

