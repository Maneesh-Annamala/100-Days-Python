"""
Automates the TinDog website using Selenium.

The bot logs in using a Facebark account, dismisses
initial popups, and automatically likes 20 dog profiles.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import os
from time import sleep
from dotenv import load_dotenv

load_dotenv()

MY_MAIL = os.getenv("MAIL")
MY_PASSWORD = os.getenv("PASSWORD")
TIND_DOG_URL = "https://app.100daysofpython.dev/services/tindog/u/i6OQ8qFCwApU_ojS0GJYg2af08QOVkJf"

# ---------------------------- CHROME DRIVER SETUP ------------------------------- #

chrome_options = webdriver.ChromeOptions()

# Keep browser open after script finishes
chrome_options.add_experimental_option("detach", True)

# Use a custom Chrome profile to preserve login sessions
user_data_dir = os.path.join(os.getcwd(), "chrome_data")
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

driver = webdriver.Chrome(options=chrome_options)
driver.get(TIND_DOG_URL)

# Explicit wait object
wait = WebDriverWait(driver, 10)

# ---------------------------- LOGIN PROCESS ------------------------------- #

# Click the login button
login_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[text()="Log in"]')))
login_button.click()

# Select Facebark login
facebook_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn-facebark')))
facebook_button.click()

# ---------------------------- FACEBARK LOGIN ------------------------------- #

# Wait for popup window to open
sleep(2)

# Store both browser windows
base_window = driver.window_handles[0]
facebark_window = driver.window_handles[1]

# Switch to Facebark login popup
driver.switch_to.window(facebark_window)
print(driver.title)

# Enter login credentials
email = wait.until(EC.visibility_of_element_located((By.ID, 'email')))
password = wait.until(EC.visibility_of_element_located((By.ID, 'pass')))

email.send_keys(MY_MAIL)
password.send_keys(MY_PASSWORD)

# Submit login form
password.send_keys(Keys.ENTER)

# Return to TinDog window
driver.switch_to.window(base_window)
print(driver.title)

# ---------------------------- HANDLE POPUPS ------------------------------- #

# Allow location permission
wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Allow"]'))).click()

# Dismiss notifications popup
wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Not interested"]'))).click()

# Accept terms and conditions
wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="I Accept"]'))).click()

# ---------------------------- LIKE DOG PROFILES ------------------------------- #

# Like the first 20 available dog profiles
for n in range(20):
    try:
        like_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn-like')))
        like_button.click()

    except ElementClickInterceptedException:

        # Match popup appeared, close it and continue
        try:
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.match-popup a'))).click()

        except NoSuchElementException:
            print("We failed to find that element")

# Close browser
driver.quit()