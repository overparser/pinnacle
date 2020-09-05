from seleniumwire import webdriver
from document.document import get_proxy, write_line
from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options

import time

# Create a new instance of the Firefox driver

def save_token():
    proxy = get_proxy()
    options = {
        'proxy': {
            'https': f'https://{proxy}',
            'http': f'http://{proxy}',
        }
    }
    user_agent = UserAgent().random
    driver = webdriver.Chrome('Session/chromedriver.exe', seleniumwire_options=options)
    driver.header_overrides = {'User-Agent': user_agent}
    driver.get('https://pinnacle.com/')
    # driver.find_element_by_xpath('//input[@id="username"]').send_keys('AA1200771')
    # driver.find_element_by_xpath('//input[@id="password"]').send_keys('SC1pion_stavka')
    # driver.find_element_by_xpath('//button[@data-test-id="Button"][@class="style_button__19Ipo ellipsis style_small__2pIlz dead-center style_ghostOnDark__3mYd5"]').click()
    driver.wait_for_request('/0.1/devices', timeout=60)

    for request in driver.requests:
        if request.response:
            if '/0.1/devices' in request.url:
                write_line('text_files/token.csv', [request.headers['X-API-Key'], request.headers['X-Device-UUID'], user_agent, round(time.time()), proxy, 0])
                driver.close()
                break