import requests
import urllib3
import csv
from os import path
from bs4 import BeautifulSoup

exitloop = True
page = 1
# use "+" instead of spaces to enter product_name
product_name = "gift+box"
fields = ["Product Name", "Image Url", "Product Url"]
if not path.exists("amazon data.csv"):
    f = open("amazon data.csv", "a")
    writer = csv.writer(csvfile)
    writer.writerow(fields)
with open("amazon data.csv", 'a') as csvfile:
    writer = csv.writer(csvfile)
    while exitloop:
        r = requests.get('https://www.amazon.in/s', params={'k': product_name, 'page': page})
        # print(r.status_code)
        http_pool = urllib3.connection_from_url(r.url)
        r = http_pool.urlopen('GET', r.url)
        soup = BeautifulSoup(r.data, 'html.parser')
        count = 0
        for img in soup.findAll("img", {"class": "s-image"}):
                # Product
            printimg = True
            for parent in img.parents:
                try:
                    if parent["data-component-type"] == "sp-sponsored-result":
                        printimg = False
                        break
                except:
                    pass
            if printimg:
                imghref = "https://amazon.in/" + img.find_parent("a")["href"]
                data_list = [img["alt"], img["src"], imghref]
                writer.writerow(data_list)
                count += 1
        print(count, page)
        page += 1
        if count == 0:
            exitloop = False
