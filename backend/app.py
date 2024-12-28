from flask import Flask, request
from utils.parser import parse_poker_log
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])  # Allow requests from React app


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    hands = parse_poker_log(file)
    return {"hands": hands}

if __name__ == '__main__':
    app.run(debug=True)
