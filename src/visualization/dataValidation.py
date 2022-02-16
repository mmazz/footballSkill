import matplotlib.pyplot as plt
from datetime import date
import time
import pandas as pd
import git
from pathlib import Path

plt.style.use('seaborn')
font_size = 22
ticks_size= 18
plt.rc('font', size=font_size) #controls default text size
plt.rc('axes', titlesize=font_size) #fontsize of the title
plt.rc('axes', labelsize=font_size) #fontsize of the x and y labels
plt.rc('xtick', labelsize=ticks_size) #fontsize of the x tick labels
plt.rc('ytick', labelsize=ticks_size) #fontsize of the y tick labels
plt.rc('legend', fontsize=font_size) #fontsize of the legend


root = Path(git.Repo('.', search_parent_directories=True).working_tree_dir)
data_loadraw_dir = root / "data/raw"
data_load_dir = root / "data/interim"
fig_save_dir = root / "reports/img/dataInsights"

csv_game = data_load_dir / 'GameInfo_features.csv'
df_game = pd.read_csv(csv_game, index_col=None, header=0, lineterminator='\n')

csv_gamePlayer = data_load_dir / 'PlayerByGame_features.csv'
df_gamePlayer = pd.read_csv(csv_gamePlayer, index_col=None, header=0, lineterminator='\n')

csv_stadiums = data_load_dir / 'StadiumsInfo_purify.csv'
df_stadiums = pd.read_csv(csv_stadiums, index_col=None, header=0, lineterminator='\n')

csv_events = data_loadraw_dir / 'GamesEvents.csv'
df_events = pd.read_csv(csv_events, index_col=None, header=0, lineterminator='\n')

csv_players = data_loadraw_dir / 'PlayersBioComplete.csv'
df_players = pd.read_csv(csv_players, index_col=None, header=0, lineterminator='\n')

#Edad de los jugadores
def calculateAge(birthDate):
    birthDate = pd.Timestamp(birthDate)
    today = date.today()
    age = (today.year - birthDate.year -
          ((today.month, today.day) <
          (birthDate.month, birthDate.day)))
    return age

age = df_players[df_players.retirement.isnull()].copy()
age['age'] = age.apply(lambda x: calculateAge(x['born']), axis=1)
age.age.hist(bins=15)
plt.tight_layout()
plt.xlabel('Edad')
plt.savefig(fig_save_dir/'edades.png', dpi=300)

# Edad de retirada

def calculateAge_retirement(birthDate, retirement):
    try:
        birthDate = pd.Timestamp(birthDate)
        retirement = pd.Timestamp(retirement)
        age = (retirement.year - birthDate.year -
              ((retirement.month, retirement.day) <
              (birthDate.month, birthDate.day)))
    except:
        print(retirement)
    return age

age_retirement = df_players[~df_players.retirement.isnull()].copy()

age_retirement = age_retirement.loc[~age_retirement.retirement.eq('error')]
age_retirement['age'] = age_retirement.apply(lambda x: calculateAge_retirement(x['born'], x['retirement']), axis=1)
age_retirement.age.hist(bins=15)
print("Oldest retirement: ", age_retirement.loc[age_retirement.age.max(axis = 0)])
plt.tight_layout()
plt.xlabel('Edad')
plt.savefig(fig_save_dir/'retirada.png', dpi=300)

# Minutos jugados por jugador en temporadas
font_size = 14
ticks_size= 12
plt.rc('font', size=font_size) #controls default text size
plt.rc('axes', titlesize=font_size) #fontsize of the title
plt.rc('axes', labelsize=font_size) #fontsize of the x and y labels
plt.rc('xtick', labelsize=ticks_size) #fontsize of the x tick labels
plt.rc('ytick', labelsize=ticks_size) #fontsize of the y tick labels
plt.rc('legend', fontsize=font_size) #fontsize of the legend

tournaments = df_game.tournament.unique()
df_tournaments = df_game.groupby('tournament')

fig, axes = plt.subplots(3,3, figsize=(12, 9))
ax = axes.ravel() # hace que tenga un vector y no una matriz de ejes (1 por cada plot)
i = 0
for j in range(9):#len(tournaments)): # veo un par
    i+=5
    games = df_tournaments.get_group(tournaments[i]).id_game.unique()
    events_tournament = df_gamePlayer.loc[df_gamePlayer.id_game.isin(games)].copy()
    time_play = events_tournament.groupby('id_player')['time_played'].mean()
    time_play.hist(bins=30, ax=ax[j], label=tournaments[i])
    ax[j].legend(fontsize=10)
    ax[j].set_xlabel('Cambios')
