import json
import asyncio
import aiohttp
from Contants import BASE_URL
import time

async def fetchSol(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()  
                data = await response.json()
                return data.get('code')
    except Exception as e:
        print(f"Error fetching solution from {url}: {e}")
        return '' 

async def giveSol():
    start_time = time.monotonic() 
    with open('1.json', 'r') as file:
        data = json.load(file)

    res = []

  
    for curr in range(0, len(data)):
        print(curr)
        for sol in range(0, len(data[curr]['solutions'])):
            for key, value in data[curr]['solutions'][sol].items():
                # print(f"{key}: {value}")
                temp = {}
                temp['rank'] = data[curr]['rank']
                temp['username'] = data[curr]['username']
                temp['questionId'] = key
                temp['solution_url'] = value
                temp['code'] = await fetchSol(value)
                res.append(temp)

    with open('responses.json', 'w') as outfile:
        json.dump(res, outfile, indent=4)
    end_time = time.monotonic()    # Stop the timer
    total_time = end_time - start_time
    print(f"Total execution time: {total_time:.2f} seconds") 
    
asyncio.run(giveSol())