import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

# Load JSON data from 1.json file
with open('1.json', 'r') as file:
    data = json.load(file)

# Setup Selenium
def setup_driver():
    options = Options()
    # options.add_argument('--headless')  # Uncomment this line if you want to run in headless mode
    options.add_argument('--disable-gpu')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# Fetch the solution code from a given URL
def fetch_solution(user, solution_url, questionId):
    driver = setup_driver()
    try:
        driver.get(solution_url)
        time.sleep(1)  # Slightly longer wait time for safety

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        pre_tag = soup.find('pre')

        if pre_tag:
            json_data = json.loads(pre_tag.text)
            code = json_data.get('code', '')
            return {
                "rank": user['rank'],
                "username": user['username'],
                "solution_url": solution_url,
                "questionId" : questionId,
                "code": code
            }
    except Exception as e:
        print(f"Error fetching {solution_url} for {user['username']}: {e}")
    finally:
        driver.quit()
    return None

responses = []

# Use ThreadPoolExecutor to parallelize fetching process
with ThreadPoolExecutor(max_workers=5) as executor:  # Adjust max_workers as needed
    futures = []

    for user in data:
      

        for solution_url in user['solutions']:
            # print(solution_url, solution_url['3'])
            if '3' in solution_url :
                 futures.append(executor.submit(fetch_solution, user, solution_url['3'], 3))
            if '4' in solution_url : 
                futures.append(executor.submit(fetch_solution, user, solution_url['4'], 4))

    
    for future in as_completed(futures):
        result = future.result()
        if result:
            responses.append(result)

with open('responses1.json', 'w') as file:
    json.dump(responses, file, indent=4)

print("Data fetched and saved to responses1.json")
