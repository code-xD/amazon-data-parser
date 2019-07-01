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


def get_amazon_data(product_name, site_url, country):
    exitloop = True
    page = 1
    print('called')
    while exitloop:
        soup = get_url_data(site_url+'/s', {'k': product_name, 'page': page})
        count = 0
        for product in soup.find_all("div", {"data-asin": True}):
            print('loop')
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
                    prices = product.find_all('span', class_='a-price-whole')
                    if len(prices) == 1:
                        price = product.find('span', class_='a-price-whole').text
                    else:
                        price = []
                        for pr in prices:
                            pr = pr.text
                            price.append(pr)
                except:
                    try:
                        print('exception')
                        price_raw = product.find_all('div', class_='sg-row')[1]
                        price_raw = price_raw.find_all('div', class_='sg-row')[1]
                        price_raw = price_raw.find_all('div', class_='a-section')[1]
                        price = price = price_raw.find('span', class_='a-color-base').text[1:]
                        print(price)
                    except:
                        print('uncaught')
                try:
                    rnr = product.find('div', class_="a-row a-size-small")
                    rating = rnr.find('span', class_='a-icon-alt').text
                    review = rnr.find('span', class_='a-size-base').text
                except:
                    pass
                yield {'Product Name': img['alt'], 'Image URL': img['src'], 'Product URL': ahref, 'Ratings': rating, 'No: of Responses': review, 'price': price, 'country': country}
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
                yield {'Product Name': img['alt'], 'Image URL': img['src'], 'Product URL': href, 'Ratings': rating, 'No: of Responses': responses, 'price': price, 'country': 'India'}
            print(page)
        except:
            print('exception')
            exitloop = False
        page += 1


def get_snapdeal_data(product_name):
    soup = get_url_data('https://www.snapdeal.com/search',
                        {'keyword': product_name, 'sort': 'plrty'})
    count = 1
    total = int(soup.find('div', class_='search-result-txt-section').text.split(' ')[2])
    while count < total:
        soup = get_url_data('https://www.snapdeal.com/search',
                            {'keyword': product_name, 'sort': 'plrty', 'start': count})
        for product in soup.find_all('div', {'data-islive': 'true'}):
            try:
                desc = product.find('div', {'class': 'product-desc-rating'})
                href = desc.find('a')['href']
                product_pool = urllib3.connection_from_url(href)
                r = product_pool.urlopen('GET', href)
                product_soup = BeautifulSoup(r.data, 'html.parser')
                img = product_soup.find('img', class_='cloudzoom')
                try:
                    price = product_soup.find('span', class_='payBlkBig').text
                except:
                    price = 'Price Not available'
                rating = 'No ratings Provided'
                responses = 'No responses available'
                try:
                    rating = product_soup.find('span', class_='avrg-rating').text[1:4]
                    responses = product_soup.find(
                        'span', {'itemprop': 'ratingCount'}).text + product_soup.find('span', {'itemprop': 'reviewCount'}).text
                    # print(img['src'], img['title'], price, rating, responses)
                except:
                    pass
                count += 1
                yield {'Product Name': img['title'], 'Image URL': img['src'], 'Product URL': href, 'Ratings': rating, 'No: of Responses': responses, 'price': price, 'country': 'India'}
            except:
                count += 1
                pass


def get_country_amazon(country):
    country_dict = {
        'China'	: 'amazon.cn',
        'India'	: 'amazon.in',
        'Japan'	: 'amazon.co.jp',
        'Singapore'	: 'amazon.com.sg',
        'Turkey'	: 'amazon.com.tr',
        'United Arab Emirates'	: 'amazon.ae',
        'France'	: 'amazon.fr',
        'Germany'	: 'amazon.de',
        'Italy'	: 'amazon.it',
        'Netherlands':	'amazon.nl',
        'Spain':	'amazon.es'	,
        'United Kingdom':	'amazon.co.uk',
        'Canada':	'amazon.ca',
        'Mexico':	'amazon.com.mx',
        'United States':	'amazon.com',
        'Australia':	'amazon.com.au',
        'Brazil':	'amazon.com.br'
    }
    url = 'http://'+country_dict.get(country)
    return url


if __name__ == '__main__':
    fields = ['Product Name', 'Image URL', 'Product URL',
              'price', 'Ratings', 'No: of Responses', 'country']
    if not path.exists("E-commerce Data.csv"):
        f = open("E-commerce Data.csv", "a")
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        f.close()
    with open('E-commerce Data.csv', 'a') as csvfile:
        for data in get_amazon_data('ps4', get_country_amazon('United Kingdom'), 'United Kingdom'):
            print('data')
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            writer.writerow(data)
