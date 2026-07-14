from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import os
from time import sleep
from load_dotenv import load_dotenv

load_dotenv()


"""
Checks internet speed using Speedtest.net.

If the measured download or upload speed is below
the expected speed, the bot logs into the Y platform
and posts a complaint automatically.
"""

Y_URL = "https://app.100daysofpython.dev/services/y"
Y_MAIL = os.getenv("MAIL")
Y_PASSWORD = os.getenv("PASSWORD")

# Expected internet speeds
DOWN_SPEED = 100
UP_SPEED = 30

INTERNET_URL = "https://www.speedtest.net/"


class InternetSpeedTwitterBot:
    """Automates internet speed testing and complaint posting."""

    def __init__(self):
        """Initializes Chrome browser and WebDriverWait."""

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)

        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 600)

    # ---------------------------- INTERNET SPEED TEST ---------------------------- #

    def get_internet_speed(self):
        """Measures current download and upload speed."""

        self.driver.get(INTERNET_URL)

        # Give the page some time to load
        sleep(5)

        # Accept cookie popup
        continue_cookie = self.wait.until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        )
        continue_cookie.click()

        # Start speed test
        go_button = self.driver.find_element(
            By.XPATH,
            value='//*[@id="root"]/div/div[1]/div/div[2]/div[2]/div[2]/div/div/div[2]/div[2]/button'
        )
        go_button.click()

        try:
            # Wait until download speed is displayed
            self.download_speed = self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH,
                     '//*[@id="root"]/div/div[1]/div/div[2]/div[2]/div[2]/div/div/div/div[2]/div[2]/div[1]/div[1]/div/h3')
                )
            ).text

            # Wait until upload speed is displayed
            self.upload_speed = self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH,
                     '//*[@id="root"]/div/div[1]/div/div[2]/div[2]/div[2]/div/div/div/div[2]/div[2]/div[1]/div[2]/div/h3')
                )
            ).text

        except TimeoutException:
            print("It's taking more than 10 minutes, please check your connection.")
            return

    # ---------------------------- POST COMPLAINT ---------------------------- #

    def post_internet_speed(self):
        """Posts a complaint if internet speed is below the expected value."""

        if DOWN_SPEED > float(self.download_speed) or UP_SPEED > float(self.upload_speed):

            self.driver.get(Y_URL)

            # Accept cookie popup
            ok_cookie_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".y-btn-primary"))
            )
            ok_cookie_button.click()

            # Open login page
            login_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".y-login-link"))
            )
            login_button.click()

            # Enter email
            email_box = self.wait.until(
                EC.visibility_of_element_located((By.ID, "email"))
            )
            email_box.clear()
            email_box.send_keys(Y_MAIL)

            # Enter password
            pass_box = self.wait.until(
                EC.visibility_of_element_located((By.ID, "password"))
            )
            pass_box.clear()
            pass_box.send_keys(Y_PASSWORD)

            # Login
            login = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".y-btn-primary.y-login-submit"))
            )
            login.click()

            # Open post composer
            post_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".x-sidebar button"))
            )
            post_button.click()

            # Download speed issue only
            if DOWN_SPEED > float(self.download_speed) and UP_SPEED <= float(self.upload_speed):

                message = (
                    f"I have been using the Jio network for a long time, "
                    f"but I am facing internet issues. According to my plan, "
                    f"I should get {DOWN_SPEED} Mbps download speed, "
                    f"but I am getting only {self.download_speed} Mbps."
                )

                self.message_poster(message)
                return

            # Upload speed issue only
            elif DOWN_SPEED <= float(self.download_speed) and UP_SPEED > float(self.upload_speed):

                message = (
                    f"I have been using the Jio network for a long time, "
                    f"but I am facing internet issues. According to my plan, "
                    f"I should get {UP_SPEED} Mbps upload speed, "
                    f"but I am getting only {self.upload_speed} Mbps."
                )

                self.message_poster(message)
                return

            # Both download and upload are below expected
            else:

                message = (
                    f"I have been using the Jio network for a long time, "
                    f"but I am facing internet issues. According to my plan, "
                    f"I should get {DOWN_SPEED} Mbps download speed and "
                    f"{UP_SPEED} Mbps upload speed, but I am getting "
                    f"{self.download_speed} Mbps download and "
                    f"{self.upload_speed} Mbps upload. "
                    f"Will you please resolve this issue?"
                )

                self.message_poster(message)
                return

    # ---------------------------- POST MESSAGE ---------------------------- #

    def message_poster(self, message):
        """Posts the given message on the Y platform."""

        writing_window = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="modal-compose"]'))
        )
        writing_window.send_keys(message)

        final_post = self.wait.until(
            EC.element_to_be_clickable((By.ID, "modal-post-btn"))
        )
        final_post.click()

        self.driver.quit()


# ---------------------------- START BOT ---------------------------- #

bot = InternetSpeedTwitterBot()

bot.get_internet_speed()

bot.post_internet_speed()