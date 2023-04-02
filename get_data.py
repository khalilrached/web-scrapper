import sys
import os
import time
from random import random
from re import match
from threading import Thread

import requests

try:
    from bs4 import BeautifulSoup
    from bs4.element import Tag, PageElement
except:
    print("")
    sys.exit(0)

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


def map_links(base_url):
    def f(link: Tag):
        return f"{base_url}{link.get('href')}"

    return f


def calc_quality(n: int):
    if n > 30:  # mauvais
        return 'mauvaise'
    elif n <= 30 and n >= 20:
        return 'moyenne'
    else:
        return 'excellent'


def get_data_private_school(file, std_output=True):
    index = 0
    while True:
        try:
            # get region list
            public_root_content = get_html_content(f"{DATA_SOURCE['private']}{index}")
            public_root_soup = BeautifulSoup(public_root_content, 'html.parser')

            raw_data = public_root_soup.find_all("div", {"class": 'title-content'})
            for data in raw_data:
                csv_data = f"{data.getText().strip()},Privee,None"
                file.write(csv_data+"\n")
                file.flush()
                if std_output:
                    print(csv_data)
            index += 1
        except Exception as ex:
            print(ex)
            break


def get_data_public_school(file, std_output=True, speed=2):
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
                    time.sleep(random() * speed)
                    public_data_content = get_html_content(
                        BASE_URL + DATA_SOURCE['public']['symbol']['url'] + '/' + _id)
                    public_data_soup = BeautifulSoup(public_data_content, 'html.parser')
                    data = public_data_soup.find("div", {
                        "class": 'views-row views-row-1 views-row-odd views-row-first views-row-last'})
                    temp_data = {}
                    for d in data:
                        if d.getText().find(':') != -1:
                            key, value = d.getText().split(':')
                            temp_data[key] = value
                    quality = calc_quality(
                        int(temp_data[" Nombre total d'étudiants"]) / int(temp_data[" Total Classes"]))
                    csv_data = f"{temp_data[' Nom']},Publique,{quality}"
                    file.write(csv_data + "\n")
                    file.flush()
                    if std_output:
                        print(csv_data)
                index += 1
            except Exception as ex:
                print(ex)
                break


if __name__ == '__main__':
    # initialize data folder
    if not os.path.exists('data'):
        os.mkdir('data')

    args = sys.argv[1:]

    STD_OUTPUT = True
    for arg in args:
        if arg == "--silent":
            STD_OUTPUT = True
        if arg.find('--speed') != -1:
            _, speed_str = arg.split('=')
            if speed_str in ['1', '2', '3']:
                SPEED = int(speed_str)
            else:
                SPEED = 2
    file_path = os.path.join(os.getcwd(), 'data', 'output.csv')
    f = open(file_path, 'a')

    # threading
    thread1 = Thread(target=lambda: get_data_public_school(file=f, std_output=STD_OUTPUT, speed=SPEED))
    thread2 = Thread(target=lambda: get_data_private_school(file=f, std_output=STD_OUTPUT))
    thread2.start()
    thread1.start()

    print(f"Thanks for using our application.\n your data is saving {file_path}.")
