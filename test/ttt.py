import trueskillthroughtime as ttt
from matplotlib import pyplot as plt
import numpy as np
import git
from pathlib import Path

root = Path(git.Repo('.', search_parent_directories=True).working_tree_dir)
data_load_dir = root / "data/interim"
data_save_dir = root / "reports/img"

c1 = [["a"],["b"]]
c2 = [["b"],["c"]]
c3 = [["c"],["a"]]

c = [c1,c2,c3]
h = ttt.History(c, mu=0.0,  sigma=6.0, beta=1.0, gamma=0.0, p_draw=0.0)
h.convergence(verbose=False)

lc = h.learning_curves()

print(lc["a"])
print(lc["b"])
print(lc["c"])
print("Results form")

composition = []
results = []
times = []
size=100

for i in range(size):
    composition.append([["a"],["b"]])
    results.append([0,1])
    times.append(i)
h = ttt.History(composition, results, times, mu=0.0,  sigma=6.0, beta=1.0, gamma=0.0, p_draw=0.3)
h.convergence(verbose=False)
for i in range(5):
    a = h.learning_curves()["a"][-1-i][1]
    b = h.learning_curves()["b"][-1-i][1]
    print("a: ", a, ' b: ', b)
print("[0,1] second wins")
print(" ")
print("draw")

composition = []
results = []
times = []
size=100

for i in range(size):
    composition.append([["a"],["b"]])
    results.append([0,0])
    times.append(i)
h = ttt.History(composition, results, times, mu=0.0,  sigma=6.0, beta=1.0, gamma=0.0, p_draw=0.3)
h.convergence(verbose=False)

for i in range(5):
    a = h.learning_curves()["a"][-1-i][1]
    b = h.learning_curves()["b"][-1-i][1]
    print(a, ' ', b)

print("synthatic")

import math; from numpy.random import normal, seed;
seed(99);
N=1000
def skill(experience, middle, maximum, slope):
    return maximum/(1+math.exp(slope*(-experience+middle)))

def skill(experience, gamma):
    return math.exp(-gamma)*gamma**experience/math.factorial(experience)

def skill(experience, gamma, A):
    return A*np.sin(experience*gamma/590)

target = [skill(i, 3.0, 1) for i in range(N)]

mus = []
for _ in range(1):
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

