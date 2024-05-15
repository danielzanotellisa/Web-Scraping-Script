import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

driver = webdriver.Firefox()

driver.get('https://www.formula1.com/en.html')
sleep(5)
results = driver.find_element(By.LINK_TEXT, 'Results')
results.click()
table = driver.find_element(By.XPATH, '//div[@class="table-wrap"]//table[@class="resultsarchive-table"]')
html_content = table.get_attribute('outerHTML')


soup = BeautifulSoup(html_content, 'html.parser')
tabela = soup.find(name='table')

df_full = pd.read_html(str(tabela))[0]
df = df_full[['Grand Prix', 'Winner', 'Car']]
df.columns = ['gp', 'winner', 'car']

df.to_excel('winners.xlsx')

driver.quit()
