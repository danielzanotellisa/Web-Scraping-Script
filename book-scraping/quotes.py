import pandas as pd
import requests
from bs4 import BeautifulSoup

page_count = 1


data = []

while page_count <= 10:
    url = f'https://quotes.toscrape.com/page/{page_count}/'

    page = requests.get(url)

    soup = BeautifulSoup(page.text, 'html.parser')

    quotes = soup.find_all('div', class_='quote')
    for q in quotes:

        item = {}
        item['Quote'] = q.find('span', class_='text').text
        item['Author'] = q.find('small', class_='author').text
        
        data.append(item)
    page_count+=1

df = pd.DataFrame(data)

df.to_csv('quotes.csv')
df.to_excel('quotes.xlsx')

