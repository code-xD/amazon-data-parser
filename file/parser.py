from bs4 import BeautifulSoup
import urllib3
import requests
import time
from .connections import get_url_data, get_url_data_bot, initbot
from billiard import Pool

# wd = initbot()


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
            # print('exception')
            price_raw = htmlcode.find_all('div', class_='sg-row')[1]
            price_raw = price_raw.find_all('div', class_='sg-row')[1]
            price_raw = price_raw.find_all('div', class_='a-section')[1]
            price[0] = price = price_raw.find('span', class_='a-color-base').text[1:]
            print(price)
        except:
            pass
            # print('uncaught')
    return price


option = 0


def get_amazon_ranking(href):
    global option
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
    product_pool = urllib3.PoolManager(timeout=10)
    r = product_pool.urlopen('GET', href)
    soup = BeautifulSoup(r.data, 'lxml')
    ranking = soup.find('table', {'id': 'productDetails_detailBullets_sections1'})
    if ranking is None:
        ranking = soup.find('li', {'id': 'SalesRank'})
        if ranking is None:
            print('not found')
            ranks = []
        else:
            ranking = ranking.text
            flag = 0
            ranks = []
            rank_no = ''
            for ch in ranking:
                if ch == '#':
                    rank_no = ''
                    flag = 1
                    continue
                if flag == 1:
                    if ch.isdigit():
                        rank_no += ch
                    else:
                        ranks.append(rank_no)
                        flag = 0
    else:
        ranks = ranking.find_all('th')
        final_rank = ''
        for rank in ranks:
            if 'Best Sellers Rank' in rank.text:
                final_rank = rank.parent.find('td').text
                break
        flag = 0
        ranks = []
        rank_no = ''
        for ch in final_rank:
            if ch == '#':
                flag = 1
            if flag == 1:
                if ch != ' ':
                    rank_no += ch
                else:
                    ranks.append(rank_no[1:])
                    rank_no = ''
                    flag = 0
    print(ranks)
    return ranks


def get_amazon_data(product_name, country, category=None):
    exitloop = True
    page = 1
    global wd
    site_url = get_country_amazon(country)
    while exitloop:
        try:
            print(page)
            if category is None:
                soup = get_url_data(site_url+'/s', {'k': product_name, 'page': page})
            else:
                # print('category')
                soup = get_url_data(
                    site_url+'/s',  {'k': product_name,  'page': page, 'i': category})
            soup = soup.find('div', {'class': 's-result-list'})
            # print(soup)
            count = 0
            main_count = 0
            product_dict = []
            href_list = []
            for product in soup.find_all("div", {"data-asin": True}):
                # print('loop')
                sponsored = False
                for tag in product.find_all('div'):
                    try:
                        if tag["data-component-type"] == "sp-sponsored-result":
                            sponsored = True
                            break
                    except:
                        pass
                if not sponsored:
                    rating = 0
                    review = 0
                    count += 1
                    img = product.find('img')
                    ahref = img.parent.parent
                    hash = ahref['href']
                    ahref = site_url+ahref['href']
                    # print(ahref)
                    price = get_amazon_price(product)
                    try:
                        rnr = product.find('div', class_="a-row a-size-small")
                        rating = rnr.find('span', class_='a-icon-alt').text.split()[0]
                        review = rnr.find('span', class_='a-size-base').text
                    except:
                        pass
                    rmk = None
                    try:
                        remarks = product.find_all('span', class_='a-badge-text')
                        for remark in remarks:
                            rmk += str(remark.text)+' '
                        # print(rmk)
                    except:
                        pass
                    prod_name = ''
                    if hash != '#':
                        for ch in img['alt']:
                            if ch == ';':
                                ch = ' '
                            prod_name += ch
                        for i in range(len(price)):
                            main_count += 1
                            href_list.append(ahref)
                            product_dict.append([prod_name,  img['src'],  ahref,
                                                rating,  review, price[i],  country, rmk])
                    else:
                        list = product.find('span', {'cel_widget_id': 'osp-search'})
                        remark = list.find('span', {'class': 'a-size-large'}).text
                        itr = 0
                        for card in list.find_all('li', {'class': 'a-carousel-card'}):
                            if itr == 0:
                                itr += 1
                                continue
                            count += 1
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
                                rating = rnr.find('span', class_='a-icon-alt').text.split()[0]
                                review = rnr.find('span', class_='a-size-base').text
                            except:
                                pass
                            for i in range(len(price)):
                                main_count += 1
                                href_list.append(href)
                                if rmk is None or rmk.strip() == '':
                                    rmk = 'None'
                                product_dict.append(
                                    [prod_name,  img_url, href,  rating, review, price[i],  country,  rmk])
        except:
            break
        if len(href_list) != 0:
            p = Pool(len(href_list))  # Pool tells how many at a time
            records = p.map(get_amazon_ranking, href_list)
            p.terminate()
            p.join()
            for i in range(len(href_list)):
                if records[i]!=[]:
                    product_dict[i].append(int(''.join(min(records[i]).split(','))))
                else:
                    product_dict[i].append(0)
                product_dict[i].append(len(records[i]))
                yield product_dict[i]
            if count == 0:
                exitloop = False
            print(count, page)
            page += 1
        else:
            exitloop = False   


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
                yield [img['alt'],  img['src'], href, rating,  responses, price, 'India']
            print(page)
        except:
            print('exception')
            exitloop = False
        page += 1


