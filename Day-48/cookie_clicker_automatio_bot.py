"""
Automates the Cookie Clicker game using Selenium.

The bot continuously clicks the cookie, purchases the
most expensive affordable upgrade every 5 seconds,
and runs for 5 minutes.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep, time

# ---------------------------- SETUP CHROME DRIVER ------------------------------- #

# Configure Chrome browser
chrome_options = webdriver.ChromeOptions()

# Keep browser open after script finishes
chrome_options.add_experimental_option("detach", True)

# Launch Chrome
driver = webdriver.Chrome(options=chrome_options)

# Open Cookie Clicker
driver.get("https://ozh.github.io/cookieclicker/")

# Wait for page to load
sleep(3)

# ---------------------------- LANGUAGE SELECTION ------------------------------- #

print("Looking for language selection...")

try:
    # Select English language
    language_button = driver.find_element(
        by=By.ID,
        value="langSelect-EN"
    )

    print("Found language button, clicking...")

    language_button.click()

    # Allow page to finish loading
    sleep(3)

except NoSuchElementException:
    print("Language selection not found")

# Wait before starting
sleep(2)

# ---------------------------- COOKIE & STORE SETUP ------------------------------- #

# Locate the main cookie
cookie = driver.find_element(
    by=By.ID,
    value="bigCookie"
)

# Generate all product IDs
item_ids = [
    f"product{i}"
    for i in range(18)
]

# ---------------------------- TIMERS ------------------------------- #

# Buy upgrades every 5 seconds
wait_time = 5

timeout = time() + wait_time

# Run the bot for 5 minutes
five_min = time() + (60 * 5)

# ---------------------------- MAIN GAME LOOP ------------------------------- #

while True:

    # Continuously click the cookie
    cookie.click()

    # Check every few seconds if an upgrade can be purchased
    if time() > timeout:

        try:

            # Get current cookie count
            cookies_element = driver.find_element(
                by=By.ID,
                value="cookies"
            )

            cookie_text = cookies_element.text

            # Convert "12,345 cookies" into an integer
            cookie_count = int(
                cookie_text.split()[0]
                .replace(",", "")
            )

            # Get all available products
            products = driver.find_elements(
                by=By.CSS_SELECTOR,
                value="div[id^='product']"
            )

            # Find the most expensive upgrade we can buy
            best_item = None

            for product in reversed(products):

                # Only enabled products can be purchased
                if "enabled" in product.get_attribute("class"):

                    best_item = product
                    break

            # Purchase the selected upgrade
            if best_item:

                best_item.click()

                print(
                    f"Bought item: "
                    f"{best_item.get_attribute('id')}"
                )

        except (
            NoSuchElementException,
            ValueError,
        ):

            print(
                "Couldn't find cookie count "
                "or available upgrades."
            )

        # Reset purchase timer
        timeout = time() + wait_time

    # Stop after 5 minutes
    if time() > five_min:

        try:

            cookies_element = driver.find_element(
                by=By.ID,
                value="cookies"
            )

            print(
                f"Final result: "
                f"{cookies_element.text}"
            )

        except NoSuchElementException:

            print(
                "Couldn't retrieve "
                "the final cookie count."
            )

        break