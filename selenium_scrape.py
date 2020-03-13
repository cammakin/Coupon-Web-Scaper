"""
Selenium Web Scraper
"""

import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


def extract_min_items(description):
    """
    Takes the description of a product and extracts the minimum number of items
        that must be purchased to use the coupon
    :param description: Text description of the coupon (string)
    :return min_items: Minimum # of items for coupon to work (int)
    """
    min_items_begin = description.find(' (')
    if min_items_begin < 0:  # If there is no (#), then just return 0, else continue
        return 0
    min_items_end = description[min_items_begin:min_items_begin + 6].find(') ')
    if min_items_end < 0:
        return 0
    min_items = int(description[min_items_begin+2:min_items_begin+min_items_end])
    return min_items


def get_qualifying_product_price(product):
    """
    Since there are 3 different ways prices are listed,
        this method checks for the current price of the item
    :param product: Product (webdriver object)
    :return price:  Price for product (float)
    """
    # Scrape for a promo price on the product
    item_price = safe_data_scrape(product, 'kds-Price-promotional')

    # If there is no promo price, then scrape the singular price
    if not item_price:
        item_price = safe_data_scrape(product, 'kds-Price-singular')

    # In the event that there is no price (i.e. 'Prices May Vary'), return 0
    if item_price:
        price = float(item_price[1:])
    else:
        price = 0
    return price


def extract_discount(title):
    """
    Searches the title string for the $ off value
    :param title: Coupon title (string)
    :return discount: Decimal value of the coupon (float)
    """
    pointer = title.find('ave $')
    if not pointer == -1:
        discount = float(title[pointer+5:pointer+9])
    else:
        discount = 0
    return discount


def safe_data_scrape(web_driver, class_name):
    """
    Use this method if the HTML element may or may not be present
    :param web_driver: HTML Element to Scrape (webdriver object)
    :param class_name: Class to search for (string)
    :return: Text associated with the given class_name
    """
    try:
        return web_driver.find_element_by_class_name(class_name).text
    except NoSuchElementException:
        return ''


def load_entire_page(webpage_body):
    """
    Scroll down to load all coupons
    :param webpage_body: Body of element to send PAGE_DOWN command to (webdriver object)
    """
    for i in range(7):
        webpage_body.send_keys(Keys.PAGE_DOWN)
        webpage_body.send_keys(Keys.PAGE_DOWN)
        webpage_body.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.75)


def get_coupon_details(web_driver):
    """
    Input:  web_driver to use for scraping
    Output: Coupon title, description, number of uses, and expiration date
    """

    # Gets entire coupon popup window
    coupon_popup_obj = web_driver.find_element_by_class_name('CouponDetails-details-new')

    # Get full coupon description
    coupon_description = ''
    for entry in (coupon_popup_obj.find_elements_by_class_name('CouponDetails-longDescription-new')):
        coupon_description = coupon_description + ' ' + entry.text

    # Dictionary of data for the entire coupon
    info = {'title': safe_data_scrape(coupon_popup_obj, 'CouponDetails-new-title'),
            'description': coupon_description[1:],
            'coupon_value': '',
            'num_uses': safe_data_scrape(coupon_popup_obj, 'CouponDetails-filterTagDescription'),
            'min_items_for_use': '',
            'expiration': safe_data_scrape(coupon_popup_obj, 'CouponExpiration-text'),
            'qualifying_products': [],
            'best_product': [],
            'final_price': ''}

    # Extracts coupon value
    info['coupon_value'] = extract_discount(info['title'])

    # Extract the min # of items required
    info['min_items_for_use'] = extract_min_items(info['description'])

    # Grabs info for qualifying products
    best_price = 100
    qualifying_products = web_driver.find_elements_by_class_name('ProductCardList')  # List of qualifying products
    for product in qualifying_products:
        qualifying_product = {
            'name': safe_data_scrape(product, 'ProductCardList-name'),
            'volume': safe_data_scrape(product, 'ProductCardList-sellBy-unit'),
            'price': get_qualifying_product_price(product)
        }

        info['qualifying_products'].append(qualifying_product)   # Adds qualifying product to coupon details dict
        if qualifying_product['price'] < best_price and not qualifying_product['price'] == 0:
            best_price = qualifying_product['price']
            info['best_product'] = qualifying_product
        info['final_price'] = (best_price * info['min_items_for_use']) - info['coupon_value']

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
        popup = driver.find_element_by_class_name("DynamicTooltip--Button--Confirm")
        popup.click()

        time.sleep(2)  # More loading time

        # Scroll down to load all coupons
        load_entire_page(driver.find_element_by_css_selector('body'))

        # Create CSV file for data export
        # myFile = open('example2.csv', 'w')

        # Load a list of all coupons
        for coupon_tile in driver.find_elements_by_class_name("CouponCard-content"):
            coupon_tile.find_element_by_tag_name("p").click()  # open coupon popup with more details
            time.sleep(2)
            coupon_details = get_coupon_details(driver)

            data = ''
            if coupon_details['final_price']:
                data = '"{}"\n"{} {} - ${:,.2f}"\n\n'.format(
                    coupon_details['title'], coupon_details['best_product']['name'],
                    coupon_details['best_product']['volume'], coupon_details['final_price'])

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
