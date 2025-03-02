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
from collections import Counter
import itertools

################################################################
#initialize page
################################################################

#get location to chrome driver
options = Options()
driver = webdriver.Chrome(options=options)

#get all the tags to DPR
driver.get("https://app.structionsite.com/projects/xxx/info")

#enters user name
driver.switch_to.active_element.send_keys("xxx") #REPLACE EMAIL

#enter password
passwordSelector = driver.find_element(By.ID, "user_password")
passwordSelector.send_keys("xxx") #REPLACE PASSWORD

#click login button
loginButton = driver.find_element(By.ID, "sign-in-button")
loginButton.click()

#hold all drawing counts across tags
all_drawings_counts = {}
all_image_counts = {}

################################################################
#beautifulsoup to get name for each tag
################################################################

# allow time for JavaScript to load (use explicit waits for better results)
wait = WebDriverWait(driver, 10)  # wait for 10 seconds
wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "pr-0")))

# get the HTML content from the page
html_content = driver.page_source

# parse the HTML with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# find all elements with the specific class
class_name = "sw-chip rounded-r-none pr-0 group"
tags = soup.select(f".{'.'.join(class_name.split())}")  # Converts class names into a CSS selector

# atore usable element texts for future use
all_tags = [tag.get_text(strip=True) for tag in tags if tag.get_text(strip=True).startswith('202')]


# print out the texts of these elements
print(all_tags)

################################################################
#get tag done...
#now avigate under the photo tab
################################################################
photos_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.LINK_TEXT, "Photos"))
)
photos_button.click()

# allow time for JavaScript to load (use explicit waits for better results)
wait = WebDriverWait(driver, 10)  # wait for 10 seconds

#enable search by tag
#click drop down
tag_drop_down = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//*[@id='project_list']/div/div[2]/div[2]/div[1]/div/div/button"))
)
tag_drop_down.click()

#enable search by tag
tag_switch = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='tags-toggle']"))
)
tag_switch.click()

#close drop down
tag_drop_down = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//*[@id='project_list']/div/div[2]/div[2]/div[1]/div/div/button"))
)
tag_drop_down.click()

################################################################
#functions
################################################################

def enter_tag(tag_name):
    #open drop down
    tag_drop_down = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='project_list']/div/div[2]/div[2]/div[1]/div/div/button"))
    )
    tag_drop_down.click()

    #enter tag
    tag_entry = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@aria-label='Search tags...']"))
    )
    tag_entry.send_keys(tag_name)

    # wait for the dropdown to appear and load all options
    wait.until(EC.visibility_of_element_located((By.ID, "ReactTags-listbox")))

    # locate the dropdown list item by its ID or other attributes
    dropdown_item = driver.find_element(By.ID, "ReactTags-listbox-0")

    # click on the dropdown item
    dropdown_item.click()

    #close drop down
    tag_drop_down = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='project_list']/div/div[2]/div[2]/div[1]/div/div/button"))
    )
    tag_drop_down.click()

def delete_tag(tag_name):
    try:
        #click drop down
        tag_drop_down = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='project_list']/div/div[2]/div[2]/div[1]/div/div/button"))
        )
        tag_drop_down.click()

        # wait for the tag to be visible and clickable
        tag_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//button[contains(@class, 'react-tags__selected-tag')]/.."))
        )
        
        # click the tag to delete it
        tag_button.click()
        print(f"Tag '{tag_name}' deleted successfully.")

        # close drop down
        tag_drop_down = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='project_list']/div/div[2]/div[2]/div[1]/div/div/button"))
        )
        tag_drop_down.click()

    except Exception as e:
        print(f"Failed to delete tag '{tag_name}': {str(e)}")
        delete_tag(tag_name)

def get_numbers():
    global all_drawings_counts
    # continuously click the "Next" button until it becomes disabled
    print("Getting numbers...")
    spinner = itertools.cycle(['-', '/', '|', '\\'])
    page_num = 1
    # initialize a Counter to store and count drawing names
    drawing_counts = Counter()
    while True:
        # force to wait 5 sec
        time.sleep(5)

        drawing_elements = driver.find_elements(By.XPATH, "//p[contains(text(), 'Drawing:')]")

        # process each element found
        print(f"Now on page {page_num}")
        for element in drawing_elements:
            drawing_name = element.text.split('Drawing: ')[1]
            drawing_counts[drawing_name] += 1
        try:
            # check if the "Next" button is disabled
            next_button_disabled = driver.find_elements(By.CSS_SELECTOR, "li.next.disabled")
            if next_button_disabled:
                print("Reached the last page.")
                break

            # if not disabled, click the "Next" button
            page_num += 1
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "li.next a[role='button'][aria-disabled='false']"))
            )
            next_button.click()

        except Exception as e:
            print(f"Stopped navigation due to an error: {str(e)}")
            break
    # update global counts for this tag
    if tag not in all_drawings_counts:
        all_drawings_counts[tag] = drawing_counts
    else:
        all_drawings_counts[tag].update(drawing_counts)

    # Print the results
    for name, count in drawing_counts.items():
        print(f"{name}: {count}")
    print("\nget number done.")

def get_total_images(tag):
    # get total number of images under that tag
    # get the updated HTML content
    time.sleep(2)
    updated_html_content = driver.page_source

    # parse the HTML with BeautifulSoup
    soup = BeautifulSoup(updated_html_content, 'html.parser')

    # find the span with the class 'selected-count' and get its text
    selected_count_text = soup.find('span', class_='selected-count').get_text()

    # extract the number of photos
    number_of_photos = selected_count_text.split('/')[1].split()[0]

    # store the count in the global dictionary
    all_image_counts[tag] = int(number_of_photos)

    print(number_of_photos, " for tag: " + tag)

################################################################
#main function
################################################################

if __name__ == "__main__":
    #test_count = 0
    for tag in all_tags:
        time.sleep(2)
        enter_tag(tag)
        time.sleep(2)
        get_total_images(tag)
        time.sleep(2)
        get_numbers()
        time.sleep(2)
        delete_tag(tag)
        # test_count += 1
        # if test_count == 2:
        #     break
    # print all collected drawing counts
    print("\nFinal Results:")
    for tag in all_tags:
        print(f"Results for {tag}:")
        if tag in all_drawings_counts:
            for drawing, count in all_drawings_counts[tag].items():
                print(f"  {drawing}: {count} drawings")
        if tag in all_image_counts:
            print(f"  Total images: {all_image_counts[tag]}")

    #dont close the browswer after done
    input("done")
