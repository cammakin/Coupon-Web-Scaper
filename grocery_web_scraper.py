#!/usr/env python3.8.2

'''
Grocery Store Web Scraper
This program will load Kroger's Digital Coupons page and make a
Google Sheets doc with the data on each coupon including:
	*Coupon Value
	*Coupon Details/Restrictions
	*Coupon Expiration
	*Coupon Compatable Items
		*Compatible Items Price

Once the program populates the CSV, queries may be done to list
coupons by expiration, value, and show the least costly item that
pairs with the coupon thus maximizing savings on coupon

Last Modified: 03/02/2020
'''

# Following libraries were installed and used (see pip commands)
from bs4 import BeautifulSoup 			# pip install bs4
from requests_html import HTMLSession	# pip install requests-html

if __name__ == "__main__":

	print("Step 1:")	# Get HTML from website
	target_url = 'https://www.kroger.com/cl/coupons/'
	session = HTMLSession()
	response = session.get(target_url)
	print(response)
	# response.html.render()

	print("Step 2:")	# Parse Data using soup
	soup = BeautifulSoup(response.html.html, "lxml")
	print(soup.body)

	print("Step 3:")	# $$ Profit $$



