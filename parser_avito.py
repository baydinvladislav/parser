import requests
from bs4 import BeautifulSoup
import csv
import os

URL = 'https://www.avito.ru/moskva/avtomobili/s_probegom/bmw-ASgBAgICAkSGFMjmAeC2DeSXKA?cd=1' #Укажите URL адрес avito.ru
HEADERS = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
    'accept':'*/*'
}
DOMAIN = 'https://www.avito.ru'
FILE = 'cars.csv' #название файла с автомобилями

def get_html(url, params=None):
    '''Получение ответа от сервера авито'''
    response = requests.get(url, headers=HEADERS, params=params)
    return response


def get_pages_count(html):
    '''Получаем контент со всех страниц пагинации'''
    soup = BeautifulSoup(html, 'html.parser')
    page = soup.find_all('span', class_='pagination-item-1WyVp')
    if page:
        return int(page[-2].get_text()) #индекс не [-1], так как у авито последний элемент в пагинации "След"
    else:
        return 1


def get_content(html):
    '''Указываем программе какие блоки информации мы хотим получить'''
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='item__line')

    cars = []
    for item in items:
        station_metro = item.find('span', class_='item-address-georeferences-item__content') #после теста отбило ошибку из-за не указаной станции метро в объявлении
        if station_metro:
            station_metro = station_metro.get_text(strip='True')
        else:
            station_metro = 'Станция метро не указана'
        cars.append({
            'title': item.find('a', class_='snippet-link').get_text(strip=True), #название объявления
            'link': DOMAIN + item.find('a', class_='snippet-link').get('href'), #ссылка на объявление
            'price': item.find('div', class_='snippet-price-row').get_text(strip='True'), #цена в объявлении
            'station_metro': station_metro, #станция метро продавца
        })
    return cars


def save_csv(items, path):
    '''Сохранение полученного списка автомобилей в файл CSV.
    Файл сохраняется в папку с файлом программы, с именем "cars.csv"
    При повторном сборе информации, старый файл cars необходимо удалить/пренести из папки.
    Автоматический запуск файла, через стандартное приложение чтения файлов CSV.
    '''
    with open(path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Марка','Цена','Метро','Ссылка'])
        for item in items:
            writer.writerow([item['title'], item['price'], item['station_metro'], item['link']])


def parse():
    '''Объединяем все предыдущие функции,
    также добавляем вывод информации на экран для вазимодействия с пользователем.
    '''
    URL = input('Введите адрес ссылки для сбора данных: ')
    URL = URL.strip()
    html = get_html(URL)
    if html.status_code == 200:
        cars = []
        pages_count = get_pages_count(html.text)
        for a in range(1, pages_count + 1):
            print(f'Парсинг страницы {a} из {pages_count}...')
            html = get_html(URL, params={'p':a})
            cars.extend(get_content(html.text))
        save_csv(cars, FILE)
        print(f'Получено {len(cars)} автомобилей.')
        os.startfile(FILE)
    else:
        print('Не удалось получить ответ от web-страницы')


parse()
