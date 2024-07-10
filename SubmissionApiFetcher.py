from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities 
import time 
import regex as re
import json 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    StaleElementReferenceException, 
    ElementNotInteractableException, 
    ElementClickInterceptedException,
    TimeoutException
)
import concurrent.futures
from datetime import datetime
from selenium.webdriver.common.keys import Keys
import threading

lock = threading.Lock()

def wait_click(driver, xpath, retries=3):
    for attempt in range(retries):
        try:
            element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            element.click()
            return True
        except (ElementClickInterceptedException, ElementNotInteractableException, TimeoutException) as e:
            print(f"Attempt {attempt + 1} to click element failed")
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
    return False

def click_element(driver, element, retries=1):
    for attempt in range(retries):
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable(element))
            element.click()
            return True
        except (ElementClickInterceptedException, ElementNotInteractableException) as e:
            print(f"Attempt {attempt + 1} to click element failed")
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
    return False

base_url = 'https://leetcode.com/contest/biweekly-contest-134/ranking/'
NUM_THREADS = 3  # Adjust based on your system

def process_page(page_number):
    solutions_list = []

    options = webdriver.ChromeOptions()
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
    options.add_argument("--ignore-certificate-errors") 
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    options.add_argument("--mute-audio")
    options.add_argument("--disable-popup-blocking")

    driver = webdriver.Chrome(options=options) 

    start_time = datetime.now().strftime("%H:%M:%S")
    print(f"Starting to process page {page_number} at {start_time}")

    url = f'{base_url}{page_number}/'
    driver.get(url)

    table_body = WebDriverWait(driver, 12).until(
        EC.presence_of_element_located((By.TAG_NAME, 'tbody'))
    )

    rows = WebDriverWait(table_body, 12).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, 'tr'))
    )

    try:
        for idx, row in enumerate(rows):
            try:
                cols = row.find_elements(By.TAG_NAME, 'td')
                rank = cols[0].text
                username = cols[1].text
                result = { "rank" : rank , "username" : username , "solutions" : []}
                for i in range(6, 8):
                    questionid = i - 3
                    try:
                        a_tag = cols[i].find_element(By.TAG_NAME, 'a')
                        if click_element(driver, a_tag):
                            logs = driver.get_log("performance") 
                            wait_click(driver, '//*[@id="submission"]/div/div/div[1]/button/span[1]')
                            match = ""
                            for i in range(len(logs) - 1, -1, -1):
                                log = str(logs[i])
                                matches = re.search(r'https://leetcode.com/api/submissions\/[0-9]+\/', log)
                                if matches:
                                    match = matches.group(0)
                                    result["solutions"].append({questionid : match})
                                    break
                            print(match)
                    except (StaleElementReferenceException, ElementNotInteractableException, ElementClickInterceptedException) as e:
                        print(f"Error processing column {i} for row {idx} on page {page_number}: {e}")
                solutions_list.append(result)
            except Exception as e:
                print(f"Error processing row {idx} on page {page_number}: {e}")
    except Exception as e:
        print(f"Error processing page {page_number}: {e}")
    finally:
        driver.quit()
    
    # Write the results of this page to the file immediately
    with lock:
        try:
            with open('2.json', 'r') as file:
                final_array = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            final_array = []
        
        final_array += solutions_list

        with open('2.json', 'w') as file:
            json.dump(final_array, file, indent=4)
    
    return solutions_list

with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
    executor.map(process_page, range(65, 81))