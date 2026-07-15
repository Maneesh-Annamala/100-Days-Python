from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from dotenv import load_dotenv
import os

"""
Automates the Share-a-Naan platform.

The bot logs into an account, searches for a target account,
follows it if necessary, opens its followers list, scrolls
through all followers, and follows every account that is not
already being followed.
"""

load_dotenv()

ACC = "chefsteps"
MAIL = os.getenv("MAIL")
PASSWORD = os.getenv("PASSWORD")
URL = "https://app.100daysofpython.dev/services/share-a-naan/welcome"


class InstaFollower:
    """Handles login, account search, and follower automation."""

    def __init__(self):
        """Initializes Chrome browser and opens the website."""

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach",True)

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(URL)
        self.wait = WebDriverWait(self.driver,600)

    # ---------------------------- LOGIN ---------------------------- #

    def login(self):
        """Logs into the Share-a-Naan account."""

        mail_box = self.wait.until(EC.visibility_of_element_located((By.XPATH,"/html/body/div/aside/div/form/input[1]")))
        mail_box.send_keys(MAIL)

        pass_box = self.wait.until(EC.visibility_of_element_located((By.XPATH,"/html/body/div/aside/div/form/input[2]")))
        pass_box.send_keys(PASSWORD)

        # Click login button
        self.wait.until(EC.element_to_be_clickable((By.XPATH,"/html/body/div/aside/div/form/button"))).click()

        # Dismiss "Save Login" popup
        self.wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="popup-save-login"]/div/div[2]'))).click()

        # Dismiss notification popup
        self.wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="popup-notifications"]/div/button[2]'))).click()

    # ---------------------------- SEARCH ACCOUNT ---------------------------- #

    def find_account(self):
        """Searches for the target account and follows it if needed."""

        # Open search
        self.wait.until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[1]/nav/button"))).click()

        # Enter account name
        search_box = self.wait.until(EC.visibility_of_element_located((By.XPATH,"/html/body/aside/div[2]/input")))
        search_box.send_keys(ACC)

        # Open searched account
        self.wait.until(EC.element_to_be_clickable((By.XPATH,"/html/body/aside/div[4]/a"))).click()

        # Follow account if not already followed
        follow = self.wait.until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[1]/main/header/div[2]/div[1]/div/button[1]")))

        if follow.text == "Following":
            pass
        else:
            follow.click()

    # ---------------------------- FOLLOW FOLLOWERS ---------------------------- #

    def finding_followers(self):
        """Opens followers list, scrolls through it, and follows users."""

        # Open followers popup
        self.wait.until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[1]/main/header/div[2]/div[2]/span[2]/a"))).click()

        # Followers popup container
        pop_up = self.wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[2]/div/div[3]")))

        # Scroll until all followers are loaded
        while True:

            self.follow()

            old_height = self.driver.execute_script(
                "return arguments[0].scrollHeight;",
                pop_up
            )

            self.driver.execute_script(
                "arguments[0].scrollTop = arguments[0].scrollHeight;",
                pop_up
            )

            sleep(2)

            new_height = self.driver.execute_script(
                "return arguments[0].scrollHeight;",
                pop_up
            )

            # Stop scrolling when no new followers are loaded
            if old_height == new_height:
                break

        # self.driver.quit()

    # ---------------------------- FOLLOW USERS ---------------------------- #

    def follow(self):
        """Follows all users that are not already followed."""

        followers = self.wait.until(
            EC.visibility_of_all_elements_located(
                (By.CSS_SELECTOR,".naan-follow-btn")
            )
        )

        for follower in followers:

            if follower.text == "Following":
                continue

            else:
                follower.click()


# ---------------------------- START BOT ---------------------------- #

bot = InstaFollower()

bot.login()

bot.find_account()

bot.finding_followers()