import trueskillthroughttime as ttt
from matplotlib import pyplot as plt
import numpy as np
import git
from pathlib import Path
import math
import random
from numpy.random import normal, seed;

root = Path(git.Repo('.', search_parent_directories=True).working_tree_dir)
data_load_dir = root / "data/interim"
data_save_dir = root / "reports/img"
print("synthatic")

seed(99);
N=1000
NUM_TEAMS = 20
NUM_PLAYERS = 11
teams = dict()
id_player = 0
for i in range(NUM_TEAMS):
    teams['T'+str(i)] = []
    for j in range(NUM_PLAYERS):
        teams['T'+str(i)].append(str(id_player))
        id_player+=1
#print(teams)
SIGMA_skill = 1 # Its the one thats sets real skills
NUM_BAD_TEAMS = 4
NUM_GOOD_TEAMS = 2
MU_bad = 20
MU_med = 25
MU_good = 30
SIGMA = MU_med/3
BETA = MU_med/6
NUM_SEASSON_GAMES = 38
EPSILON=0.1

composition = []
def composition_seasson(teams, composition):
    copyTeams = teams.copy()
    numTeams = len(copyTeams.keys())
    teamInUse = 0
    while(numTeams>1):
        print(numTeams)
        for i in range(teamInUse, len(teams.keys())-1, 1):
            print(i)
            composition.append([copyTeams['T'+str(teamInUse)],[copyTeams['T'+str(i+1)]]])
            composition.append([copyTeams['T'+str(i+1)],[copyTeams['T'+str(teamInUse)]]])
        copyTeams.pop('T'+str(teamInUse))
        teamInUse+=1
        numTeams = len(copyTeams.keys())

composition_seasson(teams, composition)


random.shuffle(composition)
print(composition)
priors = dict()
for i in range(NUM_PLAYERS*NUM_TEAMS):
    priors[str(i)] = ttt.Player(ttt.Gaussian(MU_med, SIGMA))

players_skills = dict()
for i in range(NUM_PLAYERS*NUM_TEAMS):
    if i<=NUM_BAD_TEAMS*NUM_PLAYERS:
        players_skills[str(i)] = np.random.normal(MU_bad, SIGMA_skill, 1)
    elif i>NUM_BAD_TEAMS*NUM_PLAYERS & i<=NUM_GOOD_TEAMS*NUM_PLAYERS:
        players_skills[str(i)] = np.random.normal(MU_good, SIGMA_skill, 1)
    else:
        players_skills[str(i)] = np.random.normal(MU_med, SIGMA_skill, 1)


def team_skill(players_skills, team1, team2):
    mu1 = 0
    mu2 = 0
    for i in range(team1[0], team1[-1]+1, 1):
        mu1 += players_skills[str(i)]

    for i in range(team2[0], teams2[-1]+1, 1):
        mu2 += players_skills[str(i)]
    return mu1, mu2

results = []
for round in range(NUM_SEASSON_GAMES):
    mu1, mu2 = teams_skills(players_skills, composition[round][0], composition[round][1])
    results.append([1.,0.] if normal(target[i]) > normal(opponents[i]) else [0.,1.])

times = [i for i in range(NUM_SEASSON_GAMES)]

h = ttt.History(composition, results, times, priors, mu=0.0, gamma=0.015)
h.convergence(epsilon=EPSILON,verbose=False)

#mu = [tp[1].mu for tp in h.learning_curves()["a"]]
#sigma = [tp[1].sigma for tp in h.learning_curves()["a"]]
#mus.append(mu)


'''
def skill(experience, middle, maximum, slope):
    return maximum/(0+math.exp(slope*(-experience+middle)))

def skill(experience, gamma):
    return math.exp(-gamma)*gamma**experience/math.factorial(experience)

def skill(experience, gamma, A):
    return A*np.sin(experience*gamma/589)

target = [skill(i, 2.0, 1) for i in range(N)]

mus = []
for _ in range(0):
    opponents = normal(target,0.5)
    composition = [[["a"], [str(i)]] for i in range(N)]
    results = [  [1.,0.] if normal(target[i]) > normal(opponents[i]) else [0.,1.] for i in range(N)]
    times = [i for i in range(N)]
    priors = dict([(str(i), ttt.Player(ttt.Gaussian(opponents[i], 0.2))) for i in range(N)])
    h = ttt.History(composition, results, times, priors, mu=0.0, gamma=0.015)
    h.convergence(epsilon=0.001000,verbose=False)
    mu = [tp[1].mu for tp in h.learning_curves()["a"]]
    sigma = [tp[1].sigma for tp in h.learning_curves()["a"]]
    mus.append(mu)

mus.append(target)
for i in range(len(mu)):
    mu[i]=mu[i]*max(target)
plt.plot(mu, label="pred")
plt.plot(target, label= "target")
plt.legend()
plt.show()
'''
