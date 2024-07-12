import time
import random
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from Scripts.fun import chrome, create_save_file

pause = random.uniform(0.4, 0.8)

# HTTP 헤더 설정
opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')]
urllib.request.install_opener(opener)

while True:
    query = input("검색어 입력: ")
    create_save_file(query)

    driver = chrome()

    query2 = query.replace(' ', '%20')
    driver.get(f"https://namu.wiki/w/{query2}")
    time.sleep(pause)

    text = ' '.join(element.text for element in driver.find_elements(By.XPATH, '/html/body/div/div/div[2]/main/div/div/div[4]/div'))

    with open(f'texts\{query}.txt', 'w', encoding='utf-8') as f:
        f.write(text)

    driver.quit()
    print(f"{query} 검색어 텍스트 수집 완료...")
    print("작업 완료 'exit' 입력시 종료 아무거나 입력하시면 다시 반복합니다.")
    wa = input()
    if wa == 'exit':
        print("종료중...")
        break
