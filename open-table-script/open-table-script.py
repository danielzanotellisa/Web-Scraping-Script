import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import json
from io import StringIO
from time import sleep
from bs4 import BeautifulSoup
#Script that alocates all the reviews with stars on a excel file

url = 'https://www.opentable.com/r/via-sophia-by-the-sea-kennebunk-me-kennebunkport'

#Opening the url
driver = webdriver.Firefox()
driver.get(url)
#Getting cookies
def cookies():
    cookies = pickle.load(open('cookies_open_table.pkl', 'rb'))
    for cookie in cookies:
        cookie['domain'] = '.opentable.com'
        try:
            driver.add_cookie(cookie)
        except Exception as e:
            print(e)
cookies()
driver.get(url)
#Creating a soup
review_list = driver.find_element(By.ID, 'restProfileReviewsContent')
html_content = review_list.get_attribute('outerHTML')
soup = BeautifulSoup(html_content, 'html.parser')
#Finding the reviews
data = []

page_counter = 2
while page_counter <= 10:
    reviews = soup.find_all('li', class_='afkKaa-4T28-')
    for r in reviews:
        
        review = {}
        review['review'] = r.find('span', class_='l9bbXUdC9v0- ZatlKKd1hyc- ukvN6yaH1Ds-').text
        review['name'] = r.find('p', class_='_1p30XHjz2rI- C7Tp-bANpE4-').text
        review['from'] = r.find('p', class_='POyqzNMT21k- C7Tp-bANpE4-').text
        review['overall'] = r.find('span', class_='-y00OllFiMo-').text
        data.append(review)
    page_counter+=1
    sleep(0.5)
    url = f'https://www.opentable.com/r/via-sophia-by-the-sea-kennebunk-me-kennebunkport?page={page_counter}&sortBy=newestReview'
    driver.get(url)

df = pd.DataFrame(data)
df.to_excel('reviews.xlsx')

driver.quit()