from requests import get
from time import sleep, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_argument('--headless=new')
driver = webdriver.Chrome(options=options)
last_request = time()

def get_selenium_wrapper(url, xpath):
    global last_request
    # Verify last request was 3 seconds ago
    if 0 < time() - last_request < 3:
        sleep(3)
    last_request = time()
    try:
        driver.get(url)
        element = driver.find_element(By.XPATH, xpath)
        return f'<table>{element.get_attribute("innerHTML")}</table>'
    except:
        print('Error obtaining data table.')
        return None

def get_wrapper(url):
    global last_request
    # Verify last request was 3 seconds ago
    if 0 < time() - last_request < 3:
        sleep(3)
    last_request = time()
    r = get(url)
    while True:
        if r.status_code == 200:
            return r
        elif r.status_code == 429:
            retry_time = int(r.headers["Retry-After"])
            print(f'Retrying after {retry_time} sec...')
            sleep(retry_time)
        else:
            return r