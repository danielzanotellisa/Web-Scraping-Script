import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import pandas as pd
from time import sleep

ano = input('Escolha o ano para gerar sua tabela: ')
url = 'https://www.formula1.com/en.html'
driver = webdriver.Firefox()
driver.get(url)
def load_cookies():
    cookies = pickle.load(open('cookies.pkl', 'rb'))
    for cookie in cookies:
        cookie['domain'] = '.formula1.com'
        try:
            driver.add_cookie(cookie)
        except Exception as e:
            print(e)
load_cookies()
driver.get(url)
driver.find_element(By.LINK_TEXT, value='Results').click()
sleep(1)
page = driver.current_url
load_cookies()
sleep(1)
scroll_click = driver.find_element(By.XPATH, '//html//body//div[@class="site-wrapper"]//main[@class="template template-resultsarchive"]//article//div[@class="inner-wrap ResultArchiveWrapper"]//div[@class="ResultArchiveContainer"]//div[@class="resultsarchive-filter-container"]//div[@class="resultsarchive-filter-wrap"]//button[@class="filter-controls-down icon-arrow ScrollDownTrigger active"]')

while True:
    try:
        driver.find_element(By.LINK_TEXT, value=ano).click()
        break
    except:
        scroll_click.click()

sleep(2)

table = driver.find_element(By.XPATH, '//div[@class="table-wrap"]//table[@class="resultsarchive-table"]')
html_content = table.get_attribute('outerHTML')


soup = BeautifulSoup(html_content, 'html.parser')
tabela = soup.find(name='table')

df_full = pd.read_html(str(tabela))[0]
df = df_full[['Grand Prix', 'Winner', 'Car']]
df.columns = ['gp', 'winner', 'car']

df.to_excel(f'winners_{ano}.xlsx')

driver.quit()
