import json
from PlagModel import checkPlagPercentage  # Ensure this is an async function
import asyncio
import time

max_retries = 5        # Maximum retry attempts
retry_delay = 1        # Initial delay in seconds
api_call_limit = 20   # Limit of API calls before pausing
pause_duration = 20    # Pause duration in seconds
call_counter = 0

async def check_plag_percentage_with_retry_and_throttling(code, question_id):
    global call_counter
    call_counter += 1

    if call_counter > api_call_limit:
        print("Reached API call limit. Pausing for 1 minute...")
        await asyncio.sleep(pause_duration)
        call_counter = 1

    for attempt in range(max_retries):
        try:
            result = checkPlagPercentage(code, question_id)
            # print(result)  
            return json.loads(result)
        except Exception as e:  
            if attempt < max_retries - 1:  
                print(f"Error checking plagiarism, retrying ({attempt + 1}/{max_retries}): {e}")
                await asyncio.sleep(retry_delay * 2 ** attempt) 
            else: 
                raise
            # ret = {"score" : 0.01}
            # print(ret)
            # return json.loads(ret)


async def giveMeCheaters():
    global call_counter
    call_counter = 0 # initialize call counter

    with open('responses1.json', 'r') as file:
        data = json.load(file)

    cheaters4 = []
    cheaters4Sol = []
    cheaters3 = []
    cheaters3Sol = []
    i = 0
    for curr in range(0, len(data)):
        print(i)
        i = i + 1
        if data[curr]['questionId'] == 4:
            cheatedPercentage = await check_plag_percentage_with_retry_and_throttling(data[curr]['code'], '4')
            if cheatedPercentage['score'] > 0.7:
                cheaters4.append({"rank": data[curr]['rank'], "username": data[curr]["username"], "cheatedPercentage": cheatedPercentage['score']})
                cheaters4Sol.append({"rank": data[curr]['rank'], "solution": data[curr]["code"]})
        if data[curr]['questionId'] == 3:
            cheatedPercentage = await check_plag_percentage_with_retry_and_throttling(data[curr]['code'], '3')
            if cheatedPercentage['score'] > 0.7:
                cheaters3.append({"rank": data[curr]['rank'], "username": data[curr]["username"], "cheatedPercentage": cheatedPercentage['score']})
                cheaters3Sol.append({"rank": data[curr]['rank'], "solution": data[curr]["code"]})

    cheaters = [cheaters3, cheaters3Sol, cheaters4, cheaters4Sol]
    return cheaters
