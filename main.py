import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

url = 'https://store.steampowered.com/search/results/?query&start=1&count=50&dynamic_data=&sort_by=Name_ASC&term=Action&snr=1_7_7_151_7&infinite=1'

def get_total(url):
    r = requests.get(url)
    data = dict(r.json())
    return data['total_count']

def get_data(url):
    r = requests.get(url)
    data = dict(r.json())
    return data['results_html']

def parse(data):
    games_list = []
    soup = BeautifulSoup(data, 'html.parser')
    games = soup.find_all('a')
    for game in games:
        title = game.find('span', {'class': 'title'}).text #get text
        if title=="":
            title='No title'
        price_list = game.find('div', {'class': 'search_price'}).text.strip().split('$')
        if len(price_list)==3:
            price = price_list[1]
            discount=price_list[2]
        elif len(price_list)==2:
            price=price_list[1]
            discount='no discount'
        elif len(price_list)==1 and price_list[0] in ['Free','Free Demo']:
            price=price_list[0]
            discount=''
        elif len(price_list)==1 and price_list[0]=='':
            price='free'
            discount=""
        else:
            price=price_list[0]
            discount=''

        my_game={
            'title' : title,
            'Price': price,
            'Discount':discount
        }
        games_list.append(my_game)
    return games_list

def output(games_list):
    gamesdf = pd.concat([pd.DataFrame(g) for g in results])
    gamesdf.to_csv('games_steam.csv', index=False)
    print('Fin. Saved to CSV')
results=[]
for x in range(0,int(get_total(url)),50):
    data = get_data(f'https://store.steampowered.com/search/results/?query&start={x}&count=50&dynamic_data=&sort_by=Name_ASC&term=Action&snr=1_7_7_151_7&infinite=1')
    results.append(parse(data))
    print(results)


output(results)

#this script will scrap the store of games steam and save the prices of all games in csv file