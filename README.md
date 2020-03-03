# Grocery Store Web Scraper

This program will load Kroger's [Digital Coupons](https://www.kroger.com/cl/coupons/) page and make a
Google Sheets doc with the data on each coupon including:
  - Coupon Value
  - Coupon Details/Restrictions
  - Coupon Expiration
  - Coupon Compatable Items
    - Compatible Items Price

Once the program populates the CSV, queries may be done to list
coupons by expiration, value, and show the least costly item that
pairs with the coupon thus maximizing savings on coupon

### How to Use it

The web scraper requires 2 packages: [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) and [requests_html](https://pypi.org/project/requests-html/) to run.


```sh
$ pip install bs4
$ pip install requests-html
```

Then run the script
...

### Todos

 - Parse out data
 - Include other grocery stores
 - Include full usage tutorial

