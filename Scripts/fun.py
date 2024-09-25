import os
import time
import random
import urllib.request
from selenium.webdriver.common.by import By
from selenium import webdriver
from functools import wraps
from urllib.error import URLError, HTTPError
from ssl import SSLError

def chrome():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument('--ignore-ssl-errors')
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def default_settings(driver, pause):
    driver.get("https://www.google.com/preferences?hl=ko&prev=https://www.google.com/search?q%3D%25E3%2585%2587%26sca_esv%3Dcde25c42fe00d5a3%26sca_upv%3D1#tabVal=1")
    time.sleep(pause)

    s1 = driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(2) > div.iORcjf > div:nth-child(2) > div:nth-child(2) > div.HrFxGf > div > div > div > div").click()
    time.sleep(pause)

    s1 = driver.find_element(By.CSS_SELECTOR, "body > div.iORcjf > div:nth-child(2) > div > div:nth-child(2) > div > div:nth-child(2) > div > div:nth-child(2) > div.HrqWPb > div").click()
    time.sleep(pause)

    s1 = driver.find_element(By.CSS_SELECTOR, "#lb > div > div.mcPPZ.nP0TDe.xg7rAe.ivkdbf > span > div > g-text-field > div.WO1lOd > div.FFTibe > input")
    s1.click()
    time.sleep(pause)
    s1.send_keys("미국")

    s1 = driver.find_element(By.CSS_SELECTOR, "#lb > div > div.mcPPZ.nP0TDe.xg7rAe.ivkdbf > span > div > g-menu > g-menu-item:nth-child(53) > div").click()
    time.sleep(pause)

    s1 = driver.find_element(By.CSS_SELECTOR, "#lb > div > div.mcPPZ.nP0TDe.xg7rAe.ivkdbf > span > div > div.JhVSze > span:nth-child(2)").click()
    time.sleep(pause)

    driver.get("https://www.google.com/preferences?hl=ko&prev=https://www.google.com/search%3Fq%3D%25E3%2585%2587%26sca_esv%3Dcde25c42fe00d5a3%26sca_upv%3D1")
    s2 = driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(2) > div.iORcjf > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div > div > div > div").click()
    time.sleep(pause)

    s2 = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/g-radio-button-group/div[3]/div[3]")
    s2.click()
    time.sleep(pause)

def scroll_and_load(driver, scroll_pause_time):
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause_time)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                try:
                    driver.find_element(By.CSS_SELECTOR, ".RVQdVd").click()
                except:
                    try:
                        driver.find_element(By.CSS_SELECTOR, ".mye4qd").click()
                    except:
                        break
            last_height = new_height


def retry(ExceptionToCheck, tries = 3, delay = 2+random.random(), backoff = 2, logger=None):
    """Retry calling the decorated function using an exponential backoff.

    http://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/
    original from: http://wiki.python.org/moin/PythonDecoratorLibrary#Retry

    :param ExceptionToCheck: the exception to check. may be a tuple of
        exceptions to check
    :type ExceptionToCheck: Exception or tuple
    :param tries: number of times to try (not retry) before giving up
    :type tries: int
    :param delay: initial delay between retries in seconds
    :type delay: int
    :param backoff: backoff multiplier e.g. value of 2 will double the delay
        each retry
    :type backoff: int
    :param logger: logger to use. If None, print
    :type logger: logging.Logger instance
    """
    def deco_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except ExceptionToCheck as e:
                    msg = f"{str(e)}, Retrying in {mdelay} seconds..."
                    print(msg)
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)
        return f_retry # true decorator
    return deco_retry

def error(filename, query, i, num_images, e):
    if not os.path.exists(filename):
        print(f"{i+1}번째 이미지 처리 중 오류 발생: {e}")
    else:
        print(f"{i + 1}/{num_images} 이미지 다운로드 완료...")

def create_save_folder(query):
    if not os.path.exists('images'):
        os.makedirs('images')
    if not os.path.exists(query):
        os.makedirs(f'images\{query}', exist_ok=True)
        print(f"'{query}' 폴더 생성 완료...")

def image_limit_check(i, num_images):
    if i >= num_images:
        return True

def file_extention_f(original_img_src, query, i):
    # 확장자 설정&파일경로 설정
    file_extension = original_img_src.rsplit('.', 1)[-1].split('/', 1)[0].split('?', 1)[0]
    if file_extension in ['com', 'net', 'do', 'kr', 'data', 'bmp', 'webp']:
        file_extension = 'png'
    filename = f'images\{query}\{query}_{i + 1}.{file_extension}'
    return filename

@retry((TimeoutError, URLError, HTTPError, SSLError), tries=3, delay=2+random.random(), backoff=2)
def image_download(original_img_src, filename, query, i, num_images):
    try:
        urllib.request.urlretrieve(original_img_src, filename)
        print(f"{query} : {i + 1}/{num_images} 이미지 다운로드 완료...")
    except Exception as e:
        try:
            original_img_src = original_img_src.replace('https', 'http')
            urllib.request.urlretrieve(original_img_src, filename)
            print(f"{query} : {i + 1}/{num_images} 이미지 다운로드 완료...")
        except Exception as e:
            error(filename, query, i, num_images, e)

def create_save_file(query):
    if not os.path.exists('texts'):
        os.makedirs('texts')
    if not os.path.exists(query):
        with open(f'texts\{query}.txt', 'w', encoding='utf-8') as f:
            f.write(f"{query} 파일 생성 완료")