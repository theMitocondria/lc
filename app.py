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

async def save_contest_with_Cheaters(contest):
    cheaters = await giveMeCheaters()
    # print(cheaters[2])
    contest.question3 = cheaters[0]
    contest.question4 = cheaters[2]
    contest.save()

    print('hihih')
    
    def fill(cheater):
        for curr in  range(0,len(cheater)) :
            solution = Solution(contestId = contest.name , rank = cheater[curr]['rank']  , solution = cheater[curr]['solution'])
            solution.save()
    
    fill(cheaters[3])
    fill(cheaters[1])

@app.route('/contest/create', methods=['POST'])
def contest_creation():
    try:
        data = request.get_json()
        contest_name = data.get('name')
        contest = Contest(name=contest_name)
        
        # Save the contest immediately
        contest.save()
      
        # Run the async task in a separate thread
        threading.Thread(target=lambda: asyncio.run(save_contest_with_Cheaters(contest))).start()

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

@app.route('/solution/all', methods=['GET'])
def get_all_solutions():
    try:
        contests = Solution.objects().to_json()  # Fetch all contests from MongoDB
        return contests, 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == "__main__":
    port = os.getenv("PORT", 5000)
    app.run(port=port)
