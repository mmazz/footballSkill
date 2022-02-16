from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import trueskillthroughtime as ttt
import git
from pathlib import Path

root = Path(git.Repo('.', search_parent_directories=True).working_tree_dir)
data_load_dir = root / "data/interim"
fig_save_dir = root / "reports/img"


def parameters(fileName, composition, results, times, prior_dic_names, sigmas, betas, gammas, draws, epsilons):
    it = 10
    mu = 25.0
    sigma_def = mu/2
    beta_def = mu/6
    draw_def = 0.3 # statistic value
    epsilon_def = 0.01

    evidences = []
    print("Starting gamma optimization")
    for i in range(len(gammas)):
        prior_dic = dict()
        for key in prior_dic_names:
            prior_dic[key] = ttt.Player(ttt.Gaussian(mu, sigma_def), beta_def, gammas[i])

        h = ttt.History(composition, results, times, prior_dic, mu=25.0, sigma=sigma_def,
                        beta=beta_def, gamma=gammas[i], p_draw=draw_def)
        h.convergence(epsilon=epsilon_def, verbose=False, iterations=it)
        evidence = round(h.log_evidence(), 2)
        evidences.append(evidence)

    gamma_op = gammas[np.argmax(evidences)]
    fig, ax = plt.subplots( nrows=1, ncols=1 )
    ax.plot(gammas, evidences)
    fig.savefig(fig_save_dir / 'gamma_op.png')
    plt.close(fig)
    evidences = []

    print("Starting sigma optimization")

    for i in range(len(sigmas)):
        prior_dic = dict()
        for key in prior_dic_names:
            prior_dic[key] = ttt.Player(ttt.Gaussian(mu, sigmas[i]), beta_def, gamma_op)

        h = ttt.History(composition, results, times, prior_dic, mu=25.0, sigma=sigmas[i],
                        beta=beta_def, gamma=gamma_op, p_draw=draw_def)
        h.convergence(epsilon=epsilon_def,verbose=False, iterations=it)
        evidence = round(h.log_evidence(), 2)
        evidences.append(evidence)

    sigma_op = sigmas[np.argmax(evidences)]
    fig, ax = plt.subplots( nrows=1, ncols=1 )
    ax.plot(sigmas, evidences)
    fig.savefig(fig_save_dir / 'sigma_op.png')
    plt.close(fig)
    evidences = []

    print("Starting beta optimization")
    for i in range(len(betas)):
        prior_dic = dict()
        for key in prior_dic_names:
            prior_dic[key] = ttt.Player(ttt.Gaussian(mu, sigma_op), betas[i], gamma_op)

        h = ttt.History(composition, results, times, prior_dic, mu=25.0, sigma=sigma_op,
                        beta=betas[i], gamma=gamma_op, p_draw=draw_def)
        h.convergence(epsilon=epsilon_def,verbose=False, iterations=it)
        evidence = round(h.log_evidence(), 2)
        evidences.append(evidence)

    beta_op = betas[np.argmax(evidences)]
    fig, ax = plt.subplots( nrows=1, ncols=1 )
    ax.plot(betas, evidences)
    fig.savefig(fig_save_dir / 'beta_op.png')
    plt.close(fig)
    evidences = []

    print("Starting draw optimization")
    for i in range(len(draws)):
        prior_dic = dict()
        for key in prior_dic_names:
            prior_dic[key] = ttt.Player(ttt.Gaussian(mu, sigma_op), beta_op, gamma_op)

        h = ttt.History(composition, results, times, prior_dic, mu=25.0, sigma=sigma_op,
                        beta=beta_op, gamma=gamma_op, p_draw=draws[i])
        h.convergence(epsilon=epsilon_def,verbose=False, iterations=it)
        evidence = round(h.log_evidence(), 2)
        evidences.append(evidence)

    draw_op = draws[np.argmax(evidences)]
    fig, ax = plt.subplots( nrows=1, ncols=1 )
    ax.plot(draws, evidences)
    fig.savefig(fig_save_dir / 'draw_op.png')
    plt.close(fig)
    evidences = []

    print("Starting evidence optimization")
    for i in range(len(epsilons)):
        prior_dic = dict()
        for key in prior_dic_names:
            prior_dic[key] = ttt.Player(ttt.Gaussian(mu, sigma_op), beta_op, gamma_op)

        h = ttt.History(composition, results, times, prior_dic, mu=25.0, sigma=sigma_op,
                        beta=beta_op, gamma=gamma_op, p_draw=draw_op)
        h.convergence(epsilon=epsilons[i],verbose=False, iterations=it)
        evidence = round(h.log_evidence(), 2)
        evidences.append(evidence)

    epsilon_op = epsilons[np.argmax(evidences)]
    fig, ax = plt.subplots( nrows=1, ncols=1 )
    ax.plot(epsilons, evidences)
    fig.savefig(fig_save_dir / 'draw_op.png')
    plt.close(fig)
    with open(root / f'models/{fileName}.txt', 'w') as f:
        f.write('Gamma: ')
        f.write(str(gamma_op))
        f.write('\n')
        f.write('Sigma: ')
        f.write(str(sigma_op))
        f.write('\n')
        f.write('Beta: ')
        f.write(str(beta_op))
        f.write('\n')
        f.write('Draw: ')
        f.write(str(draw_op))
        f.write('\n')
        f.write('Epsilon: ')
        f.write(str(epsilon_op))



