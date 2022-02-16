import pandas as pd
import git
from pathlib import Path
import os
import sys


root = Path(git.Repo('.', search_parent_directories=True).working_tree_dir)
data_load_dir = root / "data/interim"
fig_save_dir = root / "reports/img"

fpath = os.path.join(root, 'src')
sys.path.append(fpath)
import utils.findParameters as util

csv_game = data_load_dir / 'GamesInfo_features.csv'
df = pd.read_csv(csv_game, index_col=None, header=0, lineterminator='\n')

csv_stadiums = data_load_dir / 'StadiumsInfo_purify.csv'
df_stadiums = pd.read_csv(csv_stadiums, index_col=None, header=0, lineterminator='\n')

df = df[df.year.ge(1990)]


column_values = df[["team1", "team2"]].values.ravel()
unique_values =  pd.unique(column_values).tolist()

results = []
year  = df['year'].tolist()
rounds = df['round'].tolist()
rounds_list = [int(str(x)+str(y)) for x,y in zip(year,rounds)]
dates = year


print("results")
for res in df.local_win:
    if res == 1:
        results.append([0,1])
    elif res == 0:
        results.append([1,0])
    else:
        results.append([0,0]) # chequear

print("composition")
composition = []
print("Starting composition appending")
for index, row in df.iterrows():
    id_stadium = row['id_stadium']
    #check if the local team its actually playing as local.
    team1 = df_stadiums.loc[df_stadiums['id_stadium'].eq(id_stadium), 'team'].values[0]
    if team1 == row['team1']:
        if row['porcentage_attendance']>=0.5:
            composition.append([[row['team1'], f"localia_{row['team1']}"], [row['team2']]])
        else:
            composition.append([[row['team1']], [row['team2']]])
    else:
        composition.append([[row['team1']], [row['team2']]])

gammas = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08]
sigmas = [ 4.17,  8.33, 12.5, 16.67, 20.83, 25., 29.17]
betas = [25/2, 25/3, 25/4, 25/5, 25/5, 25/6]
draws = [0.1, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45]
epsilons = [0.001, 0.01, 0.1, 1, 10]
dates = [i for i in range(len(composition))]


util.parameters("parameters_local", composition, results, dates, unique_values, sigmas, betas, gammas, draws, epsilons)

