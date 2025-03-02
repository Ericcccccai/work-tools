#using selenium 4
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#for update
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType


# Path to ChromeDriver
chrome_driver_path = '/usr/bin/chromedriver'

# Path to Chrome binary
chrome_binary_path = '/usr/bin/chromium-browser'


options = Options()
options.binary_location = chrome_binary_path

# Initialize the Service object with the path to ChromeDriver
service = Service(executable_path=chrome_driver_path)

# Pass the Service object and options when creating the Chrome WebDriver instance
# Update driver too
driver = webdriver.Chrome(service=service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()), options=options)


driver.get("https://app.structionsite.com/projects/xxx/xxx")


#enters user name
driver.switch_to.active_element.send_keys("xxx")

#enter password
passwordSelector = driver.find_element(By.ID, "user_password")
passwordSelector.send_keys("xxx")

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

parent_folder = "xxx"

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
driver.get("xxx")

#test upload ability
def find_zip_files(directory):
    """Recursively find all .zip files within a given directory."""
    zip_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".zip"):
                zip_files.append(os.path.join(root, file))
    return zip_files

parent_folder = "xxx"

zip_files = find_zip_files(parent_folder)

for zip_file_path in zip_files:
    file_input = driver.find_element(By.ID, "fileToUpload")
    file_input.send_keys(zip_file_path)
    click_upload_button = driver.find_element(By.ID, "uploadButton")
    click_upload_button.click()
    print(f"Uploaded: {zip_file_path}")  # Optional: print the path of the uploaded file
    time.sleep(10)  # Wait for 10 seconds before the next upload
'''
