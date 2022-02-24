import trueskillthroughtime as ttt
from matplotlib import pyplot as plt
import numpy as np
import git
import os
from pathlib import Path
import math
import random
from numpy.random import normal, seed;
import pandas as pd
root = Path(git.Repo('.', search_parent_directories=True).working_tree_dir)
data_load_dir = root / "data/interim"
data_save_dir = root / "data/processed"
print("synthatic")

seed(99);
random.seed(99)
N=1000
NUM_TEAMS = 20
NUM_PLAYERS = 11
NUM_INT_GAMES = 8
NUM_SELECTIONS = 16
NUM_SEASSON_GAMES = 380 # 38 rondas de 10 partidos

teams = dict()
id_player = 0
# Me armo los equipos con sus jugadores
for i in range(NUM_TEAMS):
    teams[str(i)] = []
    for j in range(NUM_PLAYERS):
        teams[str(i)].append(str(id_player))
        id_player+=1

SIGMA_skill = 0.5 # Its the one thats sets real skills
NUM_BAD_TEAMS = 4
NUM_GOOD_TEAMS = 2
MU_bad = 0
MU_med = 1
MU_good = 2
SIGMA = 5
BETA = 1
GAMMA = 0.1
EPSILON = 0.01
composition = []

print("mu medio: ", MU_med, " beta: ", BETA)
def composition_seasson(teams, composition, lim=1):
    copyTeams = teams.copy()
    numTeams = len(copyTeams.keys())
    teamInUse = 0
    while(numTeams>lim):
        for i in range(teamInUse, len(teams.keys())-lim, 1):
            composition.append([copyTeams[str(teamInUse)],copyTeams[str(i+1)]])
            composition.append([copyTeams[str(i+1)],copyTeams[str(teamInUse)]])
        copyTeams.pop(str(teamInUse))
        teamInUse+=1
        numTeams = len(copyTeams.keys())

# Me armo la temporada de partidos, y los desordeno para simular
# que es una temporada (asi podria pasar que el ida y vuelta se den en dias
# consecutivos...)
composition_seasson(teams, composition)
random.shuffle(composition)

# agrego al final 8 partidos por jugador de equipos inventados como si fueran
# de seleccion
players =[str(i) for i in range(NUM_TEAMS*NUM_PLAYERS)]
# forma sucia de asegurarme que el jugador estrella 0 este en una seleccion
temp = players[:2]
temp2 = players[2:]
random.shuffle(temp2)
players = temp + temp2
selections = dict()
def international_teams(NUM_SELECTIONS, selections, players):
    for i in range(NUM_SELECTIONS):
        selections[str(i)] = players[i*11:i*11+11]

international_teams(NUM_SELECTIONS, selections, players)

def composition_international(NUM_INT_GAMES, composition, selections):
    for i in range(NUM_INT_GAMES):
        composition.append([selections[str(i)],selections[str(NUM_SELECTIONS-i-1)]])
        composition.append([selections[str(NUM_SELECTIONS-i-1)],selections[str(i)]])

composition_seasson(selections, composition, 12)

priors = dict()
for i in range(NUM_PLAYERS*NUM_TEAMS):
    priors[str(i)] = ttt.Player(ttt.Gaussian(MU_med, SIGMA))

# Las habilidades reales fijas de los jugadores
players_skills = dict()
for i in range(NUM_PLAYERS*NUM_TEAMS):
    if i<=NUM_GOOD_TEAMS*NUM_PLAYERS:
        players_skills[str(i)] = np.random.normal(MU_good, SIGMA_skill, 1)
    elif i>NUM_GOOD_TEAMS*NUM_PLAYERS & i<=NUM_BAD_TEAMS*NUM_PLAYERS:
        players_skills[str(i)] = np.random.normal(MU_bad, SIGMA_skill, 1)
    else:
        players_skills[str(i)] = np.random.normal(MU_med, SIGMA_skill, 1)

# Jugador estrella
players_skills[str(0)] += BETA
print('Skill Messi:', players_skills[str(0)])
print('Skill Compa�ero de Messi:', players_skills[str(2)])
print('Skill jugador equipo malo:', players_skills[str(22)])
# Considero que la habilidad real del equipo es la media de los jugadores
def teams_skill(players_skills, team1, team2):
    mu1 = 0
    mu2 = 0
    N1 = 0
    N2 = 0
    for i in range(len(team1)):
        mu1 += float(players_skills[str(team1[i])])
        N1 += 1
    for i in range(len(team2)):
        mu2 += float(players_skills[str(team2[i])])
        N2 += 1
    return mu1/N1, mu2/N2

results = []
for round in range(len(composition)):
    mu1, mu2 = teams_skill(players_skills, composition[round][0], composition[round][1])
    results.append([1.,0.] if normal(mu1, SIGMA_skill) > normal(mu2, SIGMA_skill) else [0.,1.])

times = [i for i in range(len(composition))]
h = ttt.History(composition, results, times, priors, mu=MU_med, gamma=GAMMA)
h.convergence(epsilon=EPSILON,verbose=False)

trueskill_mu = dict()
trueskill_sigma = dict()

for player_id in range(NUM_PLAYERS*NUM_TEAMS):
    trueskill_mu[player_id] = []
    trueskill_sigma[player_id] = []

print(h)
for player_id in range(NUM_PLAYERS*NUM_TEAMS) :
    for batch in h.learning_curves()[str(player_id)]:
        trueskill_mu[player_id].append(batch[1].mu)
        trueskill_sigma[player_id].append(batch[1].sigma)
    if len(trueskill_mu[player_id])<46:
        for i in range(8):
            trueskill_mu[player_id].append(trueskill_mu[player_id][-1])

df = pd.DataFrame.from_dict(trueskill_mu)
df = df.transpose()
csv_path = data_save_dir / f'{os.path.basename(__file__).strip(".py")}.csv'
df.to_csv(csv_path, index=False)
print(df.head())



