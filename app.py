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
import time

app = Flask(__name__)
load_dotenv()

# Database connection
connect_database()

# Middleware
CORS(app)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Routes

async def add_cheaters_to_contest(contest):
    # Run the main function
    start_time = time.time()
    # asyncio.run(giveMeCheaters())
 

    cheaters = await giveMeCheaters()
    # print(cheaters[2])
    end_time = time.time()
    print("Total Time Taken: ",end_time - start_time)
    # contest = Contest(name=contest_name)
    contest.question3 = contest.question3 + cheaters[0]
    contest.question4 =  contest.question4 + cheaters[2]
    contest.save()

    print('hihih')
    
    def fill(cheater, num):
        for curr in  range(0,len(cheater)) :
            solution = Solution(contestId = contest.name , rank = cheater[curr]['rank'], solution = cheater[curr]['solution'], solutionNumber = num)
            solution.save()
    
    fill(cheaters[3], 4)
    fill(cheaters[1], 3)


@app.route('/contest/addNewCheaters', methods=['POST'])
def add_new_cheaters():
    try:
        data = request.get_json()
        contest_name = data.get('name')

        contest = Contest.objects.get(name = contest_name)
  
        # Run the async task in a separate thread
        threading.Thread(target=lambda: asyncio.run(add_cheaters_to_contest(contest))).start()

        return jsonify({"message": "Contest found"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



async def save_contest_with_Cheaters(contest_name):
    # Run the main function
    start_time = time.time()
    # asyncio.run(giveMeCheaters())
 

    cheaters = await giveMeCheaters()
    # print(cheaters[2])
    end_time = time.time()
    print("Total Time Taken: ",end_time - start_time)
    contest = Contest(name=contest_name)
    contest.question3 = cheaters[0]
    contest.question4 = cheaters[2]
    contest.save()

    print('hihih')
    
    def fill(cheater, num):
        for curr in  range(0,len(cheater)) :
            solution = Solution(contestId = contest.name , rank = cheater[curr]['rank'], solution = cheater[curr]['solution'], solutionNumber = num)
            solution.save()
    
    fill(cheaters[3], 4)
    fill(cheaters[1], 3)

@app.route('/contest/create', methods=['POST'])
def contest_creation():
    try:
        data = request.get_json()
        contest_name = data.get('name')
        # contest = Contest(name=contest_name)
        
        # Save the contest immediately
        # contest.save()
      
        # Run the async task in a separate thread
        asyncio.run(save_contest_with_Cheaters(contest_name))

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
