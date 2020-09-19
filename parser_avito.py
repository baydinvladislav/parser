import requests
from bs4 import BeautifulSoup

URL = 'https://www.avito.ru/moskva/avtomobili/s_probegom/bmw-ASgBAgICAkSGFMjmAeC2DeSXKA?cd=1' # Укажите URL адрес avito.ru
HEADERS = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
    'accept':'*/*'
}
DOMAIN = 'https://www.avito.ru'


def get_html(url, params=None):
    response = requests.get(url, headers=HEADERS, params=params)
    return response


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    page = soup.find_all('span', class_='pagination-item-1WyVp')
    if page:
        return int(page[-2].get_text()) #индекс не [-1], так как у авито последний элемент в пагинации "След"
    else:
        return 1


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='item__line')

    cars = []
    for item in items:
        cars.append({
            'title': item.find('a', class_='snippet-link').get_text(strip=True), #название объявления
            'link': DOMAIN + item.find('a', class_='snippet-link').get('href'), #ссылка на объявление
            'price': item.find('div', class_='snippet-price-row').get_text(strip='True'), #цена в объявлении
            #'station_metro': item.find('span', class_='item-address-georeferences-item__content').get_text(strip='True'), #станция метро продавца
        })
    return cars


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        cars = []
        pages_count = get_pages_count(html.text)
        for a in range(1, pages_count + 1):
            print(f'Парсинг страницы {a} из {pages_count}...')
            html = get_html(URL, params={'p':a})
            cars.extend(get_content(html.text))
            #cars = get_content(html.text)
        print(cars)
    else:
        print('Не удалось получить ответ от web-страницы')


parse()
