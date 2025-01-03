import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.stats import calculate_player_stats

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
    

@app.route('/files', methods=['GET'])
def get_uploaded_files():
    files = os.listdir(UPLOAD_FOLDER)
    return jsonify(files)


@app.route('/stats', methods=['GET'])
def get_file_stats():
    file_name = request.args.get('file')
    if not file_name:
        return jsonify({'error': 'File name is required'}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file_name)
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404

    try:
        stats = calculate_player_stats(file_path)
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)