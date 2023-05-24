import requests
from bs4 import BeautifulSoup
import pandas as pd
# import re
import time

rows = []
for i in range(1, 51):
    url = f"https://www.flipkart.com/search?q=smartphone+5g&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page={i}"
    
    try:
        response = requests.get(url)
        response.raise_for_status() # Raise an exception if there's an HTTP error
        
        content = response.content
        soup = BeautifulSoup(content, "lxml")

        main_divs = soup.find_all("div", class_="_3pLy-c row")

        for div in main_divs:
            try:
                title = div.find("div", class_="_4rR01T").text
            except AttributeError:
                title = None
            
            try:
                rating = div.find("div", class_="_3LWZlK").text
            except AttributeError:
                rating = None
            
            try:
                total_ratings_reviews = div.find("span", class_="_2_R_DZ").text
                total_ratings_reviews = total_ratings_reviews.split("&")
                # print(total_ratings_reviews)
                ratings = total_ratings_reviews[0]
                # ratings = re.findall(r'\d+,?\d+,?\d*', ratings)
                # ratings = ratings[0]
                reviews = total_ratings_reviews[1]
                # reviews = re.findall(r'\d+,?\d+,?\d*', reviews)
                # reviews = reviews[0]
            except (AttributeError, ValueError):
                ratings, reviews = None, None
            
        
            try:
                current_price = div.find("div", class_="_30jeq3 _1_WHN1").text
            except AttributeError:
                current_price = None
            
            try:
                original_price = div.find("div", class_="_3I9_wc _27UcVY").text
                # offer = div.find("div", class_="_3Ay6Sb").text
                # delevery_status = div.find("div", class_="_2Tpdn3").text
            except AttributeError:
                original_price = None
                # offer = None
                # delevery_status = None
        
            rows.append([title, rating, ratings, reviews, current_price, original_price])
        
        time.sleep(1) # Introduce a delay of 1 second between requests to be respectful of the website's server resources
            
    except requests.exceptions.RequestException as e:
        print(f"An error occured while making the request: {e}")
    except Exception as e:
        print(f"An error occured: {e}")

columns = ['Title', 'Rating', 'Total Rating', 'Total Reviews', 'Current Price', 'Original Price']
df = pd.DataFrame(rows, columns=columns)
df.to_csv('H:/Web Scrapping/beautifulsaoup4/project2_flipcart_5g_phones_data_scrape/flipcart_5gmobile_data.csv')
print(df.head())


