import os
import time
import random
import urllib.request
from selenium.webdriver.common.by import By
from urllib.error import URLError, HTTPError
from ssl import SSLError
from functools import wraps

VALID_EXTENSIONS = ['com', 'net', 'do', 'kr', 'data', 'bmp', 'webp', 'jpg', 'png', 'jpeg', 'JPG', 'jpg&w=1920&q=100', 'id']

def init_env():
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')]
    urllib.request.install_opener(opener)
    
    pause_times = {
        'default': 0.3,
        'click': 0.3,
        'scroll': 1.5
    }
    
    return pause_times, 0

def create_save_folder(query):
    if not os.path.exists('images'):
        os.makedirs('images')
    
    save_path = f'images/{query}'
    if not os.path.exists(save_path):
        os.makedirs(save_path, exist_ok=True)
        print(f"'{query}' 폴더 생성 완료...")
    else:
        print(f"'{query}' 폴더가 이미 존재합니다.")

def file_extension_check(img_src, query, index, default_extension):
    file_extension = img_src.rsplit('.', 1)[-1].split('/', 1)[0].split('?', 1)[0]
    if file_extension in VALID_EXTENSIONS:
        file_extension = default_extension
    
    return f'images/{query}/{query}_{index + 1}.{file_extension}'

def log_error(filename, query, index, total, error_msg):
    print(f"{query}: {index + 1}/{total} - 오류: {error_msg}")

def retry(exception_to_check, tries=3, delay=2, backoff=2):
    def deco_retry(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            mtries, mdelay = tries, delay + random.random()
            while mtries > 1:
                try:
                    return func(*args, **kwargs)
                except exception_to_check as e:
                    print(f"오류 발생: {e}, {mdelay:.2f}초 후 재시도...")
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return func(*args, **kwargs)
        return wrapper
    return deco_retry

@retry((TimeoutError, URLError, HTTPError, SSLError), tries=3)
def image_download(img_src, filename, query, index, total):
    try:
        urllib.request.urlretrieve(img_src, filename)
        print(f"{query}: {index + 1}/{total} 이미지 다운로드 완료...")
        return True
    except Exception as e:
        try:
            if img_src.startswith('https'):
                http_src = img_src.replace('https', 'http')
                urllib.request.urlretrieve(http_src, filename)
                print(f"{query}: {index + 1}/{total} 이미지 다운로드 완료 (HTTP로 재시도)...")
                return True
        except Exception:
            pass
        
        log_error(filename, query, index, total, e)
        return False

def scroll_and_load(driver, pause_time):
    print("이미지 로딩 중...")
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause_time)
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            try:
                for selector in [".RVQdVd", ".mye4qd"]:
                    try:
                        load_more = driver.find_element(By.CSS_SELECTOR, selector)
                        load_more.click()
                        time.sleep(pause_time)
                        break
                    except:
                        continue
                else:
                    print("모든 이미지가 로드되었습니다.")
                    break
            except:
                print("모든 이미지가 로드되었습니다.")
                break
        
        last_height = new_height