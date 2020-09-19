import requests
from bs4 import BeautifulSoup

URL = 'https://www.avito.ru/moskva/avtomobili/s_probegom/bmw-ASgBAgICAkSGFMjmAeC2DeSXKA?cd=1'
HEADERS = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
    'accept':'*/*'
}
DOMAIN = 'https://www.avito.ru'


def get_html(url, params=None):
    response = requests.get(url, headers=HEADERS, params=params)
    return response


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='item__line')

    cars = []
    for item in items:
        cars.append({
            'title': item.find('a', class_='snippet-link').get_text(strip=True),
            'link': DOMAIN + item.find('a', class_='snippet-link').get('href'),
            'price': item.find('div', class_='snippet-price-row').get_text(strip='True'),
            'station_metro': item.find('span', class_='item-address-georeferences-item__content').get_text(strip='True'),
        })
    print(cars)



def parse():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
    else:
        print('Не удалось получить ответ от web-страницы')


parse()
