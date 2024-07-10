from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from database import connect_database
from models import Contest
from models import Solution
from GiveMeCheaters import giveMeCheaters
import threading
import asyncio

app = Flask(__name__)
load_dotenv()

# Database connection
connect_database()

# Middleware
CORS(app)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Routes

async def save_contest_with_Cheaters(contest, solution):
    cheaters = await giveMeCheaters()
    # print(cheaters[2])
    contest.question3 = cheaters[0]
    contest.question4 = cheaters[2]
    question3Sol = cheaters[1]
    question4sol = cheaters[3]

    


    contest.save()
    print('hihih')

@app.route('/contest/create', methods=['POST'])
def contest_creation():
    try:
        data = request.get_json()
        contest_name = data.get('name')
        contest = Contest(name=contest_name)
        solution = Solution(contestId = contest_name)
        # Save the contest immediately
        contest.save()
        solution.save()
      
        # Run the async task in a separate thread
        threading.Thread(target=lambda: asyncio.run(save_contest_with_Cheaters(contest, solution))).start()

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
