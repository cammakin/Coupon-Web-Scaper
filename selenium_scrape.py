"""
Selenium Web Scraper
"""

import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


# Use this method if the HTML element may or may not be present
def safe_data_scrape(web_driver, class_name):
    try:
        return web_driver.find_element_by_class_name(class_name).text
    except NoSuchElementException:
        return ''


# Scroll down to load all coupons
def load_entire_page(webpage_body):
    for i in range(7):
        webpage_body.send_keys(Keys.PAGE_DOWN)
        webpage_body.send_keys(Keys.PAGE_DOWN)
        webpage_body.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.75)


# Input:  web_driver to use for scraping
# Output: Coupon title, description, number of uses, and expiration date
def get_coupon_details(web_driver):

    # Gets entire coupon popup window
    coupon_popup_obj = web_driver.find_element_by_class_name('CouponDetails-details-new')

    # Get full coupon description
    coupon_description = ''
    for entry in (coupon_popup_obj.find_elements_by_class_name('CouponDetails-longDescription-new')):
        coupon_description = coupon_description + ' ' + entry.text

    # Dictionary of data for the entire coupon
    info = {'title': safe_data_scrape(coupon_popup_obj, 'CouponDetails-new-title'),
            'description': coupon_description[1:],
            'num_uses': safe_data_scrape(coupon_popup_obj, 'CouponDetails-filterTagDescription'),
            'min_items_for_use': safe_data_scrape(coupon_popup_obj, 'CouponsProgressBar-productsCount'),
            'expiration': safe_data_scrape(coupon_popup_obj, 'CouponExpiration-text'),
            'qualifying_products': []}

    # Grabs info for qualifying products
    qualifying_products = web_driver.find_elements_by_class_name('ProductCardList')  # List of qualifying products
    for product in qualifying_products:
        qualifying_product = {
            'name': safe_data_scrape(product, 'ProductCardList-name'),
            'volume': safe_data_scrape(product, 'ProductCardList-sellBy-unit'),
            'promo_price': safe_data_scrape(product, 'kds-Price-promotional'),
            'original_price': safe_data_scrape(product, 'kds-Price-original')}
        info['qualifying_products'].append(qualifying_product)   # Adds qualifying product to coupon details dict

    # Closes popup and returns all coupon info
    web_driver.find_element_by_class_name('CouponModal-close').click()
    return info


def main():
    # D:\\Downloads\\geckodriver\\geckodriver.exe
    executable_path_to_driver = 'C:\\Users\\camma\\Downloads\\geckodriver\\geckodriver.exe'
    driver = webdriver.Firefox(executable_path=executable_path_to_driver)
    try:
        driver.get("https://www.kroger.com/cl/coupons/")
        time.sleep(2)  # Learn the proper way to wait for a load (especially for popup)

        # Removes the popup when Digital Coupon page loads
        popup = driver.find_element_by_xpath('//button[@class="kds-Button kds-Button--primaryInverse kds-Button--hasIconOnly ModalitySelectorTooltip-CloseButton"]')
        popup.click()

        # time.sleep(4)  # More loading time

        # Scroll down to load all coupons
        # load_entire_page(driver.find_element_by_css_selector('body'))

        # Create CSV file for data export
        # myFile = open('example2.csv', 'w')

        # Load a list of all coupons
        for coupon_tile in driver.find_elements_by_class_name("CouponCard-content"):
            coupon_tile.find_element_by_tag_name("p").click()  # open coupon popup with more details
            time.sleep(3)
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


if __name__ == "__main__":
    main()


# with webdriver.Firefox(executable_path='D:\\Downloads\\geckodriver\\geckodriver.exe') as driver:
    # Webdriver code here
# Web driver automatically closes after operation
