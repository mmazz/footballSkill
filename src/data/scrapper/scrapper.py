# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import time
import git
from pathlib import Path

test = False

root = Path(git.Repo('.', search_parent_directories=True).working_tree_dir)
data_save_dir = root / "data/temp"
data_save_dir.mkdir(parents=True, exist_ok=True)

#df_GamesEvents
def events_adder(type_event, id_game, id_player, time, E_id_game, E_id_player, E_event, E_time):
    E_id_game.append(id_game)
    E_event.append(type_event)
    E_id_player.append(id_player)
    E_time.append(time)

#df_PlayersByGames
def game_adder(id_game, team, id_player, titular,  D_id_games, D_id_player, D_team,
              D_titular):
    D_id_games.append(id_game)
    D_id_player.append(id_player)
    D_team.append(team)
    D_titular.append(titular)

#df_PlayersBio
def player_id(player_href, player, id_player, P_href,  P_players, P_id_player, P_name, P_lastName):
    if player[0]== ' ':
        player = player[1:]
    if (player_href not in P_players):
        P_players.add(player_href)
        P_href.append(player_href)
        id_player += 1
        P_id_player[id_player] = player_href
        name = player.split(' ', 1)
        if name[0]== '':
            name = name[1].split(' ', 1)
        if len(name)>1:
            P_name.append(name[0])
            P_lastName.append(name[1])
        else:
            P_name.append(' ')
            P_lastName.append(name[0])
    return player, id_player

'''
type_event: 1=gol, 2=time enter player, 3=time out player, 4=Red card, 5=Yellow card
            6=Double yellow card.
'''
def table_scraper(table, index, incidente, jugador_gol, id_game, id_player, team, P_href, P_players,
                  P_id_player,  P_name, P_lastName, E_id_player, E_event, E_time, E_id_game,
                  D_id_games, D_id_player, D_team, D_titular): # el 2 y el 3
    titular = 1
    # Es un equipo esto
    for tr in table[index+incidente].find_all('tr'):
        index_count = 0
        time_out = 0
        entra = 0
        time_in = 0
        time_red = 0
        time_yellow = 0
        time_Dyellow = 0
        for td in tr.find_all('td'):
            if index_count == 0:
                if 'subst' in td.text.lower():
                    titular = 0
                num = td.find('span')

            elif index_count == 1:
                player = td.find('a').text
                player_href = td.find('a', href=True)
                player_href = player_href['href']
                player_href = player_href.replace('/player_summary/', "")
                player_href = player_href[:-1]
                player, id_player = player_id(player_href, player, id_player, P_href, P_players, P_id_player, P_name, P_lastName)
                id_p = [k for k, v in P_id_player.items() if v == player_href]

                red = td.find('img', {'title':'Red card'})
                if red != None:
                    time_red = td.find_all('span')
                    type_event = 4
                    if time_red != []:
                        if len(time_red)>1:
                            time_red = time_red[1].text
                            time_red = int(time_red.replace('\'',""))
                        else:
                            time_red = time_red[0].text
                            time_red = int(time_red.replace('\'',""))
                    else:
                        time_red = None
                    events_adder(type_event, id_game, id_p[0],
                                     time_red, E_id_game, E_id_player, E_event, E_time)
                yellow = td.find('img', {'title':'Yellow card'})
                if yellow != None:
                    time_yellow = td.find('span')
                    if time_yellow != None:
                        time_yellow = time_yellow.text
                        time_yellow = int(time_yellow.replace('\'',""))
                    else:
                        time_yellow = None
                    type_event = 5
                    events_adder(type_event, id_game, id_p[0],
                                     time_yellow, E_id_game, E_id_player, E_event, E_time)

                double_yellow = td.find('img', {'title':'Second yellow card'})
                if double_yellow != None:
                    time_Dyellow = td.find_all('span')
                    type_event = 6
                    if time_Dyellow != []:
                        if len(time_Dyellow)>1:
                            time_Dyellow = time_Dyellow[1].text
                            time_Dyellow = int(time_Dyellow.replace('\'',""))
                        else:
                            time_Dyellow = time_Dyellow[0].text
                            time_Dyellow = int(time_Dyellow.replace('\'',""))
                    else:
                        time_Dyellow = None
                    events_adder(type_event, id_game, id_p[0],
                                     time_Dyellow, E_id_game, E_id_player, E_event, E_time)
            elif index_count == 2:
                num = td.find('span')
                if num.find('span', {'class':'rottext'}):
                    type_event = 3
                    time_out = num.find('span', {'class':'rottext'}).text
                    time_out = int(time_out.replace('\'',""))
                    events_adder(type_event, id_game, id_p[0],
                                     time_out, E_id_game, E_id_player, E_event, E_time)
                # Players that enter at some time
                elif num.find('span', {'class':'gruentext'}):
                    entra = 1
                    type_event = 2
                    time_in = num.find('span', {'class':'gruentext'}).text
                    time_in = int(time_in.replace('\'',""))
                    events_adder(type_event, id_game, id_p[0],
                                     time_in, E_id_game, E_id_player, E_event, E_time)
                   # Players that stays at the bench
                elif titular==0:# num.find('span', {'class':'gruentext'}):  # MAL!!!!!
                    titular = -1

            index_count += 1
        # Save only  players that plays in the game. Stay at the beanch, now yes.
        if (titular==1) or (entra == 1) or (titular==-1):
            game_adder(id_game, team,  id_p[0], titular, D_id_games, D_id_player, D_team,
                   D_titular)

    return id_player

