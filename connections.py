import requests
import urllib3
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver


def get_url_data_bot(site_url, wd, params=None):
    r = requests.get(site_url, params=params)
    wd.get(r.url)
    # print(r.url)
    # with open('code.text', 'w') as file:
    #     file.write(wd.page_source)
    soup = BeautifulSoup(wd.page_source, 'lxml')
    return soup


def get_url_data(site_url, params=None):
    #     http_pool = AppEngineManager()
    r = requests.get(site_url, params=params)
    print(r.url)
    http_pool = urllib3.connection_from_url(r.url)
    r = http_pool.urlopen('GET', r.url)
    soup = BeautifulSoup(r.data, 'lxml')
    return soup


def initbot():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    wd = webdriver.Chrome()
    return wd
