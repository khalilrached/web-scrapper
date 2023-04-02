import sys
import os
import time
from random import random
from re import match
import requests

try:
    from bs4 import BeautifulSoup
    from bs4.element import Tag, PageElement
except:
    print("")
    sys.exit(0)





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
            'url': '/fr/tun-primary-school/symbol',
            'class_name': 'view-dom-id-4c123d63c456936f3ae2acbf0e59216e'
        }
    },
    'private': 'https://www.ecoles.com.tn/etablissements/primaire?titreville=&ville=All&garderie=All&prepa=All&restaurant=All&transport=All&clubs=All&page='
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
    if response.status_code not in [202, 201, 200]:
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


def get_data_private_school():
    index = 0
    while True:
        try:
            # get region list
            public_root_content = get_html_content(f"{DATA_SOURCE['private']}{index}")
            public_root_soup = BeautifulSoup(public_root_content, 'html.parser')

            raw_data = public_root_soup.find_all("div", {"class": 'title-content'})
            for data in raw_data:
                print(data.getText())
            index += 1
        except:
            break

def get_data_public_school():
    # get region list
    public_root_content = get_html_content(BASE_URL + DATA_SOURCE['public']['root']['url'])
    public_root_soup = BeautifulSoup(public_root_content, 'html.parser')

    temp = public_root_soup.find("div", {"class": DATA_SOURCE['public']['root']['class_name']})

    if len(temp) == 0:
        # error
        raise Exception('error')

    region_list = list(map(map_links(BASE_URL), temp.find_all('a')))

    for u in region_list:
        index = 0
        while True:
            try:
                public_org_content = get_html_content(u + f"?page={index}")
                public_org_soup = BeautifulSoup(public_org_content, 'html.parser')

                raw_data = public_org_soup.find_all('table')[0].find_all_next('a')

                raw_data = list(filter(lambda link: match(r"[0-9]+", link.getText()), raw_data))
                raw_data = list(map(PageElement.getText, raw_data))
                for _id in raw_data:
                    time.sleep(random() * 2)
                    public_data_content = get_html_content(BASE_URL + DATA_SOURCE['public']['symbol']['url'] + '/' + _id)
                    public_data_soup = BeautifulSoup(public_data_content, 'html.parser')
                    data = public_data_soup.find("div", {"class": 'view-content'})
                    for d in data:
                        print(d.getText())

                index += 1
            except:
                break


if __name__ == '__main__':
    # initialize data folder
    if not os.path.exists('data'):
        os.mkdir('data')
    # get_data()
    get_data_private_school()