# MEjorar la forma de buscar id player.
def game_scraper(url, page_result, id_game, id_player, team1, team2, stadium, assistance,
                 referees, dt_team1, dt_team2, P_href, P_players, P_id_player, P_name, P_lastName, E_id_player, E_event,
                 E_time, E_id_game, D_id_games, D_id_player, D_team, D_titular, time_sleep=5.0):

    url_page = url + page_result
    print(url_page)
    time.sleep(np.random.poisson(time_sleep))
    source_code = requests.get(url=url_page, verify=True, timeout=35) # verify?
    plain_text = source_code.text
    soup = bs(plain_text, "html.parser")
    div = soup.find('div', {'class': 'box'})
    data = div.find('div', {'class': 'data'})
    table = data.find_all('table', {'class': 'standard_tabelle'})
    jugador_gol = []
    incidente = 0
    if len(table)>6:
        incidente = 1# En este caso hay una tabla mas, sobre incidentes

    for tr in table[1].find_all('tr'):
        td = tr.find_all('td')
        if len(td)>1:
            names = td[1].find_all('a')
            player_href = td[1].find('a', href=True)
            player_href = player_href['href']
            player_href = player_href.replace('/player_summary/', "")
            player_href = player_href[:-1]
            player = names[0].text
            player, id_player = player_id(player_href, player, id_player, P_href, P_players,
                                          P_id_player, P_name, P_lastName)
            jugador_gol.append(player)
            time_gol = names[0].next_sibling.strip()
            time_gol = time_gol.split('.')
            time_gol = time_gol[0].replace(" ","")
               # ID del jugador!
            type_event = 1
            id_p = [k for k, v in P_id_player.items() if v == player_href]
            events_adder(type_event, id_game, id_p[0], time_gol, E_id_game, E_id_player, E_event, E_time)




    id_player = table_scraper(table, 2, incidente, jugador_gol, id_game, id_player, team1, P_href, P_players,
                  P_id_player,  P_name, P_lastName, E_id_player, E_event, E_time, E_id_game,
                  D_id_games, D_id_player, D_team, D_titular)

    id_player = table_scraper(table, 3, incidente, jugador_gol, id_game, id_player, team2, P_href, P_players,
                  P_id_player, P_name, P_lastName,  E_id_player, E_event, E_time, E_id_game,
                  D_id_games, D_id_player, D_team, D_titular)
    # Game Data

    for tr in table[4+incidente].find_all('tr'):
        td = tr.find_all('td')
        td1 = td[0].text.replace("\t","")
        td2 = td[1].text.replace("\t","")
        dato_dt1 = list(filter(None, td1.split('\n'))) # .replace(" ","")
        dato_dt2 = list(filter(None, td2.split('\n')))
        if len(dato_dt1)>=1:
            dt1 = dato_dt1[0].split(':')
            dt1 = dt1[1]
            if dt1[0]== ' ':
                dt1 = dt1[1:]
            dt_team1.append(dt1)
        if len(dato_dt1)==0:
            dt_team1.append("No data")

        if len(dato_dt2)>=1:
            dt2 = dato_dt2[0].split(':')
            dt2 = dt2[1]
            if dt2[0]== ' ':
                dt2 = dt2[1:]
            dt_team2.append(dt2)
        if len(dato_dt2)==0:
            dt_team2.append("No data")


    estadios = []
    tr = table[5+incidente].find_all('tr')
    td = tr[0].find_all('td')
    stadium_href = td[2].find('a', href=True)
    stadium_href = stadium_href['href']
    stadium_href = stadium_href.replace('/venues/', "")
    estadio = stadium_href

    for tr in table[5+incidente].find_all('tr'):
        tr = tr.text.replace("\t","")
        dato_estadio = list(filter(None, tr.split('\n'))) # .replace(" ","")
        estadios.append(dato_estadio[0]) # Por que hago esto?


    for tr in table[5+incidente].find_all('tr'):
        tr = tr.text.replace("\t","")
        dato_estadio = list(filter(None, tr.split('\n'))) # .replace(" ","")
        estadios.append(dato_estadio[0]) # Por que hago esto?


    asistencia_cancha = estadios[1]
    if len(estadios)>2:
        referee = estadios[2]
        referees.append(referee)
    else:
        referees.append("no hay datos")
    if 'without' in asistencia_cancha.lower():
        asistencia_cancha = 0
        assistance.append(asistencia_cancha)
    else: # para poder pasarlo a entero
        assistance.append(int(asistencia_cancha.replace('.','')))

    stadium.append(estadio)

    return id_game, id_player


