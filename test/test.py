import unittest
import pandas as pd
import git
from pathlib import Path

root = Path(git.Repo('.', search_parent_directories=True).working_tree_dir)
data_load_dir = root / "data/interim"


csv_game = data_load_dir / 'WFI_GamesInfoComplete_extra.csv'
df_game = pd.read_csv(csv_game, index_col=None, header=0, lineterminator='\n')

csv_gamePlayer = data_load_dir / 'WFI_PlayersByGameComplete_extra.csv'
df_gamePlayer = pd.read_csv(csv_gamePlayer, index_col=None, header=0, lineterminator='\n')

csv_events = data_load_dir / 'WFI_GamesEventsComplete.csv'
df_events = pd.read_csv(csv_events, index_col=None, header=0, lineterminator='\n')

csv_players = data_load_dir / 'WFI_PlayersBioComplete_extra.csv'
df_players = pd.read_csv(csv_players, index_col=None, header=0, lineterminator='\n')

games = df_game.loc[(df_game.season.ge(1987))].id_game.to_list()
df_gamePlayer_primer = df_gamePlayer.loc[df_gamePlayer.id_game.isin(games)].copy()
df_gamePlayer_primer = df_gamePlayer.loc[df_gamePlayer.titular.ne(-1)].copy()
df_events_primer = df_events.loc[df_events.id_game.isin(games)].copy()



jugadores = ['frank-lampard', 'carlos-tevez', 'wayne-rooney', 'roy-keane', 'cristiano-ronaldo',
              'romelu-lukaku', 'david-luiz', 'alan-shearer', 'patrick-vieira', 'kevin-nolan']
ids = []
for i in range(len(jugadores)):
    id_play = df_players.loc[df_players.href.eq(jugadores[i])]['id_player'].iloc[0]
    ids.append(id_play)
# Datos desde 1987/1988 hasta la liga 2020/2021 de la propia pagina WF
#                          lamp  teve roon kean, cr7  lukaku  luiz shea viei nolan
datosOF_numGames        = [609, 202, 491, 440, 199-3, 257-5, 213, 559, 307, 401]
datosOF_numGoals        = [177,  85, 209,  55,  87-3, 117-3,  15, 283,  32,  70]
datosOF_numYellow       = [ 58,  24,  99,  73,    26,    19,  41,  40,  77,  83]
datosOF_dobYellow       = [  1,   0,   1,   1,     2,     0,   0,   1,   5,   2]
datosOF_numRed          = [  2,   0,   2,   6,     2,     0,   4,   1,   3,   3]
datosOF_numCambiosIn    = [ 63,  37,  70,  17,    39,    43,  13,  27,  23,  41]
datosOF_numCambiosOut   = [ 53,  86, 111,  49,    45,    50,  14,  35,  22,  92]
# Modificaciones hechas a los datos de WF, ya que estaban mal.
# a kean, le saque un partido.
# 1 mas lamp, rooney lukaku, luiz, nolan. 1 menos kean
#max_gol = df_events_goles.groupby('id_player').size().sort_values(ascending=False)
class TestDataBase(unittest.TestCase):
    def test_num_games(self):
        # Cuantos partidos
        datos_numGames = []
        for i in range(len(ids)):
            num_games = df_gamePlayer_primer.loc[df_gamePlayer_primer.id_player.eq(ids[i])]['id_player'].size
            datos_numGames.append(num_games)
            self.assertEqual(datosOF_numGames[i]-num_games, 0)

    def test_num_goals(self):
        datos_numGoals = []
        df_events_goles = df_events_primer.loc[df_events_primer.event.eq(1)].copy()

        for i in range(len(ids)):
            num_goals = df_events_goles.loc[df_events_goles.id_player.eq(ids[i])]['id_player'].size
            datos_numGoals.append(num_goals)
            self.assertEqual(datosOF_numGoals[i]-num_goals, 0)

    def test_num_CambiosOut(self):
        df_events_CambiosOut = df_events_primer.loc[df_events_primer.event.eq(3)].copy()
        #numCambiosOut = df_events_CambiosOut.groupby('id_player').size().sort_values(ascending=False)

        datos_numCambiosOut = []
        for i in range(len(ids)):
            num_Out = df_events_CambiosOut.loc[df_events_CambiosOut.id_player.eq(ids[i])]['id_player'].size
            datos_numCambiosOut.append(num_Out)
            self.assertEqual(datos_numCambiosOut[i]-num_Out,  0)

    def test_num_CambiosIn(self):
        df_events_cambiosIn = df_events_primer.loc[df_events_primer.event.eq(2)].copy()
        #numCambiosIn = df_events_cambiosIn.groupby('id_player').size().sort_values(ascending=False)
        datos_numCambiosIn = []
        for i in range(len(ids)):
            num_In = df_events_cambiosIn.loc[df_events_cambiosIn.id_player.eq(ids[i])]['id_player'].size
            datos_numCambiosIn.append(num_In)
            self.assertEqual(datos_numCambiosIn[i]-num_In , 0)

    def test_num_amarillas(self):
        games = df_game.loc[df_game.season.ge(1992)].id_game.to_list()
        df_events_primer = df_events.loc[df_events.id_game.isin(games)].copy()
        df_events_amarillias = df_events_primer.loc[df_events_primer.event.eq(5)].copy()
        df_events_DobleAmarillias = df_events_primer.loc[df_events_primer.event.eq(6)].copy()
        df_amarillas = pd.concat([df_events_amarillias, df_events_DobleAmarillias], ignore_index=True)

        datos_numYellow = []
        for i in range(len(ids)):
            num_games = df_amarillas.loc[df_amarillas.id_player.eq(ids[i])]['id_player'].size
            datos_numYellow.append(num_games)
            self.assertEqual(datosOF_numYellow[i]+datosOF_dobYellow[i]-num_games, 0)

    def test_num_rojas(self):
        games = df_game.loc[df_game.season.ge(1992)].id_game.to_list()
        df_events_primer = df_events.loc[df_events.id_game.isin(games)].copy()
        df_events_roja = df_events_primer.loc[df_events_primer.event.eq(4)].copy()
        df_events_DobleAmarillias = df_events_primer.loc[df_events_primer.event.eq(6)].copy()
        df_rojas = pd.concat([df_events_roja, df_events_DobleAmarillias], ignore_index=True)
        datos_numRed = []
        for i in range(len(ids)):
            num_games = df_rojas.loc[df_rojas.id_player.eq(ids[i])]['id_player'].size
            datos_numRed.append(num_games)
            self.assertEqual(datosOF_numRed[i]+datosOF_dobYellow[i]-num_games, 0)





if __name__ == '__main__':
    unittest.main()
