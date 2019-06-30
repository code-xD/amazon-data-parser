import requests
import urllib3
import csv
from os import path
from bs4 import BeautifulSoup


def get_url_data(site_url, params):
    r = requests.get(site_url, params=params)
    # print(r.status_code)
    http_pool = urllib3.connection_from_url(r.url)
    r = http_pool.urlopen('GET', r.url)
    soup = BeautifulSoup(r.data, 'html.parser')
    return soup


def get_amazon_data(product_name):
    exitloop = True
    page = 1
    while exitloop:
        soup = get_url_data('https://www.amazon.in/s', {'k': product_name, 'page': page})
        count = 0
        for product in soup.find_all("div", {"data-asin": True}):
            sponsored = False
            for tag in product.find_all('div'):
                try:
                    if tag["data-component-type"] == "sp-sponsored-result":
                        sponsored = True
                        break
                except:
                    pass
            if not sponsored:
                rating = 'No ratings Provided'
                review = 'No responses available'
                count += 1
                img = product.find('img')
                ahref = product.find('a')
                ahref = 'https://www.amazon.in/'+ahref['href']
                price = 'price not provided.'
                try:
                    price = product.find('span', class_='a-price-whole').text
                except:
                    pass
                try:
                    rnr = product.find('div', class_="a-row a-size-small")
                    rating = rnr.find('span', class_='a-icon-alt').text
                    review = rnr.find('span', class_='a-size-base').text
                except:
                    pass
                yield {'Product Name': img['alt'], 'Image URL': img['src'], 'Product URL': ahref, 'Ratings': rating, 'No: of Responses': review, 'price': price}
        if count == 0:
            exitloop = False
        print(count, page)
        page += 1


def get_flipkart_data(product_name):
    exitloop = True
    page = 1
    while exitloop:
        soup = get_url_data('https://www.flipkart.com/search', {'q': product_name, 'page': page})
        try:
            soup.find('div', {'data-id': True}).text
            for product in soup.find_all('div', {'data-id': True}):
                href = product.find('a', class_="Zhf2z-")['href']
                href = 'https://www.flipkart.com'+href
                img = product.find('img', {'class': "_1Nyybr"})  # Product Name,Image Url
                price = product.find('div', class_="_1vC4OE").text
                rating = 'No ratings Provided'
                responses = 'No responses available'
                try:
                    rating = product.find('div', class_='hGSR34').text
                    responses = product.find('span', class_='_38sUEc').text[1:-1]
                except:
                    pass
                yield {'Product Name': img['alt'], 'Image URL': img['src'], 'Product URL': href, 'Ratings': rating, 'No: of Responses': responses, 'price': price}
            print(page)
        except:
            print('exception')
            exitloop = False
        page += 1


if __name__ == '__main__':
    for data in get_flipkart_data('playstation 4'):
        print(data)
