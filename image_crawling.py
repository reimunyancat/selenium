import time
import os
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from util.image_utils import (
    init_env,
    create_save_folder,
    file_extension_check,
    image_download,
    log_error,
    scroll_and_load
)
from util.browser_utils import create_driver, configure_search_settings

def main():
    pause_times, success_count = init_env()
    
    query = input("검색어 입력: ").strip()
    is_non_alpha = not query.isalpha()
    
    create_save_folder(query)
    print()
    
    num_images = int(input("수집할 이미지 개수 입력: "))
    
    extension = input("이미지 확장자 입력(1: jpg  2: png): ")
    extension = 'jpg' if extension != '2' else 'png'
    
    driver = create_driver()
    configure_search_settings(driver, pause_times['default'])
    
    driver.get("https://www.google.com/imghp")
    search_bar = driver.find_element(By.NAME, "q")
    search_bar.send_keys(query)
    search_bar.submit()
    time.sleep(pause_times['default'])
    
    scroll_and_load(driver, pause_times['scroll'])
    driver.execute_script("window.scrollTo(0, 0)")
    time.sleep(1)
    
    css_selector = ".YQ4gaf" if is_non_alpha else ".mNsIhb"
    images = driver.find_elements(By.CSS_SELECTOR, css_selector)
    print(f"\n총 {len(images)}개의 이미지를 찾았습니다.")
    
    if num_images > len(images):
        num_images = len(images)
        print(f"찾은 이미지가 요청보다 적습니다. {num_images}개만 다운로드합니다.")
    
    for i in range(num_images):
        try:
            img_element = driver.find_elements(By.CSS_SELECTOR, css_selector)[i]
            driver.execute_script("arguments[0].click();", img_element)
            time.sleep(pause_times['click'])
            
            original_img_src = get_image_source(driver, is_non_alpha)
            
            if original_img_src:
                filename = file_extension_check(original_img_src, query, i, extension)
                success = image_download(original_img_src, filename, query, i, num_images)
                if success:
                    success_count += 1
            else:
                log_error(f"이미지_{i+1}", query, i, num_images, "이미지 소스를 찾을 수 없습니다.")
                
        except Exception as e:
            log_error(f"이미지_{i+1}", query, i, num_images, e)
    
    driver.quit()
    print(f"{query} 검색어 이미지 수집 완료. 성공한 이미지 수: {success_count}")
    print("\n작업 완료 'exit' 입력시 종료, 아무거나 입력하시면 다시 반복합니다.")
    
    return input() == 'exit'

def get_image_source(driver, is_non_alpha):
    patterns = [
        '//*[@id="Sva75c"]/div[2]/div[2]/div/div[2]/c-wiz/div/div[2]/div[2]/a/img[1]',
        '/html/body/div[14]/div[2]/div[3]/div/div/c-wiz/div/div[2]/div[2]/div/div[2]/c-wiz/div/div[2]/div[2]/a/img[1]'
    ]
        
    for xpath in patterns:
        try:
            element = driver.find_element(By.XPATH, xpath)
            return element.get_attribute('src')
        except NoSuchElementException:
            continue
        except Exception:
            continue
    
    return None

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        should_exit = main()
        if should_exit:
            print("프로그램을 종료합니다...")
            break
        os.system('cls' if os.name == 'nt' else 'clear')