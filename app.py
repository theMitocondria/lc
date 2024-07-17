from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from database import connect_database
from models import Solution , CheaterArray , Contest , Cheater
from GiveMeCheaters import giveMeCheaters
import asyncio
from Contants import (code3 ,code4)
app = Flask(__name__)
load_dotenv()

# Database connection
connect_database()

# Middleware
CORS(app)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Routes

async def add_cheaters_to_contest(contest):
 
    cheaters = await giveMeCheaters()
    cheaters3 = cheaters[0]
    cheaters3sol = cheaters[1]
    cheaters4 = cheaters[2]
    cheaters4sol = cheaters[3]
    
    def fill(cheaters, cheaters_sol , contest_question_field):
        array_of_cheaters = []
        
        for curr in range(len(cheaters)):
            curr_sol = Solution(code=cheaters_sol[curr]['solution'])
            curr_sol.save()
            curr_cheater = Cheater(
                rank=cheaters[curr]['rank'],
                name_of_cheater=cheaters[curr]['username'],
                plagpercentage=cheaters[curr]['cheatedPercentage'],
                code=curr_sol
            )
            array_of_cheaters.append(curr_cheater)

        if contest_question_field == 3 :
            arraycheaters = CheaterArray.objects.get(id = contest.question3.id)
        elif contest_question_field == 4 :
            arraycheaters = CheaterArray.objects.get(id = contest.question4.id)

        array_of_cheaters = array_of_cheaters + arraycheaters.array_of_cheaters  
        sorted_array_of_cheaters = sorted(array_of_cheaters, key=lambda x: x["plagpercentage"], reverse=True)
        arraycheaters.array_of_cheaters = sorted_array_of_cheaters
        arraycheaters.save()

        if(contest_question_field == 3) :
            contest.question3 = arraycheaters
        elif (contest_question_field == 4) :
            contest.question4 = arraycheaters
            
            
    
    fill(cheaters4,cheaters4sol, 4)
    fill(cheaters3,cheaters3sol, 3)

    contest.save()


@app.route('/contest/addNewCheaters', methods=['POST'])
def add_new_cheaters():
    try:
        data = request.get_json()
        contest_name = data.get('name')

        contest = Contest.objects.get(name = contest_name)
        asyncio.run(add_cheaters_to_contest(contest))

        return jsonify({"message": "Contest found"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



async def save_contest_with_Cheaters(contest_name):

    cheaters = await giveMeCheaters()
    cheaters3 = cheaters[0]
    cheaters3sol = cheaters[1]
    cheaters4 = cheaters[2]
    cheaters4sol = cheaters[3]

    contest = Contest(name=contest_name)
    solution3 = Solution(code = code3)
    solution4 = Solution(code = code4)
    solution3.save()
    solution4.save()
    contest.cheated3Sol = solution3
    contest.cheated4Sol = solution4 
    
    def fill(cheaters, cheaters_sol, contest_question_field):
        array_of_cheaters = []
        for curr in range(len(cheaters)):
            curr_sol = Solution(code=cheaters_sol[curr]['solution'])
            curr_sol.save()
            curr_cheater = Cheater(
                rank=cheaters[curr]['rank'],
                name_of_cheater=cheaters[curr]['username'],
                plagpercentage=cheaters[curr]['cheatedPercentage'],
                code=curr_sol
            )
            array_of_cheaters.append(curr_cheater)
        
        sorted_array_of_cheaters = sorted(array_of_cheaters, key=lambda x: x["plagpercentage"], reverse=True)
        cheaterArray = CheaterArray(array_of_cheaters = sorted_array_of_cheaters) 
        cheaterArray.save()
        # print(cheaterArray)

        if(contest_question_field == 3) :
            contest.question3 = cheaterArray
        elif (contest_question_field == 4) :
            contest.question4 = cheaterArray
        
    
    fill(cheaters3 , cheaters3sol , 3) 
    fill(cheaters4 , cheaters4sol , 4)

    contest.save()

@app.route('/contest/create', methods=['POST'])
def contest_creation():
    try:
        data = request.get_json()
        contest_name = data.get('name')
    
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
