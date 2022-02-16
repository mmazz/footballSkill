from bs4 import BeautifulSoup as bs
import numpy as np
import requests
import time
import pandas as pd
import git
from pathlib import Path

test = False

root = Path(git.Repo('.', search_parent_directories=True).working_tree_dir)
data_dir = root / "data/raw"

csv_game =  data_dir / 'GamesInfo.csv'
df_game = pd.read_csv(csv_game, index_col=None, header=0, lineterminator='\n')

stadiums = df_game.stadium.unique()



def url_scraper_stadium(url, page, stad_name, city, country, capacity, team, time_sleep=5.0):
    url_page = url + page
    print(url_page)
    time.sleep(np.random.poisson(time_sleep))
    source_code = requests.get(url=url_page, verify=True, timeout=35) # verify?
    plain_text = source_code.text
    soup = bs(plain_text, "html.parser")
    table = soup.find('div', {'class': 'sidebar'})
    head = table.find('div', {'class': 'head'})
    name = head.find('h2')
    if name:
        name = name.text
        stad_name.append(name)
    else:
        stad_name.append(None)

    table = table.find('table', {'class': 'standard_tabelle yellow'})

    data_dict = {}
    data_type = 0
    good_row = 0

    for tr in table.find_all('tr'):

        for td in tr.find_all('td'):
            b = td.find('b')
            #if 'Born' in td[0]:
            if b != None:
                data_type = b.text
                data_dict[b.text] = 0
                good_row = 1
            elif (good_row==1):
                good_row = 0
                data = td.text
                data = data.replace("\t","")
                if 'Country' in data_type:
                    data = data.replace("\n","")
                    data_dict[data_type] = data
                elif 'Teams' in data_type:
                    img = td.find('img')
                    good_row = 1
                    if img == None:
                        data = data.replace("\n","")
                        data = data.replace('\xa0', '')
                        data_dict[data_type] = data
                else:
                    data_dict[data_type] = data

    city_flag = 0
    country_flag = 0
    capacity_flag = 0
    team_flag = 0


    for key, value in data_dict.items():
        if 'City' in key:
            city.append(value)
            city_flag = 1
        elif 'Country' in key:
            country.append(value)
            country_flag = 1
        elif 'Capacity' in key:
            value = value.replace('.', '')
            try:
                value = int(value)
            except:
                value = value
            capacity.append(value)
            capacity_flag = 1
        elif 'Teams' in key:
            team.append(value)
            team_flag = 1

    ############ FLAGS CONTROL #########################
    if city_flag == 0:
        city.append(None)
    if country_flag == 0:
        country.append(None)
    if capacity_flag == 0:
        capacity.append(0)
    if team_flag == 0:
        team.append(None)

stad_name = []
city = []
country = []
capacity = []
team = []
bad_stadium = []
good_stadiums = []
url = 'https://www.worldfootball.net/venues/'
count = 0
for i in range(len(stadiums)):
    try:
        url_scraper_stadium(url, stadiums[i], stad_name, city, country, capacity, team)

    except:
        bad_stadium.append(stadiums[i])
    if test==True:
        if count>1:
            print('Chau')
            break
        count += 1



df_stadium = pd.DataFrame(data=list(zip(stad_name, city, country, capacity, team, stadiums)),
              columns=['stadium', 'city', 'country', 'capacity', 'team', 'href'])

df_stadium['id_stadium'] = df_stadium.index

csv_stadium = data_dir / 'StadiumsInfo.csv'
df_stadium.to_csv(csv_stadium, index=False)

if len(bad_stadium)>0:
    with open('bad_stadiums.txt', 'w', encoding='utf-8') as f:
        f.writelines('\n'.join(bad_stadium))