def get_snapdeal_data(product_name):
    soup = get_url_data('https://www.snapdeal.com/search?keyword='+product_name+'&sort='+'plrty')
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
                yield [img['title'], img['src'],  href,  rating,  responses,  price, 'India']
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
                                {'SearchText': product_name, 'page': page, 'CatId': '', 'fsb': 'y', 'IndexArea': 'product_en', 'viewtype': 'G'})
            products = soup.find_all('div', class_='m-gallery-product-item-v2')
            products[0].text
            for product in products:
                try:
                    img = product.find('img')  # title,https:+img_url
                    href = 'https:'+product.find('a')['href']
                    title = product.find(
                        'p', class_="organic-gallery-title__content").text
                    price = product.find('div', class_='organic-gallery-offer-section__price').p['title']
                    print(price)
                    price = price.replace(' ', '')
                    price = price.replace('\n', '')
                    lst = price.split('-')
                    obj1=obj2=''
                    for ch in lst[0]:
                        if ch.isdigit() or ch == '.':
                            obj1+=ch
                    obj1 = float(obj1)
                    for ch in lst[1]:
                        if ch.isdigit() or ch == '.':
                            obj2+=ch
                    obj2 = float(obj2)
                    price = (obj1+obj2)/2
                    print("price",price)
                    rating = 0
                    responses = 0
                    resp = 0
                    try:
                        rating = product.find(
                            'span', class_='seb-supplier-review__score').text
                        rating = rating.replace(' ', '')
                        rating = rating.replace('\n', '')
                        rating = eval(rating)
                        responses = product.find(
                            'span', class_='seb-supplier-review__review-count').text
                        responses = responses.replace(' ', '')
                        responses = responses.replace('\n', '')
                        resp = ''
                        for ch in responses:
                            if ch.isdigit():
                                resp += ch
                        print("rnr",rating, resp)
                    except:
                        print('exception')
                    data = [title, 'https:'+img['src'], href, rating, resp,  str(price), 'International']
                    print(data)
                    yield data
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
                price = price.replace(',', '')
                try:
                    rnr = product.find('span', class_='v2-listing-card__rating')
                    rating = rnr.find('input')['value']
                    responses = rnr.find('span', class_='text-body-smaller').text[1:-1]
                    responses = responses.replace(',', '')
                    yield [product['title'], img['src'],  href, rating, responses, price, 'United States']
                except:
                    pass
        except:
            exitloop = False
        page += 1
        print(page)
