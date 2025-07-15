from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

service = Service(ChromeDriverManager().install())
options = Options()
options.add_argument('--headless')  # Enable headless mode
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=service, options=options)

try:
    driver.get("https://www.bing.com/")

    # print(driver.title)
    time.sleep(3) # need time to load the page

    input_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "sb_form_q"))) # wait until finds goole search text input box
    
    input_field.send_keys("python tutorial") # Fill the input box with text
    print("search text written!")

    time.sleep(7)
    
    input_field.send_keys(Keys.ENTER)
    print("search text submitted!")

    time.sleep(4)

    # Finds all titles of searched page
    results = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "b_dftt")))

    titles = []
    links = []

    print("Results...")
    for result in results:
        titles.append(result.text)
        links.append(result.get_attribute("href"))
    
    print(titles)
    print(links)

    input("Insert enter to quit!....") # To close current active window press enter
    
except:
    print(f"Website not responding! Error Occured")

driver.close()
print("Driver closed!")