fig.suptitle('Minutos jugados por jugador')
fig.tight_layout()
#plt.show()
fig.savefig(fig_save_dir/'minutos_jugados.png', dpi=300)
plt.close(fig)

# Partidos jugados por temporada

tournaments = df_game.tournament.unique()
df_tournaments = df_game.groupby('tournament')

fig,axes = plt.subplots(3,3, figsize=(12, 9))
ax = axes.ravel()# flat axes with numpy ravel
i = 0
for j in range(9):#len(tournaments)):
    i+=5
    games = df_tournaments.get_group(tournaments[i]).id_game.unique()
    events_tournament = df_gamePlayer.loc[df_gamePlayer.id_game.isin(games)].copy()
    time_play = events_tournament.groupby('id_player').size()
    time_play.hist(bins=30, ax=ax[j], label=tournaments[i])
    ax[j].legend(fontsize=10)
    ax[j].set_xlabel('Partidos')
    print('torneo: ', tournaments[i], ', maxima cantidad de partidos por jugador: ',max(time_play))
fig.suptitle('Partidos jugados por jugador')
fig.tight_layout()
#plt.show()
fig.savefig(fig_save_dir/'partidos_jugados.png', dpi=300)
plt.close(fig)

# Sustituciones por jugador por temporada

tournaments = df_game.tournament.unique()
df_tournaments = df_game.groupby('tournament')

fig,axes = plt.subplots(3,3, figsize=(12, 9))
ax = axes.ravel()# flat axes with numpy ravel
i = 0
for j in range(9):#len(tournaments)):
    i+=5
    games = df_tournaments.get_group(tournaments[i]).id_game.unique()
    events_tournament = df_events.loc[df_events.id_game.isin(games)].copy()
    events_tournament = events_tournament.loc[events_tournament.event.eq(3)]
    time_play = events_tournament.groupby('id_player').size()
    time_play.hist(bins=30, ax=ax[j], label=tournaments[i])
    ax[j].legend(fontsize=10)
    ax[j].set_xlabel('Sustituciones')
    #ax[j].set_title(tournaments[i],fontsize=9)
fig.suptitle('Sustituciones por jugador')
fig.tight_layout()
#plt.show()
fig.savefig(fig_save_dir/'sustituciones_jugador.png', dpi=300)
plt.close(fig)

# Sustituciones por equipo por temporada

def games_players(id_game, id_player):
    global id_games, id_players
    i=0
    notin = False
    while(not notin and (i<len(id_players))):
        if (id_game==id_games[i]) and (id_player==id_players[i]):
            notin = True
        i+=1
    return notin

tournaments = df_game.tournament.unique()
df_tournaments = df_game.groupby('tournament')

fig,axes = plt.subplots(3,3, figsize=(12, 9))
ax = axes.ravel()# flat axes with numpy ravel
i = 0
time_in = time.time()
for j in range(9):#len(tournaments)):
    i+=5
    games = df_tournaments.get_group(tournaments[i]).id_game.unique()
    events_tournament = df_events.loc[df_events.id_game.isin(games)].copy()
    events_tournament = events_tournament.loc[events_tournament.event.eq(3)]
    id_games = events_tournament['id_game'].values
    id_players = events_tournament['id_player'].values
    #Nuevo filtro:
    df_gamePlayer_temp = df_gamePlayer.loc[df_gamePlayer.id_game.isin(id_games)].copy()
    df_gamePlayer_temp = df_gamePlayer_temp.loc[df_gamePlayer.id_player.isin(id_players)].copy()

    boolGamePlayer = df_gamePlayer_temp.apply(lambda x: games_players(x['id_game'], x['id_player']), axis=1)

    time_play = df_gamePlayer_temp.loc[boolGamePlayer].copy()
    time_play = time_play.groupby('team').size()
    time_play.hist(bins=30, ax=ax[j], label=tournaments[i])
    ax[j].legend(fontsize=10)
    ax[j].set_xlabel('Sustituciones')
time_out = time.time()
print('Tiempo tardado: ', round(time_out - time_in, 6))
fig.suptitle('Sustituciones por equipo')
fig.tight_layout()
#plt.show()
fig.savefig(fig_save_dir/'sustituciones_equipo.png', dpi=300)
plt.close(fig)


# total de poartidos jugados por jugador




