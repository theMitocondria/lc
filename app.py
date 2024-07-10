from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from database import connect_database
from models import Contest
app = Flask(__name__)
load_dotenv()

# Database connection
connect_database()

# Middleware
CORS(app)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Routes
@app.route('/contest/create', methods=['POST'])
def contest_creation():
    try:
        data = request.get_json()
        contest_name = data.get('name')
        contest = Contest(name=contest_name)
        contest.save()

        return jsonify({"message": "Contest created"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/contest/all', methods=['GET'])
def get_all_contests():
    try:
        contests = Contest.objects().to_json()  # Fetch all contests from MongoDB
        return contests, 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = os.getenv("PORT", 5000)
    app.run(port=port)
