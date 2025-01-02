import os
from flask import Flask, request, jsonify
from utils.parser import parse_poker_log
from flask_cors import CORS
from utils.stats import calculate_player_stats  # Assume your script is saved as calculate_player_stats.py

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])  # Allow requests from React app

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the folder exists

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    try:
        # Save the uploaded file temporarily
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # Calculate stats
        stats = calculate_player_stats(file_path)
        return jsonify(stats)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)