from seleniumwire import webdriver  # Import from seleniumwire
import time

# Create a new instance of the Firefox driver
options = {
    'proxy': {
        'https': 'https://tuthixen-dest:53d8tl329rrx@45.137.40.144:80',
    }
}
driver = webdriver.Chrome('chromedriver.exe', seleniumwire_options=options)
# Go to the Google home page
driver.get('https://www.pinnacle.com/en/')
time.sleep(30)
driver.find_element_by_id('username').click()
driver.find_element_by_id('username').send_keys('AA1200771')
driver.wait_for_request('/0.1/devices', timeout=30)

for request in driver.requests:
    if request.response:
        if '/0.1/devices' in request.url:
            print(
                request.url,
                request.headers['X-API-Key'],
                request.headers['X-Device-UUID']
            )