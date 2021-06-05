import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup


male_shoes_url = 'https://www.asos.com/ru/men/tufli-botinki-i-krossovki/cat/?cid=4209&nlid=mw|%D0%BE%D0%B1%D1%83%D0' \
                 '%B2%D1%8C%7C%D1%81%D0%BE%D1%80%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D1%82%D1%8C%20%D0%BF%D0%BE%20%D1' \
                 '%82%D0%B8%D0%BF%D1%83%20%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%B0&page=1'
response_male = requests.get(male_shoes_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                                                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                                                                    'Chrome/86.0.4240.198 Safari/537.36 '
                                                                    'OPR/72.0.3815.400 (Edition Yx 03)'})
soup_male = BeautifulSoup(response_male.text, features="html.parser")

female_shoes_url = 'https://www.asos.com/ru/women/obuv/cat/?cid=4172&nlid=ww|%D0%BE%D0%B1%D1%83%D0%B2%D1%8C%7C%D1%81' \
                   '%D0%BE%D1%80%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D1%82%D1%8C%20%D0%BF%D0%BE%20%D1%82%D0%B8%D0%BF' \
                   '%D1%83%20%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%B0&page=1'
response_female = requests.get(female_shoes_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                                                        'AppleWebKit/537.36 (KHTML, like Gecko) '
                                                                        'Chrome/86.0.4240.198 Safari/537.36 '
                                                                        'OPR/72.0.3815.400 (Edition Yx 03)'})
soup_female = BeautifulSoup(response_female.text, features="html.parser")


def convert_price_to_num(price_str):
    price = float(price_str.split(',')[0].replace(' ', ''))
    return price


titles_male = soup_male.find_all('div', attrs={'class': '_3J74XsK'})
titles_female = soup_female.find_all('div', attrs={'class': '_3J74XsK'})
#Наименование i-того кроссовка мужского titles_male[i].text
#Наименование i-того кроссовка женского titles_female[i].text




prices_male = soup_male.find_all('p', attrs={'aria-hidden': 'true'})
prices_female = soup_female.find_all('p', attrs={'aria-hidden': 'true'})


#цена i-того мужского товара без скидки convert_price_to_num(prices_male[i].find_all('span')[1].text)
#цена i-того мужского товара со скидкой convert_price_to_num(prices_male[i].find_all('span')[2].text)

#цена i-того женского товара без скидки convert_price_to_num(prices_female[i].find_all('span')[1].text)
#цена i-того женского товара со скидкой convert_price_to_num(prices_female[i].find_all('span')[2].text)

sales_male_list = []
for i in range(len(prices_male)):
    try:
        ret = convert_price_to_num(prices_male[i].find_all('span')[2].text)
        sales_male_list.append(ret)
    except:
        sales_male_list.append(float('nan'))


sales_female_list = []
dataframe = pd.DataFrame(columns=['title', 'price', 'price_sale'])
def get_data_from_asos_page(soup):
    titles = soup.find_all('div', attrs={'class': '_3J74XsK'})
    number_of_titles = len(titles)
    titles_list = []
    for i in range(number_of_titles):

        titles_list.append(titles[i].text)

    prices_list = []
    prices_sale_list = []
    for i in range(number_of_titles):
        prices_soup = soup.find_all('p', attrs={'aria-hidden': 'true'})
        price_of_title = convert_price_to_num(prices_soup[i].find_all('span')[1].text)
        prices_list.append(price_of_title)
        try:
            price_of_title_sale = convert_price_to_num(prices_soup[i].find_all('span')[2].text)
        except:
            price_of_title_sale = None
        prices_sale_list.append(price_of_title_sale)
    for i in range(number_of_titles):
        dataframe.loc[len(dataframe)] = [titles_list[i].strip(), prices_list[i], prices_sale_list[i]]
    return dataframe



def next_page(soup):
    try:
        yes = soup.find('div', attrs={'class': 'fWxiz1Y'}).next_sibling
        return yes.text == 'Загрузить еще'
    except:
        return False




def collect_data(url):
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                                                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                                                                    'Chrome/86.0.4240.198 Safari/537.36 '
                                                                    'OPR/72.0.3815.400 (Edition Yx 03)'})
    soup = BeautifulSoup(response.text, features="html.parser")
    i = 1
    while next_page(soup):
        get_data_from_asos_page(soup)
        i += 1
        url = url[:url.rfind('=')] + '=' + str(i)
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                                            'AppleWebKit/537.36 (KHTML, like Gecko) '
                                                            'Chrome/86.0.4240.198 Safari/537.36 '
                                                            'OPR/72.0.3815.400 (Edition Yx 03)'})
        soup = BeautifulSoup(response.text, features="html.parser")
    return dataframe

dataframe = pd.DataFrame(columns=['title', 'price', 'price_sale'])
male_prices = collect_data(male_shoes_url)
dataframe = pd.DataFrame(columns=['title', 'price', 'price_sale'])
female_prices = collect_data(female_shoes_url)
male_prices['gender'] = 'male'
female_prices['gender'] = 'female'
prices = pd.concat([male_prices, female_prices], ignore_index=True)
prices.to_csv('asos_prices.csv', index=None)
print(prices)
