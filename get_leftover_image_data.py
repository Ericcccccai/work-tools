import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from collections import defaultdict, Counter
import itertools
import pandas as pd

################################################################
#initialize page
################################################################

#get location to chrome driver
options = Options()
driver = webdriver.Chrome(options=options)

#get all the tags to DPR
driver.get("https://app.structionsite.com/projects/45482/photos")

#enters user name
driver.switch_to.active_element.send_keys("sunggoo@fieldai.com") #REPLACE EMAIL

#enter password
passwordSelector = driver.find_element(By.ID, "user_password")
passwordSelector.send_keys("23361madero!") #REPLACE PASSWORD

#click login button
loginButton = driver.find_element(By.ID, "sign-in-button")
loginButton.click()

#hold all drawing counts across tags
all_drawings_counts = {}
all_image_counts = {}

################################################################
#enable search by date
################################################################
#click drop down
# tag_drop_down = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, "//*[@id='project_list']/div/div[2]/div[2]/div[1]/div/div/button"))
# )
# tag_drop_down.click()

# #enable search by tag
# tag_switch = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='dates-toggle']"))
# )
# tag_switch.click()



################################################################
#some time ti manually enter date range
################################################################

time.sleep(60)


################################################################
#functions
################################################################

def scrape_data():

    # Wait for the page to load fully (adjust the wait condition as needed)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".group.relative"))
    )

    # Extract the HTML content of the page
    html_content = driver.page_source

    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract all blocks that contain the date and drawing info
    blocks = soup.find_all('div', class_='group relative')

    # Dictionary to hold the data
    data = defaultdict(lambda: Counter())

    # Process each block
    for block in blocks:
        date_text = block.find('p', class_='font-semibold').get_text(strip=True)
        drawing_info = block.find('p', string=lambda t: t and 'Drawing:' in t)
        if drawing_info:
            drawing_name = drawing_info.text.split(': ')[1].strip()

            # Increment the count for the corresponding drawing level and date
            data[date_text][drawing_name] += 1

    return data

# URL of the page to scrape
results = scrape_data()

# Print results
for date, counts in results.items():
    print(f"Results for {date}:")
    for drawing, count in counts.items():
        print(f"  {drawing}: {count} images")

# Convert results to a DataFrame for better visualization
dates = list(results.keys())
levels = ['Level 1', 'Level 2', 'Level 3', 'Level 4', 'Roof']
df_data = {
    'Date': dates,
    'Level 1': [results[date].get('Building Interior - Level 1', 0) for date in dates],
    'Level 2': [results[date].get('Building Interior - Level 2', 0) for date in dates],
    'Level 3': [results[date].get('Building Interior - Level 3', 0) for date in dates],
    'Level 4': [results[date].get('Building Interior - Level 4', 0) for date in dates],
    'Roof': [results[date].get('Building Interior - Roof', 0) for date in dates]
}

df = pd.DataFrame(df_data)
print(df)