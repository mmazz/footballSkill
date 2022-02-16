# Falta ver tambien cuantos partidos lleva sin jugar.
# hay valores nan, ya que algunos eventos no tienen la informacion temporal.
import pandas as pd
import numpy as np
from pathlib import Path

test = False

import git

root = Path(git.Repo('.', search_parent_directories=True).working_tree_dir)
data_load_dir = root / "data/interim"
data_save_dir = root / "data/interim"


csv_game = data_load_dir / 'GamesInfo_features.csv'
df_game = pd.read_csv(csv_game, index_col=None, header=0, lineterminator='\n')

csv_player = data_load_dir / 'PlayersBioComplete.csv'
df_player = pd.read_csv(csv_player, index_col=None, header=0, lineterminator='\n')

df_player = df_player[df_player.retirement.ge('1990')]
df_player = df_player.reset_index(drop=True)

print(df_player)
csv_player = data_load_dir / 'PlayersByGame_features.csv'
df_playersByGame = pd.read_csv(csv_player, index_col=None, header=0, lineterminator='\n')

playersOfInterest = df_player["id_player"].tolist()
df_playersByGame = df_playersByGame[df_playersByGame.id_player.isin(playersOfInterest)]

# Creo lista de temporadas
seasons = df_game['season'].unique()

# Solo desde 1990
seasons = seasons[19:]

index_season = 0

if test:
    seasons = seasons[19:21]
    index_season = len(seasons)-2

while(index_season<len(seasons)):
    idex_season = 5
    season = seasons[index_season]
    df_season = df_game.loc[df_game.season.eq(season)]
    numOfMatches = df_season['round'].max()
    matrix_data =  np.full((df_player.shape[0], numOfMatches), -1, dtype=int)
    index_matches = 0
    maxMatches = df_season.shape[0]
    print("Temporada: ", season, "_of_ ", seasons[-1])
    for index, row in df_season.iterrows():
        match_number = row['round']-1
        gameId = row['id_game']
        df_titular = df_playersByGame.loc[df_playersByGame.id_game.eq(gameId)]
        print(index_matches, "_of_", maxMatches, end='\r')

        for index_tit, row_tit in df_titular.iterrows():
            id_player = row_tit['id_player']
            titular = row_tit['titular']
            activity = row_tit['time_played']

            index_player = df_player.loc[df_player.id_player.eq(id_player)].index[0]
            matrix_data[index_player, match_number] = activity
        index_matches = index_matches + 1

    index_season = index_season + 1
    matrix_data = np.c_[df_player.id_player.tolist(), matrix_data]
    columnIndex = list(map(str,np.linspace(1, numOfMatches, numOfMatches, dtype=int))).insert(0, "id_player")
    df_playersActivity  = pd.DataFrame(matrix_data.tolist(), columns=columnIndex)

csv_game = data_save_dir / 'PlayersActivity.csv'
df_playersActivity.to_csv(csv_game, index=False)

