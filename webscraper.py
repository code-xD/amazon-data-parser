import requests
import urllib3
import csv
import time
from os import path
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
# from urllib3.contrib.appengine import AppEngineManager
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')


def get_url_data_bot(site_url, params):
    r = requests.get(site_url, params=params)
    wd = webdriver.Chrome()
    wd.get(r.url)
    with open('code.text', 'w') as file:
        file.write(wd.page_source)
    soup = BeautifulSoup(wd.page_source, 'html.parser')
    wd.close()
    return soup


def get_url_data(site_url, params):
    #     http_pool = AppEngineManager()
    ua = UserAgent()
    r = requests.get(site_url, params=params)
    http_pool = urllib3.connection_from_url(r.url)
    r = http_pool.urlopen('GET', r.url)
    # print(r.status_code)
    # print(r.url)
    soup = BeautifulSoup(r.data, 'html.parser')
    return soup


def get_amazon_price(htmlcode):
    price = []
    try:
        prices = htmlcode.find_all('span', class_='a-price-whole')
        if len(prices) == 1:
            price.append(htmlcode.find('span', class_='a-price-whole').text)
        else:
            for pr in prices:
                pr = pr.text
                price.append(pr)
                if pr.parent.parent['data-a-strike'] == 'true':
                    price.pop()
    except:
        try:
            print('exception')
            price_raw = htmlcode.find_all('div', class_='sg-row')[1]
            price_raw = price_raw.find_all('div', class_='sg-row')[1]
            price_raw = price_raw.find_all('div', class_='a-section')[1]
            price[0] = price = price_raw.find('span', class_='a-color-base').text[1:]
            print(price)
        except:
            print('uncaught')
    return price


def get_amazon_data(product_name, site_url, country, category=None):
    exitloop = True
    page = 1
    print('called')
    while exitloop:
        if category is None:
            soup = get_url_data_bot(site_url+'/s', {'k': product_name, 'page': page})
        else:
            print('category')
            soup = get_url_data_bot(
                site_url+'/s', {'k': product_name, 'page': page, 'i': category})
        soup = soup.find('div', {'class': 's-result-list'})
        # print(soup)
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
                hash = ahref['href']
                ahref = site_url+ahref['href']
                price = get_amazon_price(product)
                try:
                    rnr = product.find('div', class_="a-row a-size-small")
                    rating = rnr.find('span', class_='a-icon-alt').text
                    review = rnr.find('span', class_='a-size-base').text
                except:
                    pass
                rmk = ''
                try:
                    remarks = product.find_all('span', class_='a-badge-text')
                    for remark in remarks:
                        rmk += str(remark.text)+' '
                    print(rmk)
                except:
                    pass
                prod_name = ''
                if hash != '#':
                    for ch in img['alt']:
                        if ch == ';':
                            ch = ' '
                        prod_name += ch
                    for i in range(len(price)):
                        yield {'Product Name': prod_name, 'Image URL': img['src'], 'Product URL': ahref, 'Ratings': rating, 'No: of Responses': review, 'price': price[i], 'country': country, 'remark': rmk}
                else:
                    list = product.find('span', {'cel_widget_id': 'osp-search'})
                    remark = list.find('span', {'class': 'a-size-large'}).text
                    itr = 0
                    for card in list.find_all('li', {'class': 'a-carousel-card'}):
                        if itr == 0:
                            itr += 1
                            continue
                        rmk = card.find('span', {'class': 'a-size-base-plus'}).text
                        img = card.find('span', {'data-component-type': 's-product-image'})
                        href = site_url+img.find('a', {'class': 'a-link-normal'})['href']
                        prod_name = ''
                        for ch in img.find('img')['alt']:
                            if ch == ';':
                                ch = ' '
                            prod_name += ch
                        img_url = img.find('img')['src']
                        price = get_amazon_price(card)
                        try:
                            rnr = card.find('div', class_="a-row a-size-small")
                            rating = rnr.find('span', class_='a-icon-alt').text
                            review = rnr.find('span', class_='a-size-base').text
                        except:
                            pass
                        for i in range(len(price)):
                            yield {'Product Name': prod_name, 'Image URL': img_url, 'Product URL': href, 'Ratings': rating, 'No: of Responses': review, 'price': price[i], 'country': country, 'remark': remark+' '+rmk}
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


def get_alibaba_data(product_name):
    page = 1
    cont = True
    print('alibaba')
    while cont:
        try:
            print('try')
            soup = get_url_data('https://www.alibaba.com/trade/search',
                                {'SearchText': product_name, 'page': page, 'CatId': '1', 'fsb': 'y', 'IndexArea': 'product_en', 'viewtype': 'G'})
            products = soup.find_all('div', class_='m-gallery-product-item-v2')
            products[0].text
            for product in products:
                try:
                    img = product.find('img')  # title,https:+img_url
                    href = 'https:'+product.find('a')['href']
                    price = product.find('div', class_='price').b.text
                    price = price.replace(' ', '')
                    price = price.replace('\n', '')
                    rating = 'No ratings Provided'
                    responses = 'No responses available'
                    try:
                        rating = product.find('span', class_='list-item__company-record-num').text
                        rating = rating.replace(' ', '')
                        rating = rating.replace('\n', '')
                        rating = eval(rating)
                        responses = product.find(
                            'span', class_='li-reviews-score__review-count').text
                        responses = responses.replace(' ', '')
                        responses = responses.replace('\n', '')
                        resp = ''
                        for ch in responses:
                            if ch.isdigit():
                                resp += ch
                        print(rating, resp)
                    except:
                        print('exception')
                    yield {'Product Name': img['alt'], 'Image URL': 'https:'+img['src'], 'Product URL': href, 'Ratings': rating, 'No: of Responses': resp, 'price': price, 'country': 'International'}
                except:
                    pass
        except:
            print('except')
            break
        page += 1
        print(page)


def get_etsy_data(product_name):
    exitloop = True
    page = 1
    while exitloop:
        soup = get_url_data('https://www.etsy.com/in-en/search?',
                            {'q': product_name, 'page': page})
        try:
            txt = soup.find('a', attrs={'data-listing-id': True}).text
            for product in soup.find_all('a', attrs={'data-listing-id': True}):
                href = product['href']
                img = product.find('img')  # title,imgurl
                rating = 'No ratings Provided'
                responses = 'No responses available'
                price = product.find('span', class_='currency-value').text
                try:
                    rnr = product.find('span', class_='v2-listing-card__rating')
                    rating = rnr.find('input')['value']
                    responses = rnr.find('span', class_='text-body-smaller').text[1:-1]
                    yield {'Product Name': product['title'], 'Image URL': img['src'], 'Product URL': href, 'Ratings': rating, 'No: of Responses': responses, 'price': price, 'country': 'United States'}
                except:
                    pass
        except:
            exitloop = False
        page += 1
        print(page)


if __name__ == '__main__':
    fields = ['Product Name', 'Image URL', 'Product URL',
              'price', 'Ratings', 'No: of Responses', 'country', 'remark']
    if not path.exists("E-commerce Data.csv"):
        f = open("E-commerce Data.csv", "a")
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        f.close()
    with open('E-commerce Data.csv', 'a') as csvfile:
        print('data')
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        for data in get_amazon_data('dog bowl', get_country_amazon('United States'), 'United States'):
            writer.writerow(data)
