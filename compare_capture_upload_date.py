######
#NOPE NOT WORKING :< DOING IT MANUALLY
######




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

time.sleep(15)

scrollbar = driver.find_element(By.XPATH, "//*[@id='prism-mainview']/div[2]/div/div/div/dashboard/div/div[1]/div/div[1]/div/div/div[4]/div[2]/div/widget/blox/div/div[2]/div")
max_scroll_height = 500  # This value should be the maximum scroll height in pixels
driver.execute_script(f"arguments[0].style.transform = 'translate(0px, {max_scroll_height}px)';", scrollbar)



input()

