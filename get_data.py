import time
from random import random

import scrapy as sc
import os
from bs4 import BeautifulSoup
from bs4.element import Tag
import requests

#  nom de l'école, statut (publique ou privée), et qualité d'éducation.

BASE_URL = 'https://tun.databasesets.com'

DATA_SOURCE = {
    'public': {
        'root': {
            'url': '/fr/tun-primary-school',
            'class_name': 'view-dom-id-95f5aba0261a94be0a2950519107eca4'
        },
        'org': {
            'url': '/fr/tun-primary-school/organization/{id}',
            'class_name': 'view-dom-id-cd0f4dbc1da641a5bfdddc4cb3f76cbb'
        },
        'symbol': {
            'url': '/fr/tun-primary-school/symbol/{id}',
            'class_name': 'region region-content'
        }
    },
    'private': 'https://www.ecoles.com.tn/etablissements/primaire?titreville=&ville=All&garderie=All&prepa=All&restaurant=All&transport=All&clubs=All&page={page}'
}


def get_html_content(url):
    """
        return html content of an url and raise an exception if the given url is not found
    """
    # get all html pages and save them in data/html
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    session = requests.Session()
    session.headers.update(headers)
    # Enable cookies
    session.get(url)
    # Enable JavaScript
    payload = {'key1': 'value1', 'key2': 'value2'}
    response = session.get(url, data=payload)
    # Get the HTML content of the page
    if response.status_code not in [202, 200]:
        print(f"NotFoundUrl: {url}")
        raise Exception('url not found.')
    return response.text


# get all region links
def scrap_html_page(base_url, fn_scrape):
    pass


def map_links(base_url):
    def f(link: Tag):
        return f"{base_url}{link.get('href')}"
    return f


def get_urls():
    soup = BeautifulSoup(data, 'html.parser')
    #


def get_data():
    # initialize data folder
    if not os.path.exists('data'):
        os.mkdir('data')
    # get region list
    public_root_content = get_html_content(BASE_URL + DATA_SOURCE['public']['root']['url'])
    public_root_soup = BeautifulSoup(public_root_content, 'html.parser')

    temp = list(filter(lambda t: t.get('class') is not None and DATA_SOURCE['public']['root']['class_name'] in t.get('class'), public_root_soup.find_all('div')))

    if len(temp) == 0:
        # error
        raise Exception('error')

    region_list = list(map(map_links(BASE_URL), temp[0].find_all('a')))

    for u in region_list:
        time.sleep(random()*3)
        print(u)
        public_org_content = get_html_content(u)
        public_org_soup = BeautifulSoup(public_org_content, 'html.parser')

        data = public_org_soup.find_all('table')[0].find_all_next('a')

        print(data)
        #https://tun.databasesets.com/fr/tun-primary-school/organization/%D8%A3%D8%B1%D9%8A%D8%A7%D9%86%D8%A9
    pass


if __name__ == '__main__':
    get_data()
