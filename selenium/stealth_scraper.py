# stealth_scraper.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import random
import time
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import urllib.robotparser


# List of rotating User-Agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15"
]

# PROXIES = [
#         "23.227.38.206:80",
#     	"216.205.52.17:80",
#     	"45.8.211.20:80",
#     	"188.42.89.204:80",
#     	"104.27.3.137:80"
# ]

# Respect robots.txt before scraping
def is_scraping_allowed(url):
    rp = urllib.robotparser.RobotFileParser()
    response = rp.set_url("/".join(url.split("/")[:3]) + "/robots.txt")

    if not response:
        print("No robots.txt")
        return None
    
    rp.read()
    return rp.can_fetch("*", url)


def simulate_human_behavior(driver):
    actions = ActionChains(driver)
    actions.move_by_offset(10, 10).perform()
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(random.uniform(1.5, 4.0))

def setup_stealth_driver():
    user_agent = random.choice(USER_AGENTS)
    # proxy = random.choice(PROXIES)

    options = Options()
    service = Service(ChromeDriverManager().install())

    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--headless=new")

    options.add_argument("--window-size=1920,1080")
    options.add_argument("--lang=en-US,en;q=0.9")

    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--start-maximized")

    # For undetected_chromedriver, use these instead of experimental options
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-notifications')

    # Handle proxy (no auth version)
    # if ":" in proxy:
    #     options.add_argument(f'--proxy-server=http://{proxy}')

    #launch driver
    driver = webdriver.Chrome(service=service, options=options)

    # Set timeouts
    driver.set_page_load_timeout(60)     # Allow slow proxy loads
    driver.implicitly_wait(10)
    driver.set_script_timeout(30)
    
    # Stealth patches
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
            Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3] });
        """
    })

    return driver

# scrape test site
def scrape_site(url, retries=3):
    if retries == 0:
        print("Max retries reached. Exiting.")
        return
    
    try:
        driver = setup_stealth_driver()
    except Exception as e:
        print(f"Can not get the driver {e}")

    try:
        driver.get(url)
        simulate_human_behavior(driver=driver)
        
        source = driver.page_source
        soup = BeautifulSoup(source, "html.parser")

        title = soup.find("title")
        
        print(title.text)

    except TimeoutException:
        print("Timeout occurred. Retrying with a different proxy...")
        driver.quit()
        return scrape_site(url, retries-1)  # Retry

    finally:
        if driver:
            try:
                driver.quit()
                print("driver closed!")
            except:
                pass  # Ignore any errors during quit

# Run the scraper
if __name__ == "__main__":
    url = "https://quotes.toscrape.com"

    is_allowed = is_scraping_allowed(url)

    if not is_allowed:
        print("Procced to scrape...")

    scrape_site(url)