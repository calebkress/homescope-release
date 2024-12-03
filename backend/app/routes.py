from flask import Flask, request, jsonify, render_template

app = Flask(__name__, static_folder='frontend/static', template_folder='frontend/templates')

# homempage render route
@app.route('/')
def home():
    return render_template('index.html')

# prediction form render route
@app.route('/form')
def form_page():
    return render_template('form.html')

# api status route
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"})

# prediction api route
@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.json
    return jsonify({"prediction": "This is a prediction."})

if __name__ == '__main__':
    app.run(debug=True)
