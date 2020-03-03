'''
Selenium Web Scraper
'''


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Firefox(executable_path='D:\\Downloads\\geckodriver\\geckodriver.exe')

try:
    driver.get("https://www.kroger.com/cl/coupons/")
    time.sleep(4) # Learn the proper way to wait for a load

    # Removes the popup when Digital Coupon page loads
    popup = driver.find_element_by_xpath('//button[@class="kds-Button kds-Button--primaryInverse kds-Button--hasIconOnly ModalitySelectorTooltip-CloseButton"]')
    popup.click()

    time.sleep(4) # More loading time

    # Scroll down to load all coupons
    body = driver.find_element_by_css_selector('body')
    for i in range(40):
        body.send_keys(Keys.PAGE_DOWN);
        time.sleep(0.75)

    # Grab the coupon information
    # coupons = driver.find_elements_by_xpath('//li[@class="AutoGrid-cell"]')
    # for coupon in coupons:
    #     coupon_name = coupon.find_element_by_xpath('//p[@tabindex="0"]')
    #     print(coupon_name.text)

    time.sleep(10)

finally:
    driver.quit()

# with webdriver.Firefox(executable_path='D:\\Downloads\\geckodriver\\geckodriver.exe') as driver:
    # Webdriver code here
# Web driver automatically closes after operation