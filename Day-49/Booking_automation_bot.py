from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
# Import exceptions
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os
import time
from dotenv import load_dotenv

load_dotenv() 

"""
Automates the gym booking process using Selenium.

The bot logs into the website, books or waitlists
Tuesday and Thursday 6:00 PM classes, and verifies
the bookings from the My Bookings page.
"""

# Create Chrome Profile and create account manually. Put YOUR email and password here:
ACCOUNT_EMAIL = os.getenv("MAIL")
ACCOUNT_PASSWORD = os.getenv("PASSWORD")
GYM_URL = "https://appbrewery.github.io/gym/"

# ---------------------------- CHROME DRIVER SETUP ------------------------------- #

chrome_options = webdriver.ChromeOptions()

# Keep the browser open after the script finishes
chrome_options.add_experimental_option("detach", True)

# Store browser profile so login sessions are remembered
user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

driver = webdriver.Chrome(options=chrome_options)
driver.get(GYM_URL)

# Explicit wait object
wait = WebDriverWait(driver, 2)

driver.get(GYM_URL)

# ---------------------------- RETRY MECHANISM ------------------------------- #

def retry(func, retries=7, description=None):
    """Retries a function if TimeoutException occurs."""

    for i in range(retries):
        print(f"Trying {description}. Attempt: {i + 1}")
        try:
            return func()
        except TimeoutException:
            if i == retries - 1:
                raise
            time.sleep(1)

# ---------------------------- LOGIN ------------------------------- #

def login():
    """Logs into the gym website."""

    login_btn = wait.until(ec.element_to_be_clickable((By.ID, "login-button")))
    login_btn.click()

    email_input = wait.until(ec.presence_of_element_located((By.ID, "email-input")))
    email_input.clear()
    email_input.send_keys(ACCOUNT_EMAIL)

    password_input = driver.find_element(By.ID, "password-input")
    password_input.clear()
    password_input.send_keys(ACCOUNT_PASSWORD)

    submit_btn = driver.find_element(By.ID, "submit-button")
    submit_btn.click()

    # Wait until the schedule page is loaded
    wait.until(ec.presence_of_element_located((By.ID, "schedule-page")))

# ---------------------------- BOOK CLASS ------------------------------- #

def book_class(booking_button):
    """Books a class or joins the waitlist."""

    booking_button.click()

    # Wait until booking status changes
    wait.until(lambda d: booking_button.text == "Booked")

# Retry login if timeout occurs
retry(login, description="login")

# ---------------------------- BOOK TUESDAY & THURSDAY CLASSES ------------------------------- #

class_cards = driver.find_elements(By.CSS_SELECTOR, "div[id^='class-card-']")

booked_count = 0
waitlist_count = 0
already_booked_count = 0

processed_classes = []

for card in class_cards:

    # Find the parent day group of the current class
    day_group = card.find_element(By.XPATH, "./ancestor::div[contains(@id, 'day-group-')]")

    # Get the day heading (Tue, Wed, etc.)
    day_title = day_group.find_element(By.TAG_NAME, "h2").text

    # Filter only Tuesday and Thursday classes
    if "Tue" in day_title or "Thu" in day_title:

        # Get class timing
        time_text = card.find_element(By.CSS_SELECTOR, "p[id^='class-time-']").text

        # Filter only 6 PM classes
        if "6:00 PM" in time_text:

            class_name = card.find_element(By.CSS_SELECTOR, "h3[id^='class-name-']").text
            button = card.find_element(By.CSS_SELECTOR, "button[id^='book-button-']")

            class_info = f"{class_name} on {day_title}"

            if button.text == "Booked":

                print(f"✓ Already booked: {class_info}")

                already_booked_count += 1
                processed_classes.append(f"[Booked] {class_info}")

            elif button.text == "Waitlisted":

                print(f"✓ Already on waitlist: {class_info}")

                already_booked_count += 1
                processed_classes.append(f"[Waitlisted] {class_info}")

            elif button.text == "Book Class":

                # Retry booking if timeout occurs
                retry(lambda: book_class(button), description="Booking")

                print(f"✓ Successfully booked: {class_info}")

                booked_count += 1
                processed_classes.append(f"[New Booking] {class_info}")

                time.sleep(0.5)

            elif button.text == "Join Waitlist":

                # Retry waitlist action if timeout occurs
                retry(lambda: book_class(button), description="Waitlisting")

                print(f"✓ Joined waitlist for: {class_info}")

                waitlist_count += 1
                processed_classes.append(f"[New Waitlist] {class_info}")

                time.sleep(0.5)

# ---------------------------- VERIFY BOOKINGS ------------------------------- #

total_booked = already_booked_count + booked_count + waitlist_count

print(f"\n--- Total Tuesday/Thursday 6pm classes: {total_booked} ---")
print("\n--- VERIFYING ON MY BOOKINGS PAGE ---")

def get_my_bookings():
    """Navigates to My Bookings page and returns all booking cards."""

    my_bookings_link = wait.until(ec.element_to_be_clickable((By.ID, "my-bookings-link")))
    my_bookings_link.click()

    # Wait until My Bookings page loads
    wait.until(ec.presence_of_element_located((By.ID, "my-bookings-page")))

    cards = driver.find_elements(By.CSS_SELECTOR, "div[id*='card-']")

    # Raise exception if booking cards are not loaded
    if not cards:
        raise TimeoutException("No booking cards found - page may not have loaded")

    return cards

# Retry navigation if timeout occurs
all_cards = retry(get_my_bookings, description="Get my bookings")

verified_count = 0

for card in all_cards:
    try:
        when_paragraph = card.find_element(By.XPATH, ".//p[strong[text()='When:']]")
        when_text = when_paragraph.text

        # Verify only Tuesday/Thursday 6 PM bookings
        if ("Tue" in when_text or "Thu" in when_text) and "6:00 PM" in when_text:

            class_name = card.find_element(By.TAG_NAME, "h3").text

            print(f"  ✓ Verified: {class_name}")

            verified_count += 1

    except NoSuchElementException:
        # Skip cards that don't contain booking information
        pass

print(f"\n--- VERIFICATION RESULT ---")
print(f"Expected: {total_booked} bookings")
print(f"Found: {verified_count} bookings")

if total_booked == verified_count:
    print("✅ SUCCESS: All bookings verified!")
else:
    print(f"❌ MISMATCH: Missing {total_booked - verified_count} bookings")