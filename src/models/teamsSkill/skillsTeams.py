import pandas as pd
import git
from pathlib import Path
import trueskillthroughtime as ttt


root = Path(git.Repo('.', search_parent_directories=True).working_tree_dir)
data_load_dir = root / "data/interim"
data_save_dir = root / "data/processed"

csv_game = data_load_dir / 'GamesInfo_features.csv'
df = pd.read_csv(csv_game, index_col=None, header=0, lineterminator='\n')


df = df[df.year.ge(2000)]
df = df.sort_values(by=['year', 'round'])
# Ravel gives flattern data
column_teams = df[["team1", "team2"]].values.ravel()
unique_teams =  pd.unique(column_teams).tolist()

year  = df['year'].tolist()
rounds = df['round'].tolist()
rounds_list = [int(str(x)+str(100+y)) for x,y in zip(year,rounds)]
dates = year
dates = [i for i in range(df.shape[0])]
dates = rounds_list

results = []
for res in df.local_win:
    # First team wins
    if res == 1:
        results.append([1,0])
    elif res == 0:
        results.append([0,1])
    # Draw
    else:
        results.append([0,0])

composition = []
print("Starting composition appending")
for index, row in df.iterrows():
    composition.append([[row['team1']], [row['team2']]])

print("End composition appending")
with open(root / 'models/parameters_teams.txt') as f:
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
for key in unique_teams:
    prior_dict[str(key)] = ttt.Player(ttt.Gaussian(25., sigma), beta, gamma)

h = ttt.History(composition, results, dates, prior_dict, mu=25.0, sigma=sigma,beta=beta,
                            gamma=gamma, p_draw=draw)

h.convergence(verbose=False, epsilon=0.01, iterations=iterations)

ttt_ev.append(h.log_evidence())

p1_mean = []
p2_mean = []
p1_std = []
p2_std = []
evidence = []
for t in h.batches:
    for i in range(len(t)):
        p1 = t.events[i].names[0][0]
        p2 = t.events[i].names[1][0]
        p1_mean.append(t.posterior(str(p1)).mu)
        p1_std.append(t.posterior(str(p1)).sigma)
        p2_mean.append(t.posterior(str(p2)).mu)
        p2_std.append(t.posterior(str(p2)).sigma)
        evidence.append(t.events[i].evidence)


res = df[['team1', 'team2', 'porcentage_attendance', 'local_win', 'year','round', 'tournament', 'date']].copy()
res["p1_mean"] = p1_mean
res["p1_std"] = p1_std
res["p2_mean"] = p2_mean
res["p2_std"] = p2_std
res["evidence"] = evidence

csv_path = data_save_dir / 'TeamsSkills.csv'
res.to_csv(csv_path, index=False)
