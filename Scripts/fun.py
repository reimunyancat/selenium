import os
import time
import random
import urllib.request
from functools import wraps
from urllib.error import URLError, HTTPError
from ssl import SSLError

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
        print(f"{query} : {i + 1}/{num_images} 이미지 다운로드 완료...")

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
    if file_extension in ['com', 'net', 'do', 'kr', 'data']:
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