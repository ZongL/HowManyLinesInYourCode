from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import requests
from bs4 import BeautifulSoup
import json
import random


# Set the path to your Chrome profile
chrome_profile_path = "C:\\Users\\andyzong\\AppData\\Local\\Google\\Chrome\\User Data"  # Update this path
#C:\Users\andyzong\AppData\Local\Google\Chrome\User Data\Default

# Set up Chrome options to use the existing profile
options = Options()
options.add_argument(f"user-data-dir={chrome_profile_path}")

# Initialize WebDriver with the specified options
driver = webdriver.Chrome(options=options)
driver.minimize_window()
# Open Bing
driver.get('https://www.bing.com')

# Wait for the page to load
time.sleep(2)

def fetch_hot_topics(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()  # Parse the JSON response
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

url = "https://api-hot.imsyy.top/douyin"

hot_topics = fetch_hot_topics(url)

if hot_topics:
    try:
        # Extract titles and put them into the questions array
        questions = [item['title'] for item in hot_topics['data']]
        print(questions)
    except (KeyError, TypeError) as e:
        print(f"An error occurred while parsing the data: {e}")
else:
    print("No data available. Please check the URL and network conditions.")

# Total number of questions
total_questions = len(questions)

# Perform searches
for index, question in enumerate(questions, start=1):
    # Find the search box and enter the question
    search_box = driver.find_element(By.NAME, "q")
    search_box.clear()
    search_box.send_keys(question)
    search_box.send_keys(Keys.RETURN)
    # Print progress
    print(f"Processing question {index} of {total_questions} ({(index / total_questions) * 100:.2f}%)")
    # Wait for the search results to load
    # Generate a random delay between 3 and 6 seconds
    random_delay = random.uniform(3, 6)
    # Use the random delay with time.sleep
    time.sleep(random_delay)


# Close the browser
driver.quit()
