# Python scrpit for extract IPLT20 auction unsold player list with requests, bs4 and lxml parser

import requests
from bs4 import BeautifulSoup
import pandas as pd
from lxml import etree

url = "https://www.iplt20.com/auction"
response = requests.get(url)
# print("response = ", response)

html_content = response.content

soup = BeautifulSoup(html_content, "lxml")

table = soup.find("table", id="t2")

# print(table)

header = table.find_all('th')
titles = []
for th in header:
    titles.append(th.text)

df = pd.DataFrame(columns=titles)
# print(df)

rows = table.find_all("tr")

for row in rows[1:]:
    data = row.find_all("td")
    table_row_data = [tr.text for tr in data]    
    lenght = len(df)
    df.loc[lenght] = table_row_data
# print(df.head())

df.to_csv("H:/Web Scrapping/beautifulsaoup4/project1_iplt20_data_scrape/iplt20_unsold_players_2023.csv")
