from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd


START_URL = "https://en.wikipedia.org/wiki/List_of_brown_dwarfs"

# Webdriver
browser = webdriver.Chrome("D:/Setup/chromedriver_win32/chromedriver.exe")
browser.get(START_URL)

time.sleep(10)

new_stars_data = []

def scrape_more_data(hyperlink):
    print(hyperlink)
    try:
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content, "html.parser")

        temp_list = []
        for tr_tag in soup.find_all("tr", attrs = {"class": "fact_row"}):
            td_tags = tr_tag.find_all("td")

            for td_tag in td_tags:
                try:
                    temp_list.append(td_tag.find_all("div", attrs = {"class": "value"})[0].contents[0])
                except:
                    temp_list.append("")
            new_stars_data.append(temp_list)

    except:
        time.sleep(1)
        scrape_more_data(hyperlink)
    
star_df_1 = pd.read_csv("updated_scraped_data.csv")

for index, row in star_df_1.iterrows():
    print(row['hyperlink'])
    scrape_more_data(row['hyperlink'])
    print(f"Data Scraping at hyperlink {index+1} completed")
    ## ADD CODE HERE ##







print(new_stars_data)

# Remove '\n' character from the scraped data
scraped_data = []

for row in new_stars_data:
    replaced = []
    
    for i in row:
        i = i.replace('\n', '')
        replaced.append(i)
    scraped_data.append(replaced)

print(scraped_data)

headers = ["star_name","radius", "mass", "distance_data"]

new_star_df_1 = pd.DataFrame(scraped_data,columns = headers)

# Convert to CSV
new_star_df_1.to_csv('new_scraped_data.csv', index=True, index_label="id")