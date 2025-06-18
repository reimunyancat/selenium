import time
import random
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

# 나무위키에서 제외할 면책 조항 텍스트 목록
se = [
    '\n이 저작물은 CC BY-NC-SA 2.0 KR에 따라 이용할 수 있습니다. (단, 라이선스가 명시된 일부 문서 및 삽화 제외',
    '\n기여하신 문서의 저작권은 각 기여자에게 있으며, 각 기여자는 기여하신 부분의 저작권을 갖습니다.',
    '\n나무위키는 백과사전이 아니며 검증되지 않았거나, 편향적이거나, 잘못된 서술이 있을 수 있습니다.',
    '\n나무위키는 위키위키입니다. 여러분이 직접 문서를 고칠 수 있으며, 다른 사람의 의견을 원할 경우 직접 토론을 발제할 수 있습니다.'
]

# 텍스트 파일 저장 경로 생성 함수
def create_save_file(query):
    os.makedirs('texts', exist_ok=True)
    return f'texts/{query}.txt'

pause = random.uniform(0.5, 0.8)

opener = urllib.request.build_opener()
opener.addheaders = [
    ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')
]
urllib.request.install_opener(opener)

def create_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')

    service = Service()
    return webdriver.Chrome(service=service, options=chrome_options)

query = input("검색어 입력: ")
create_save_file(query)

driver = create_driver()
query2 = query.replace(' ', '%20')
driver.get(f"https://namu.wiki/w/{query2}")
time.sleep(pause)

try:
    # 메인 콘텐츠 요소 찾기
    main_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//*[@id="app"]/div[1]/div[2]/div/div[4]'))
    )

    # 제외할 요소 찾기
    exclude_elements = driver.find_elements(By.XPATH, '//*[@id="app"]/div[1]/div[2]/div/div[4]/div[2]/div[4]/div[6]/div[49]/div/div[4]')

    # 제외할 텍스트 목록 생성
    exclude_texts = [elem.text for elem in exclude_elements]

    text_parts = []
    for element in main_elements:
        if element.text not in exclude_texts:
            text_parts.append(element.text)

    text = ' '.join(text_parts)

    for p in ['\n[편집]', '\n편집 요청', '\n요청', '\n토론', '|']:
        text = text.replace(p, '')

    for p in se:
        text = text.replace(p, '')

    with open(f'texts/{query}.txt', 'w', encoding='utf-8') as f:
        f.write(text)

    print(f"{query} 검색어 텍스트 수집 완료...")
except Exception as e:
    print(f"오류 발생: {e}")
finally:
    driver.quit()
