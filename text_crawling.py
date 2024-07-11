import time
import random
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from Scripts.fun import create_save_file

pause = random.uniform(0.4, 0.6)

# HTTP 헤더 설정
opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')]
urllib.request.install_opener(opener)


query = input("검색어 입력: ")
create_save_file(query)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument('--ignore-ssl-errors')
driver = webdriver.Chrome(options=chrome_options)

driver.get(f"https://namu.wiki/w/{query}")
time.sleep(pause)

text = ' '.join(element.text for element in driver.find_elements(By.XPATH, '/html/body/div/div/div[2]/main/div/div/div[4]/div/div[2]/div[4]/div[4]/div[5]'))

with open(f'texts\{query}.txt', 'w', encoding='utf-8') as f:
    f.write(text)

driver.quit()
