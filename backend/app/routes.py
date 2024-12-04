from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import numpy as np
import pandas as pd
import joblib
import os
from lightgbm import Booster

app = Flask(
    __name__, 
    static_folder='../../frontend/static', 
    template_folder='../../frontend/templates'
)

CORS(app)

# Get the absolute path to the model
model_path = os.path.join(os.path.dirname(__file__), "../../model/lightgbm_model.pkl")
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
        return render_template('form.html')
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
    data = request.json
    return jsonify({"prediction": "This is a prediction."})

if __name__ == '__main__':
    app.run(debug=True)

