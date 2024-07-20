import json
from PlagModel import checkPlagPercentage 
import asyncio
import time

max_retries = 5       
retry_delay = 1       
api_call_limit = 30   
pause_duration = 10   

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
            print(result)  
            return json.loads(result)
        except Exception as e:  
            print('error :((((((' )
            print(e)
            ret = {"score" : 0.01}
            if isinstance(ret, dict):
                return ret
            else:
                return json.loads(ret)

            
async def giveMeCheaters():
    global call_counter
    call_counter = 0 

    with open('responses.json', 'r') as file:
        data = json.load(file)
    print(len(data))

    cheaters4 = []
    cheaters4Sol = []
    cheaters3 = []
    cheaters3Sol = []
    i = 0
    for curr in range(0, len(data)):
        print(i)
        i = i + 1
        if data[curr]['questionId'] == '4':
            cheatedPercentage = await check_plag_percentage_with_retry_and_throttling(data[curr]['code'], '4')

            if cheatedPercentage['score'] > 0.78:
                cheaters4.append({"rank": data[curr]['rank'], "username": data[curr]["username"], "cheatedPercentage": cheatedPercentage['score']})
                cheaters4Sol.append({"rank": data[curr]['rank'], "solution": data[curr]["code"]})
        if data[curr]['questionId'] == '3':
            cheatedPercentage = await check_plag_percentage_with_retry_and_throttling(data[curr]['code'], '3')
            if cheatedPercentage['score'] > 0.78:

                cheaters3.append({"rank": data[curr]['rank'], "username": data[curr]["username"], "cheatedPercentage": cheatedPercentage['score']})
                cheaters3Sol.append({"rank": data[curr]['rank'], "solution": data[curr]["code"]})

    cheaters = [cheaters3, cheaters3Sol, cheaters4, cheaters4Sol]
    return cheaters
