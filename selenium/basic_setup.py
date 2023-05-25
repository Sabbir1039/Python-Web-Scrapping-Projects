from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome("C:/Program Files (x86)/chromedriver.exe")

try:
    driver.get("https://www.google.com")

    # print(driver.title)
    time.sleep(1) # need time to load the page

    xpath = "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/textarea"
    textarea = driver.find_element(By.XPATH, xpath) # finds goole search text input box
    textarea.send_keys("python tutorial") # Fill the input box with text
    
    # Click on the google search button
    driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[4]/center/input[1]").click()
    time.sleep(2)

    # Finds all titles of searched page
    try:
        titles = driver.find_elements(By.CLASS_NAME, 'LC20lb')
        for title in titles:
            print(title.text)
    except:
        print(None)

    input("Insert enter to quit!....") # To close current active window press enter
    driver.close()
    
except:
    print(f"Website not responding! Error Occured")