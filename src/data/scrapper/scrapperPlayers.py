# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as bs
import numpy as np
import requests
import time
import pandas as pd
import git
from pathlib import Path
import re
# Run only 3 players pages, and save it.
test =  False

root = Path(git.Repo('.', search_parent_directories=True).working_tree_dir)
data_load_dir = root / "data/raw"
data_save_dir = root / "data/interim"

csv_players = data_load_dir / "PlayersBio.csv"
df_players = pd.read_csv(csv_players, index_col=None, header=0, lineterminator='\n')
df_players.drop_duplicates(subset ="id_player",  inplace = True)

players = df_players["href"].to_list()
id_players = df_players["id_player"].to_list()



def url_scraper_player(url, page, player_name, born, nacionality, height, weight, position, retirement,time_sleep=5.0):
    url_page = url + page
    print(url_page)
    time.sleep(np.random.poisson(time_sleep))
    source_code = requests.get(url=url_page, verify=True, timeout=35) # verify?
    plain_text = source_code.text
    soup = bs(plain_text, "html.parser")
    try:
        table = soup.find('div', {'class': 'content'})
        box = table.find_all('div', {'class': 'box'})
        i = 0
        flag_retirement = False # para que no agarre data como manager
        while(not flag_retirement and i<len(box)):
            head = box[i].find('div', {'class': 'head'})
            if (head) and (head.find('h2').text == 'Club career'):
                flag_retirement = True
                data = box[i].find('div', {'class': 'data'})
                table = data.find('table', {'class': 'standard_tabelle'})
                tr = table.find('tr')
                td = tr.find('td')
                date = td.text
                date = date.replace("\t", "")
                date = date.split('-')
                if len(date)>1:
                    date = date[1].replace(" ", "")
                    date_check = pd.Timestamp(date)
                    today = pd.Timestamp('06/2021')
                    if date_check<= today:
                        date = pd.Timestamp(str(date))
                        retirement.append(date)
                    else:
                        retirement.append(None)
                else:
                    retirement.append(None)

            i+=1
    except:
        retirement.append("error")


    table = soup.find('div', {'class': 'sidebar'})
    head = table.find('div', {'class': 'head'})
    name = head.find('h2')
    if name:
        name = name.text
        player_name.append(name)
    else:
        player_name.append(None)

    table = table.find('table', {'class': 'standard_tabelle yellow'})

    data_type = 0
    data = 0
    born_flag = 0
    nationality_flag = 0
    height_flag = 0
    weight_flag = 0
    position_flag = 0
    for tr in table.find_all('tr'):
        tds = tr.find_all('td')
        if len(tds)>1:
            b = tds[0].find('b')# Titles are insede <b>
            if b != None:
                data_type = b.text
                data = tds[1].text
                data = data.replace('\n', '')
                data = data.replace('\t', '')
                if 'Born:' in data_type:
                    data = data.split(' ')
                    born.append(pd.Timestamp(data[0]))
                    born_flag = 1
                elif 'Nationality' in data_type:
                    data = re.sub("([a-z])([A-Z])","\g<1> \g<2>", data)
                    nacionality.append(data)
                    nationality_flag = 1
                elif 'Height' in data_type:
                    if 'cm' in data:
                        data = data.replace(' cm', "")
                        data = int(data)
                    height.append(data)
                    height_flag = 1
                elif 'Weight' in data_type:
                    if 'kg' in data:
                        data = data.replace(' kg', "")
                        data = int(data)
                    weight.append(data)
                    weight_flag = 1
                elif 'Positio' in data_type:
                    data = re.sub("([a-z])([A-Z])","\g<1> \g<2>", data)
                    position.append(data)
                    position_flag = 1
    ############ FLAGS CONTROL #########################
    if born_flag == 0:
        born.append(None)
    if nationality_flag == 0:
        nacionality.append(None)
    if height_flag == 0:
        height.append(0)
    if weight_flag == 0:
        weight.append(0)
    if position_flag == 0:
        position.append(None)

player_name = []
born = []
nacionality = []
height = []
weight = []
position = []
retirement = []
bad_players = []
url = 'https://www.worldfootball.net/player_summary/'
count = 0
if test:
    index = df_players.index
    condition = df_players["href"] == 'hannibal-mejbri'
    index = index[condition].values[0]
    df_players = df_players[index:]
    players = df_players["href"].to_list()
    id_players = df_players["id_player"].to_list()
    print(players)

for i in range(len(players)):
    try:
        url_scraper_player(url, players[i], player_name, born, nacionality, height, weight, position, retirement)
        #print(i, '_of_', len(players), end='\r')
    except:
        bad_players.append(players[i])
        print(players[i])
    if test==True:
        if count>4:
            print('Chau')
            id_players = id_players[:len(born)]
            break
        count += 1



df_players_extra = pd.DataFrame(data=list(zip(id_players, player_name, born,
                                              nacionality, height, weight, position,
                                              players, retirement)),
              columns=['id_player', 'name', 'born', 'nacionality', 'height',
                       'weight', 'position', 'href', 'retirement'])

csv_players = data_save_dir / "PlayersBioComplete.csv"
df_players_extra.to_csv(csv_players, index=False)

if len(bad_players)>0:
    with open('bad_pages.txt', 'a', encoding='utf-8') as f:
        f.writelines('\n')
        f.writelines('\n'.join(bad_players))