def url_scraper(url, page, partidas_error, id_game ,id_games, id_player, tournaments,
                rounds, dates, team1, team2, results, stadium, assistance, referees,
                dt_team1, dt_team2, P_href, P_players, P_id_player, P_name,
                P_lastName, E_id_player, E_event, E_time, E_id_game,
                D_id_games, D_id_player, D_team, D_titular, test=False, time_sleep=5.0):
    url_page = url + page
    print("###################################################################")
    print(url_page)
    print("###################################################################")
    time.sleep(np.random.poisson(time_sleep))
    source_code = requests.get(url=url_page, verify=True, timeout=35) # verify?
    plain_text = source_code.text
    soup = bs(plain_text, "html.parser")
    table = soup.find('table', {'class': 'standard_tabelle'})
    tournament = page.replace('all_matches',"").replace("/","")
    ronda = 0
    count = 0
    for tr in table.find_all('tr'):
        round_try = tr.find_all('th')
        if len(round_try)!=0:
            ronda = int(round_try[0].text.replace(". Round",""))
        tds = tr.find_all('td')
        if len(tds)!=0:
            if tds[0].text == '':
                dates.append(date)
            else:
                date = tds[0].text+'T'+tds[1].text
                dates.append(date)

            tournaments.append(tournament)
            rounds.append(ronda)
            t1 = tds[2].text.replace('\n', ""); t2 = tds[4].text.replace('\n', "")
            team1.append(t1); team2.append(t2)
            res = tds[5].text.replace('\n', "")
            res = res.split(' ')
            results.append(res[0])
            id_games.append(id_game)


            # Data del partido
            href = tds[5].find('a', href=True)

            if test==True:
                if count>5:
                    print('Prueba piloto completada!')
                    break
                count += 1
                id_game, id_player = game_scraper(url, href['href'], id_game, id_player, t1,
                                                      t2, stadium, assistance, referees, dt_team1, dt_team2,
                                                      P_href, P_players, P_id_player, P_name,
                                                      P_lastName, E_id_player,
                                                      E_event, E_time, E_id_game, D_id_games, D_id_player,
                                                      D_team, D_titular, time_sleep=5.0)
            else:
                try:
                    id_game, id_player = game_scraper(url, href['href'], id_game, id_player, t1,
                                                      t2, stadium, assistance, referees, dt_team1, dt_team2,
                                                      P_href, P_players, P_id_player, P_name,
                                                      P_lastName, E_id_player,
                                                      E_event, E_time, E_id_game, D_id_games, D_id_player,
                                                      D_team, D_titular, time_sleep=5.0)

                    id_game += 1
                except:
                    print("Error partida: ", href['href'])
                    partidas_error.append( href['href'])
    return id_game, id_player





# Take all the seasons of this categori (primer league)
url_page = 'https://www.worldfootball.net/all_matches/eng-premier-league-2021-2022/'
source_code = requests.get(url_page)
plain_text = source_code.text
soup = bs(plain_text, "html.parser")
pages = soup.find_all('select',{"name":"saison"})

list_pages = []
for i in range(len(pages[0].find_all('option'))):
    list_pages.append(pages[0].find_all('option')[i]['value'])
list_pages.pop(0)
list_pages = list_pages[:50] # Keep only up to 1970
list_pages[0].replace('all_matches',"").replace("/","")# Delete current tournament incomplete.

list_pages.reverse()
if test:
    list_pages = list_pages[-3:]
# CSV jugadores (edad, nacionalidad...)
P_id_player = {}
P_players = set()
P_name = []
P_lastName = []
P_href = []

