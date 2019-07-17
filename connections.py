import requests
import urllib3
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')


def get_url_data_bot(site_url, params=None):
    r = requests.get(site_url, params=params)
    wd = webdriver.Chrome()
    wd.get(r.url)
    with open('code.text', 'w') as file:
        file.write(wd.page_source)
    soup = BeautifulSoup(wd.page_source, 'html.parser')
    wd.close()
    return soup


def get_url_data(site_url, params=None):
    #     http_pool = AppEngineManager()
    ua = UserAgent()
    r = requests.get(site_url, params=params)
    http_pool = urllib3.connection_from_url(r.url)
    r = http_pool.urlopen('GET', r.url)
    # print(r.status_code)
    # print(r.url)
    soup = BeautifulSoup(r.data, 'html.parser')
    return soup