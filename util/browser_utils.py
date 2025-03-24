import time
from selenium import webdriver
from selenium.webdriver.common.by import By

def create_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument('--window-size=1920,1080')
    
    return webdriver.Chrome(options=chrome_options)

def configure_search_settings(driver, pause_time):
    try:
        driver.get("https://www.google.com/preferences?hl=ko&prev=https://www.google.com/search?q%3D%25E3%2585%2587%26sca_esv%3Dcde25c42fe00d5a3%26sca_upv%3D1#tabVal=1")
        time.sleep(pause_time)
        
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(2) > div.iORcjf > div:nth-child(2) > div:nth-child(2) > div.HrFxGf > div > div > div > div").click()
        time.sleep(pause_time)
        
        driver.find_element(By.CSS_SELECTOR, "body > div.iORcjf > div:nth-child(2) > div > div:nth-child(2) > div > div:nth-child(2) > div > div:nth-child(2) > div.HrqWPb > div").click()
        time.sleep(pause_time)
        
        region_input = driver.find_element(By.CSS_SELECTOR, "#lb > div > div.mcPPZ.nP0TDe.xg7rAe.ivkdbf > span > div > g-text-field > div.WO1lOd > div.FFTibe > input")
        region_input.click()
        time.sleep(pause_time)
        region_input.send_keys("미국")
        
        driver.find_element(By.CSS_SELECTOR, "#lb > div > div.mcPPZ.nP0TDe.xg7rAe.ivkdbf > span > div > g-menu > g-menu-item:nth-child(53) > div").click()
        time.sleep(pause_time)
        
        driver.find_element(By.CSS_SELECTOR, "#lb > div > div.mcPPZ.nP0TDe.xg7rAe.ivkdbf > span > div > div.JhVSze > span:nth-child(2)").click()
        time.sleep(pause_time)
        
        driver.get("https://www.google.com/preferences?hl=ko&prev=https://www.google.com/search%3Fq%3D%25E3%2585%2587%26sca_esv%3Dcde25c42fe00d5a3%26sca_upv%3D1")
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(2) > div.iORcjf > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div > div > div > div").click()
        time.sleep(pause_time)
        
        driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/g-radio-button-group/div[3]/div[3]").click()
        time.sleep(pause_time)
        
    except Exception as e:
        print(f"검색 설정 구성 중 오류 발생: {e}")
        print("기본 설정으로 계속합니다.")