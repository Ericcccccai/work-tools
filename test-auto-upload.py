import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


options = Options()
driver = webdriver.Chrome(options=options)

################################
# REMEMBER TO UPDATE THIS LINK WITH CORRESPOND FLOOR
################################
driver.get("https://app.structionsite.com/projects/45482/566546")

#enters user name
driver.switch_to.active_element.send_keys("username@fieldai.com") #REPLACE EMAIL

#enter password
passwordSelector = driver.find_element(By.ID, "user_password")
passwordSelector.send_keys("passwordHere") #REPLACE PASSWORD

#click login button
loginButton = driver.find_element(By.ID, "sign-in-button")
loginButton.click()

#click dropdown box
dropdown_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'rounded') and contains(@class,'text-white')]"))
)
dropdown_button.click()

#input("Press Enter to close the browser...")

#click Coordinated BIM
dropdown_item = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Coordinated BIM')]"))
)
dropdown_item.click()

#input("Press Enter to close the browser...")

#click Import Photos
def find_zip_files(directory):
    """Recursively find all .zip files within a given directory."""
    zip_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".zip"):
                zip_files.append(os.path.join(root, file))
    return zip_files

################################
# REMEMBER TO UPDATE THIS PATH WITH CORRESPOND FOLDER
################################
parent_folder = "/Users/caizhehao/Desktop/0318/floor_005_converted/id"

zip_files = find_zip_files(parent_folder)
zip_files = sorted(zip_files)
totalUpload = 0

for zip_file_path in zip_files:
    file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
    file_input.send_keys(zip_file_path)
    print(f"Uploaded: {zip_file_path}")  # Optional: print the path of the uploaded file
    time.sleep(20)  # Wait for 10 seconds before the next upload
    dropdown_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'rounded') and contains(@class,'text-white')]"))
    )
    dropdown_button.click()

    #click Coordinated BIM
    dropdown_item = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Coordinated BIM')]"))
    )
    dropdown_item.click()
    totalUpload += 1

print("Total Uploaded: %d \n" % totalUpload)
input("Press Enter to close the browser...")
driver.quit()


'''
#test:
driver.get("file:///Users/caizhehao/Desktop/test-upload.html")

#test upload ability
def find_zip_files(directory):
    """Recursively find all .zip files within a given directory."""
    zip_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".zip"):
                zip_files.append(os.path.join(root, file))
    return zip_files

parent_folder = "/Users/caizhehao/Desktop/test_folder"

zip_files = find_zip_files(parent_folder)

for zip_file_path in zip_files:
    file_input = driver.find_element(By.ID, "fileToUpload")
    file_input.send_keys(zip_file_path)
    click_upload_button = driver.find_element(By.ID, "uploadButton")
    click_upload_button.click()
    print(f"Uploaded: {zip_file_path}")  # Optional: print the path of the uploaded file
    time.sleep(10)  # Wait for 10 seconds before the next upload
'''