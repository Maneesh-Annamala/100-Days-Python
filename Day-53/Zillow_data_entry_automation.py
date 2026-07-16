from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from bs4 import BeautifulSoup
import requests

"""
Scrapes house listings from the Zillow Clone website
and automatically submits each property's details into
a Google Form using Selenium.
"""

FORM_URL = "https://forms.gle/5kZxJxotzEVSjtSSA"
ZILLOW_URL = "https://appbrewery.github.io/Zillow-Clone/"

# ---------------------------- SCRAPE HOUSE DATA ---------------------------- #

# Request Zillow clone webpage
response = requests.get(ZILLOW_URL)
response.raise_for_status()

data = response.text

# Parse HTML
soup = BeautifulSoup(data, "html.parser")

# Get all house addresses
houses_data = soup.select(".StyledPropertyCardDataWrapper a address")
house_addresses = [address.get_text().strip() for address in houses_data]

# Get all house prices
raw_house_price = [
    price.get_text().strip().split("+")
    for price in soup.select(
        ".StyledPropertyCardDataWrapper .PropertyCardWrapper__StyledPriceLine"
    )
]

house_prices = [price[0] for price in raw_house_price]

# Get all property links
house_links = [
    link.get("href")
    for link in soup.select(".StyledPropertyCardDataWrapper a")
]

# ---------------------------- SELENIUM SETUP ---------------------------- #

chrome_options = webdriver.ChromeOptions()

# Keep browser open after execution
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get(FORM_URL)

# Explicit wait object
wait = WebDriverWait(driver, 180)

# ---------------------------- FILL GOOGLE FORM ---------------------------- #

# Submit every property into the Google Form
for address, price, link in zip(house_addresses, house_prices, house_links):

    # Address field
    address_box = wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input'
            )
        )
    )
    address_box.send_keys(address)

    # Price field
    price_box = wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input'
            )
        )
    )
    price_box.send_keys(price)

    # Link field
    link_box = wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input'
            )
        )
    )
    link_box.send_keys(link)

    # Submit the form
    submit_button = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span'
            )
        )
    )
    submit_button.click()

    # Wait briefly before opening a new form
    sleep(1)

    # Open another blank form response
    another_response = wait.until(
        EC.element_to_be_clickable(
            (
                By.LINK_TEXT,
                "Submit another response"
            )
        )
    )
    another_response.click()
driver.quit()