import pandas as pd
import git
from pathlib import Path
import trueskillthroughtime as ttt
import os

root = Path(git.Repo('.', search_parent_directories=True).working_tree_dir)
data_load_dir = root / "data/interim"
data_save_dir = root / "data/processed"

csv_game = data_load_dir / 'GamesInfo_features.csv'
df = pd.read_csv(csv_game, index_col=None, header=0, lineterminator='\n')

csv_stadiums = data_load_dir / 'StadiumsInfo_purify.csv'
df_stadiums = pd.read_csv(csv_stadiums, index_col=None, header=0, lineterminator='\n')

df = df[df.year.ge(2000)]
df = df.sort_values(by=['year', 'round'])

column_values = df[["team1", "team2"]].values.ravel()
unique_values =  pd.unique(column_values).tolist()

results = []
year  = df['year'].tolist()
rounds = df['round'].tolist()
rounds_list = [int(str(x)+str(100+y)) for x,y in zip(year,rounds)]
times = rounds_list
times = [i for i in range(df.shape[0])]

for res in df.local_win:
    if res == 1:
        results.append([1,0])
    elif res == 0:
        results.append([0,1])
    else:
        results.append([0,0]) # chequear

composition = []
print("Starting composition appending")
# Asumo que el jugador 1 juega de local. Distingo 3 tipos de jugador localia
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

print("End composition appending")
with open(root / 'modelsData/parameters.txt') as f:
    lines = f.readlines()
    for i in lines:
        variable = i.split(':')
        if variable[0] == "Gamma":
            gamma = float(variable[1].strip('\n'))
        elif variable[0] == "Sigma":
            sigma = float(variable[1].strip('\n'))
        elif variable[0] == "Beta":
            beta = float(variable[1].strip('\n'))
        elif variable[0] == "Draw":
            draw = float(variable[1].strip('\n'))

evidences = []
iterations = 10
ttt_ev = []

prior_dict = dict()
for key in unique_values:
    prior_dict[str(key)] = ttt.Player(ttt.Gaussian(25., sigma), beta, gamma)
    prior_dict["localia_"+str(key)] = ttt.Player(ttt.Gaussian(3.5, sigma), beta, gamma)
    h = ttt.History(composition, results, times , prior_dict, mu=25.0, sigma=sigma,beta=beta,
                            gamma=gamma, p_draw=draw)



h.convergence(verbose=False, epsilon=0.01, iterations=iterations)
ttt_ev.append(h.log_evidence())

p1_mean = []
p2_mean = []
p1_std = []
p2_std = []
p1_loc_mean = [] #[ t.posterior(str('localia_'+str(w))).mu for t,w in zip(h.batches,df.player1) ]
p1_loc_std = []
evidence = []
for t in h.batches:
    for i in range(len(t)):
        p1 = t.events[i].names[0][0]
        try:
            p1_loc = t.events[i].names[0][1]
            p1_loc_mean.append(t.posterior(str(p1_loc)).mu)
            p1_loc_std.append(t.posterior(str(p1_loc)).sigma)
        except: # repeat last value
            p1_loc = 'none'
            p1_loc_mean.append(p1_loc_mean[-1])
            p1_loc_std.append(p1_loc_std[-1])
        p2 = t.events[i].names[1][0]
        p1_mean.append(t.posterior(str(p1)).mu)
        p1_std.append(t.posterior(str(p1)).sigma)
        p2_mean.append(t.posterior(str(p2)).mu)
        p2_std.append(t.posterior(str(p2)).sigma)
        evidence.append(t.events[i].evidence)


res = df[['team1', 'team2', 'porcentage_attendance', 'id_stadium', 'local_win', 'year','round', 'tournament', 'date']].copy()
res["p1_mean"] = p1_mean
res["p1_std"] = p1_std
res["p2_mean"] = p2_mean
res["p2_std"] = p2_std
res["p1_loc_mean"] = p1_loc_mean
res["p1_loc_std"] = p1_loc_std
res["evidence"] = evidence

csv_path = data_save_dir / f'{os.path.basename(__file__).strip(".py")}.csv'
res.to_csv(csv_path, index=False)
