# hay valores nan, ya que algunos eventos no tienen la informacion temporal.
import pandas as pd
import numpy as np
from pathlib import Path
import git

test = False

root = Path(git.Repo('.', search_parent_directories=True).working_tree_dir)
data_load_dir = root / "data/raw"
data_save_dir = root / "data/interim"

csv_game = data_save_dir / 'GamesInfo_features.csv'
df_game = pd.read_csv(csv_game, index_col=None, header=0, lineterminator='\n')

csv_gamePlayer = data_load_dir / 'PlayersByGameComplete.csv'
df_gamePlayer = pd.read_csv(csv_gamePlayer, index_col=None, header=0, lineterminator='\n')

csv_events = data_load_dir / 'GamesEvents.csv'
df_events = pd.read_csv(csv_events, index_col=None, header=0, lineterminator='\n')

df_gamePlayer.loc[:, 'time_played'] = 90
value = 1

# por que tengo el parametro time?
def time_played(id_game, id_player, titular, time):
    global value
    df_events_game =  df_events.loc[df_events.id_game.eq(id_game)]
    df_events_player = df_events_game.loc[df_events_game.id_player.eq(id_player)]

    sale = df_events_player.loc[df_events_player.event.eq(3)].time
    entra = df_events_player.loc[df_events_player.event.eq(2)].time
    roja = df_events_player.loc[df_events_player.event.eq(4)].time
    dobleAmarilla = df_events_player.loc[df_events_player.event.eq(6)].time
    tiempo = 90

    if titular == 1:
        #print('titular')
        if not sale.empty:
            tiempo = sale.values[0]
        elif not roja.empty:
            tiempo = roja.values[0]
        elif not dobleAmarilla.empty:
            tiempo = dobleAmarilla.values[0]

    elif titular == 0:
        #print('suplente')
        tiempo = entra.values[0]
        if not sale.empty:
            tiempo = sale.values[0] - tiempo
        elif not roja.empty:
            tiempo = roja.values[0] - tiempo
        elif not dobleAmarilla.empty:
            tiempo = dobleAmarilla.values[0] - tiempo
        # hay pocos casos con cambios en tiempo de descuento
        elif entra.values[0]<90:
            tiempo = 90 - entra.values[0]
        # al no tener el tiempo total del partido, le asigno un numero arbitrario
        else:
            tiempo = 2
    # titular = -1
    else:
        tiempo = 0
    if tiempo<0:
        print('Partida: ', id_game, ' jugador: ', id_player)
    total = len(df_gamePlayer)
    print(value, "_of_", total, end='\r')
    value += 1
    return tiempo

if test:
    df_gamePlayer = df_gamePlayer.iloc[:1000, :]
    df_gamePlayer['time_played'] = df_gamePlayer.apply(lambda x: time_played(x['id_game'], x['id_player'], x['titular'], x['time_played']), axis=1)
    print(df_gamePlayer[df_gamePlayer.titular.eq(-1)])

else:
    df_gamePlayer['time_played'] = df_gamePlayer.apply(lambda x: time_played(x['id_game'], x['id_player'], x['titular'], x['time_played']), axis=1)

    csv_game = data_save_dir / 'PlayersByGame_features.csv'
    df_gamePlayer.to_csv(csv_game, index=False)

