import requests
from bs4 import BeautifulSoup

URL = 'https://auto.ru/moskva/cars/mercedes/all/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0', 'accept': '*/*'}

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_= 'ListingItemPrice-module__content') # Получение класса из html разметки сайта
    print(items)

    cars = []
    for item in items:
        cars.append({
            'title': item.find('a', class_='proposition').get_text()
        })
    print(cars)

def parse():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
    else:
        print('Не удалось соединиться с WEB-страницей')



parse()


