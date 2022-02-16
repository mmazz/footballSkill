import pandas as pd
from pathlib import Path
import git

root = Path(git.Repo('.', search_parent_directories=True).working_tree_dir)
data_load_dir = root / "data/raw"
data_save_dir = root / "data/interim"

csv_game = data_load_dir / 'GamesInfo.csv'
df = pd.read_csv(csv_game, index_col=None, header=0, lineterminator='\n')

csv_stadiums = data_load_dir / 'StadiumsInfo_purify.csv'
df_stadiums = pd.read_csv(csv_stadiums, index_col=None, header=0, lineterminator='\n')


def name_to_id_stadium(x):
    id_stad = df_stadiums.loc[df_stadiums.href==str(x), 'id_stadium'].values[0]
    return id_stad

df['id_stadium'] = df['stadium'].apply(lambda x: name_to_id_stadium(x))

def name_stadium(x):
    stad = df_stadiums.loc[df_stadiums.id_stadium==x, 'stadium'].values[0]
    return stad

df['stadium'] = df['id_stadium'].apply(lambda x: name_stadium(x))

def local_win(string):
    res = 0
    win = string.split(":")
    if int(win[0])>int(win[1]):
        res = 1
    elif int(win[0])==int(win[1]):
        res = 2
    return res

df['local_win'] = df['result'].apply(lambda x: local_win(x))
df['year'] = df.date.apply(lambda x: pd.Timestamp(x).year)
def season(string):
    season = string.replace('eng-premier-league-', "")
    season = season.split('-')
    season = season[0]
    return season

df['season'] = df.tournament.apply(lambda x: season(x))

def capacity(id_stadium, assistance, year):
    cap_tot = df_stadiums.loc[df_stadiums['id_stadium']==id_stadium, 'capacity'].values[0]
    if cap_tot == '???':
        res = 0
    else:
        res = round(assistance/int(cap_tot), 3)
    return res

df['porcentage_attendance'] = df.apply(lambda x: capacity(x.id_stadium, x.assistance, x.year), axis=1)

df = df.sort_values(by=['year', 'round'])


csv_game = data_save_dir / 'GamesInfo_features.csv'
df.to_csv(csv_game, index=False)