url = 'https://www.worldfootball.net'
id_game = 0
id_player = 0
for i in range(len(list_pages)):
    # Estas dos no las borro en cada iteracion.
    partidas_error = []
    # CSV partido
    asistencia = []
    estadios = []
    tournaments = []
    rounds = []
    dates = []
    team1 = []
    team2 = []
    results = []
    id_games = []
    stadium = []
    assistance = []
    referees = []
    dt_team1 = []
    dt_team2 = []

    # CSV detalles
    D_id_games = []
    D_id_player = []
    D_team = []
    D_titular = []


    # CSV eventos
    E_id_player = []
    E_event = []
    E_time = []
    E_id_game = []
    id_game, id_player = url_scraper(url, list_pages[i], partidas_error, id_game, id_games, id_player,
                                     tournaments, rounds, dates, team1 , team2, results, stadium,
                                     assistance, referees, dt_team1, dt_team2, P_href, P_players, P_id_player, P_name,
                                     P_lastName, E_id_player, E_event, E_time, E_id_game,
                                     D_id_games, D_id_player, D_team, D_titular, test)

    df_game = pd.DataFrame(data=list(zip(id_games, tournaments, rounds, dates, team1 , team2,
                                         dt_team1, dt_team2, results, stadium, assistance, referees)),
              columns=['id_game', 'tournament', 'round', 'date', 'team1' , 'team2',
                       'dt_team1', 'dt_team2', 'result', 'stadium', 'assistance', 'referee'])
    file_game = '/GamesInfo_' + str(i)
    csv_game = data_save_dir+ file_game + '.csv'
    df_game.to_csv(csv_game, index=False)

    df_game_player = pd.DataFrame(data=list(zip(D_id_games, D_id_player, D_team, D_titular)),
              columns=['id_game', 'id_player', 'team', 'titular'])
    file_game_player = '/PlayersByGame_' + str(i)
    csv_game_player = data_save_dir / file_game_player + '.csv'
    df_game_player.to_csv(csv_game_player, index=False)

    df_players = pd.DataFrame(data=list(zip(P_id_player, P_name, P_lastName, P_href)),
              columns=['id_player', 'Name', 'Last name', 'href'])
    file_players = '/PlayersBio_' + str(i)
    csv_players = data_save_dir / file_players + '.csv'
    df_players.to_csv(csv_players, index=False)

    df_events = pd.DataFrame(data=list(zip(E_id_game, E_id_player, E_event, E_time)),
              columns=['id_game', 'id_player', 'event', 'time'])
    file_events = '/GamesEvents_' + str(i)
    csv_events = data_save_dir / file_events + '.csv'
    df_events.to_csv(csv_events, index=False)

    temp_P_playeres = list(P_players)
    P_file = data_save_dir / "P_players.txt"
    with P_file.open('w', encoding='utf-8') as f:
        if len(temp_P_playeres)>0:
            f.write('\n'.join(temp_P_playeres))

    badP_file = data_save_dir / "bad_pages.txt"
    if len(partidas_error)>0:
        with badP_file.open('a', encoding='utf-8') as f:
            f.writelines('\n')
            f.writelines('\n'.join(partidas_error))

data_load_dir = root / "data/temp"
data_save_dir = root / "data/raw"



files = data_load_dir.glob("./GamesInfo_*")
all_file_game = [x for x in files if x.is_file()]

li = []
for filename in all_file_game:
    df = pd.read_csv(filename, index_col=None, header=0, lineterminator='\n')
    li.append(df)

df = pd.concat(li, axis=0, ignore_index=True)
file_game = data_save_dir / 'GamesInfo.csv'
df.to_csv(file_game, index=False)


##############################################################################
##############################################################################

files = data_load_dir.glob("./PlayersByGame_*")
all_file_game_player = [x for x in files if x.is_file()]

li = []
for filename in all_file_game_player:
    df = pd.read_csv(filename, index_col=None, header=0, lineterminator='\n')
    li.append(df)

df = pd.concat(li, axis=0, ignore_index=True)

file_game_player = data_save_dir / 'PlayersByGame.csv'
df.to_csv(file_game_player, index=False)

##############################################################################
##############################################################################

files = data_load_dir.glob("./PlayersBio_*")
all_file_players = [x for x in files if x.is_file()]

li = []
for filename in all_file_players:
    df = pd.read_csv(filename, index_col=None, header=0, lineterminator='\n')
    li.append(df)

df = pd.concat(li, axis=0, ignore_index=True)

file_players = data_save_dir / 'PlayersBio.csv'
df.to_csv(file_players, index=False)

##############################################################################
##############################################################################

files = data_load_dir.glob("./GamesEvents_*")
all_file_events= [x for x in files if x.is_file()]

li = []
for filename in all_file_events:
    df = pd.read_csv(filename, index_col=None, header=0, lineterminator='\n')
    li.append(df)

df = pd.concat(li, axis=0, ignore_index=True)

file_events = data_save_dir / 'GamesEvents.csv'
df.to_csv(file_events, index=False)
