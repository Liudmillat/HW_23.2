import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

user_login = 'user/16223609'
url = f'https://www.kinopoisk.ru/{user_login}/votes/'


def collect_user_rates(user_login):
    page_num = 1

    data = []

    while True:
        url = f'https://www.kinopoisk.ru/{user_login}/votes/page/{page_num}/'

        html_content = requests.get(url).text

        soup = BeautifulSoup(html_content, 'lxml')

        entries = soup.find_all('div', class_='item')  # находим все элементы с оценками

        if len(entries) == 0:
            break

        for entry in entries:
            movie_details = entry.find('div', class_='nameRus')  # находим элементы с названием фильма
            movie_name_rus = movie_details.find('a').text  # выводим название фильма на русском языке

            movie_name_eng = entry.find('div', class_='nameEng').text  # выводим название фильма на английском языке

            rating_date = entry.find('div', class_='date').text  # находим дату и время, когда была поставлена оценка

            rating = entry.find('div', class_='vote').text  # находим оценку пользователя

            data.append({'Название фильма и год выпуска': movie_name_rus, 'Название на англ.яз': movie_name_eng,
                         'Дата оценки': rating_date, 'Оценка пользователя': rating})  # добавляем пары ключ-значение

        page_num += 1  # переходим на следующую страницу
        time.sleep(5)  # задержка между запросами

    return data


user_rates = collect_user_rates(user_login='user/16223609')

df = pd.DataFrame(user_rates)

df.to_excel('user_rates3.xlsx')
