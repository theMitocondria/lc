import json
from PlagModel import checkPlagPercentage
import asyncio

async def giveMeCheaters () : 
    with open('responses2.json', 'r') as file:
        data = json.load(file)

    cheaters4 = []
    cheaters4Sol = []
    cheaters3 = []
    cheaters3Sol = []

    for curr in range(0, len(data)) : 
        # print(data[curr]['questionId'])
        if  data[curr]['questionId'] == 4 : 
            cheatedPercentagejson = checkPlagPercentage(data[curr]['code'],'4')
            cheatedPercentage = json.loads(cheatedPercentagejson)
            if cheatedPercentage['score'] > 0.7 :
                cheaters4.append({"rank" : data[curr]['rank'], "username" : data[curr]["username"], "cheatedPercentage" : cheatedPercentage['score']})
                cheaters4Sol.append({"rank" : data[curr]['rank'], "solution" : data[curr]["code"]})
        if  data[curr]['questionId'] == 3 : 
            cheatedPercentagejson = checkPlagPercentage(data[curr]['code'],'3')
            cheatedPercentage = json.loads(cheatedPercentagejson)
            if cheatedPercentage['score'] > 0.7 :
                cheaters3.append({"rank" : data[curr]['rank'], "username" : data[curr]["username"], "cheatedPercentage" : cheatedPercentage['score']})
                cheaters3Sol.append({"rank" : data[curr]['rank'], "solution" : data[curr]["code"]})
        

    cheaters = [cheaters3, cheaters3Sol, cheaters4, cheaters4Sol]
    # cheaters = [cheaters3, cheaters4]
    return cheaters


