import requests
from bs4 import BeautifulSoup

def parse():
    URL = 'https://zen.yandex.ru/media/itgap/top10-osnovnyh-bibliotek-na-python-5db2a6823f548700ac5b1908?utm_source=serp'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'
    }

    response = requests.get(URL, headers = HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.findAll('div', class_ = 'article-render')
    cars = []

    for item in items:
        cars.append({
            'title': item.find('h2', class_= 'article-render__block article-render__block_h2').get_text(strip = True)
        })

        for car in cars:
            print(car['title'])


parse()