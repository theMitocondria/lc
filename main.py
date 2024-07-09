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
import time
from datetime import datetime
from selenium.webdriver.common.keys import Keys


def wait_click(driver,xpath, retries=3):
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
NUM_THREADS = 3 # Adjust based on your system

def process_page(page_number):
    solutions_list = []
    # Enable Performance Logging of Chrome. 
    # desired_capabilities = DesiredCapabilities.CHROME 
    # desired_capabilities["goog:loggingPrefs"] = {"performance": "ALL"} 
  
    # Create the webdriver object and pass the arguments 
    options = webdriver.ChromeOptions() 


    # set custom capability to start logging
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
  


    # Ignores any certificate errors if there is any 
    options.add_argument("--ignore-certificate-errors") 
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    options.add_argument("--mute-audio")
    options.add_argument("--disable-popup-blocking")
    # Startup the chrome webdriver with executable path and 
    # pass the chrome options and desired capabilities as 
    # parameters. 
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
                #score = cols[2].text
                #finishing_time = cols[3].text
                # [{rank , username , ['3'],['4']}]
                result = { "rank" : rank , "username" : username , "solutions" : []}
                for i in range(7, 8):
                    try:
                        a_tag = cols[i].find_element(By.TAG_NAME, 'a')
                        if click_element(driver, a_tag):
                            # time.sleep(0.3)  # Ensure the modal appears
                            # capture_api_calls(driver)
                            logs = driver.get_log("performance") 
                            wait_click(driver, '//*[@id="submission"]/div/div/div[1]/button/span[1]')
                            # driver.find_element( By.XPATH , '//*[@id="submission"]/div/div/div[1]/button/span[1]' ).click()
                            # search for the api calls starting from end of the logs and stop when the first api call is found
                            match = ""
                            for i in range(len(logs) - 1, -1, -1):
                                log = str(logs[i])
                                matches = re.search(r'https://leetcode.com/api/submissions\/[0-9]+\/', log)
                                if matches:
                                    match = matches.group(0)
                                    result["solutions"].append(match)
                                    break
                            
                            print(match)
                            
                            # return 
                           
                    except (StaleElementReferenceException, ElementNotInteractableException, ElementClickInterceptedException) as e:
                        print(f"Error processing column {i} for row {idx} on page {page_number}: {e}")
                
                solutions_list.append(result)
            except Exception as e:
                print(f"Error processing row {idx} on page {page_number}: {e}")

    except Exception as e:
        print(f"Error processing page {page_number}: {e}")
    finally:
        driver.quit()
    return solutions_list


with open('1.json', 'w') as file:
    with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        page_results = executor.map(process_page, range(1, 20))
        final_array = []
        for result in page_results:
            final_array = final_array + result 
        json_str = json.dumps(final_array, indent=4)
        file.writelines(json_str)  # Write all solutions from a page at once