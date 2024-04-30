import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


options = Options()
driver = webdriver.Chrome(options=options)

################################
# REMEMBER TO UPDATE THIS LINK WITH CORRESPOND FLOOR
################################
driver.get("https://app.structionsite.com/projects/ef977725-7ca1-4acb-891c-63922a6100a1/dashboard")


#enters user name
driver.switch_to.active_element.send_keys("sunggoo@fieldai.com") #REPLACE EMAIL

#enter password
passwordSelector = driver.find_element(By.ID, "user_password")
passwordSelector.send_keys("23361madero!") #REPLACE PASSWORD

#click login button
loginButton = driver.find_element(By.ID, "sign-in-button")
loginButton.click()

input()