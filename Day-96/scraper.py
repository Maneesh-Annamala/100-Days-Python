from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from datetime import datetime
from selenium.common.exceptions import StaleElementReferenceException

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument(r"--user-data-dir=D:\selenium\linkedin-profile")

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://www.linkedin.com/feed/")

wait = WebDriverWait(driver,15)

job_locator = (By.CSS_SELECTOR,"a[aria-label^='Jobs']")

# wait.until(ec.element_to_be_clickable(job_data_button)).click()

for _ in range(3):
    try:
        wait.until(
            ec.element_to_be_clickable(job_locator)
        ).click()
        break
    except StaleElementReferenceException:
        continue
search_key = driver.find_element(By.CSS_SELECTOR,"input[data-testid='typeahead-input']")

search_key.send_keys("python backend developer")
search_key.send_keys(Keys.ENTER)

show_more = wait.until(ec.element_to_be_clickable(
    (By.XPATH,"//*[@id='workspace']/div/div/div/section/div/div/div[1]/div/div[1]/div[2]/a"))).click()

wait.until(ec.url_contains("/jobs/search-results/"))
job_locator = (By.XPATH,"//*[contains(@componentkey, 'job-card-component')]")

# Wait until at least one job card exists
wait.until(lambda driver: len(driver.find_elements(*job_locator)) > 0)
job_cards = driver.find_elements(*job_locator)
# print("Number of jobs:", len(job_cards))
# first_job = job_cards[0]
# print(first_job.get_attribute("outerHTML")[:10000])

# print(datetime.now().strftime("%Y-%m-%d"))
date = datetime.now().strftime("%Y-%m-%d")
with open(f"{date}.csv","w") as file:
    for job in job_cards:
        title = job.find_element(By.CSS_SELECTOR,"div[data-display-contents='true'] > p > span:not([aria-hidden='true'])").text
        company = job.find_element(By.XPATH,".//div[@data-display-contents='true']/following::p[1]").text
        location = job.find_element(By.XPATH,".//div[@data-display-contents='true']/following::p[2]").text
        posted = job.find_element(By.XPATH,".//span[contains(text(), 'Posted')]").text
        file.write(f"{title},{company},{location},{posted}\n")




