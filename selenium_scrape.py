"""
Selenium Web Scraper
"""

import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


# Scroll down to load all coupons
def load_entire_page():
    body = driver.find_element_by_css_selector('body')
    for i in range(7):
        body.send_keys(Keys.PAGE_DOWN)
        body.send_keys(Keys.PAGE_DOWN)
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.75)


# Input: coupon_popup to parse out
# Output: Coupon title, description, and expiration date
def get_coupon_details(web_driver):

    coupon_popup_obj = web_driver.find_element_by_class_name('CouponDetails-details-new')
    coupon_description = ''
    for entry in (coupon_popup_obj.find_elements_by_class_name('CouponDetails-longDescription-new')):
        coupon_description = coupon_description + ' ' + entry.text

    info = {
        'title': (coupon_popup_obj.find_element_by_class_name('CouponDetails-new-title')).text,
        'description': coupon_description,
        'num_uses': "",
        'expiration': (coupon_popup_obj.find_element_by_class_name("CouponExpiration-text")).text
    }

    # Not all coupons have an explict Num Uses, hence the try/catch structure
    try:
        info['num_uses'] = (coupon_popup_obj.find_element_by_class_name('CouponDetails-filterTagDescription')).text
    except NoSuchElementException:
        pass

    web_driver.find_element_by_class_name('CouponModal-close').click()  # Closes popup
    return info


# D:\\Downloads\\geckodriver\\geckodriver.exe
driver = webdriver.Firefox(executable_path='C:\\Users\\camma\\Downloads\\geckodriver\\geckodriver.exe')
try:
    driver.get("https://www.kroger.com/cl/coupons/")
    time.sleep(2)  # Learn the proper way to wait for a load (especially for popup)

    # Removes the popup when Digital Coupon page loads
    popup = driver.find_element_by_xpath('//button[@class="kds-Button kds-Button--primaryInverse kds-Button--hasIconOnly ModalitySelectorTooltip-CloseButton"]')
    popup.click()

    # time.sleep(4)  # More loading time

    # Scroll down to load all coupons
    # load_entire_page()

    # Create CSV file for data export
    # myFile = open('example2.csv', 'w')

    # Load a list of all coupons
    for coupon_tile in driver.find_elements_by_class_name("CouponCard-content"):
        coupon_tile.find_element_by_tag_name("p").click()  # open coupon popup with more details
        coupon_popup = driver.find_element_by_class_name('CouponDetails-details-new')
        coupon_details = get_coupon_details(driver)

        data = '"{}", "{}", "{}", "{}"\n'.format(coupon_details['title'], coupon_details['description'],
                                                 coupon_details['num_uses'], coupon_details['expiration'])

        print(data)
    #     myFile.write(data)

    time.sleep(10)
    # print("Writing complete")
    # myFile.close()

finally:
    driver.quit()

# with webdriver.Firefox(executable_path='D:\\Downloads\\geckodriver\\geckodriver.exe') as driver:
    # Webdriver code here
# Web driver automatically closes after operation