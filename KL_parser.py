from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient

client = MongoClient("mongodb+srv://admin:admin@cluster0-fnovw.mongodb.net/test") #Подключаемся к клиенту
db = client.news
data = db.data


def save(comp): #Записываем в БД
    data.update({u'newsDate': comp["date"], u'newsName': comp["title"], u'newsLink': comp["link"], u'newsText': comp["text"]}, { u'$setOnInsert': { u'newsDate': comp["date"], u'newsName': comp["title"], u'newsLink': comp["link"], u'newsText': comp["text"] } }, **{ 'upsert': True })

def parse():

    URL = 'https://riac34.ru/'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
    }
    HOST = 'https://riac34.ru' #Адрес для склеивание ссылки
    response = requests.get(URL, headers = HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.findAll('div', class_ = 'col-md-8 no-paddingLeft') #Получаем блоки сайта
    comps = []

    for item in items:
        
        resites=requests.get((HOST + item.find('a', target="_blank").get('href')),headers = HEADERS) #Грузим каждый сайт
        soup2 = BeautifulSoup(resites.content, 'html.parser') #Сохроняем контент

        comps.append ({ #Находим и записываем нужные данные
            'title':item.find('h2').get_text(strip = True),
            'text':soup2.find('div', class_='detail-text').get_text(strip = True),
            'date':item.find('span', class_='date').get_text(strip = True),
            'link': HOST + item.find('a', target="_blank").get('href'),#Склеиваем полученный адресс, доменом
            })
        
    for comp in comps: #Сохроняем
        save(comp) 
parse()