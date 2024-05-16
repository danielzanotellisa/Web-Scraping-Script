import pickle
from selenium import webdriver
from time import sleep

url = 'https://www.formula1.com/'
browser = webdriver.Firefox()


browser.get(url)
sleep(3)
cookies = browser.get_cookies()


pickle.dump(cookies, open('f1_cookies.pkl', 'wb'))


browser.close()