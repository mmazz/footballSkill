import matplotlib.pyplot as plt
import time
import datetime
import pandas as pd
import git
from pathlib import Path
plt.style.use('dark_background')
font_size = 22
ticks_size= 18
plt.rc('font', size=font_size) #controls default text size
plt.rc('axes', titlesize=font_size) #fontsize of the title
plt.rc('axes', labelsize=font_size) #fontsize of the x and y labels
plt.rc('xtick', labelsize=ticks_size) #fontsize of the x tick labels
plt.rc('ytick', labelsize=ticks_size) #fontsize of the y tick labels
plt.rc('legend', fontsize=font_size) #fontsize of the legend


root = Path(git.Repo('.', search_parent_directories=True).working_tree_dir)
data_load_dir = root / "data/processed"
fig_save_dir = root / "reports/img"

csv = data_load_dir / 'WF_TeamsSkills.csv'
df = pd.read_csv(csv, index_col=None, header=0, lineterminator='\n')

teams = ["Chelsea FC", "Manchester City", "Leeds United", "Aston Villa", "West Ham United",
        "Bolton Wanderers", "Liverpool FC"]
fig, ax = plt.subplots(1,1, figsize=(12, 9))

for i in range(len(teams)):
    mean = []
    time = []
    year = []
    rounds = []
    df_temp = df[(df.team1.eq(teams[i]) | df.team2.eq(teams[i]))]
    for index, row in df_temp.iterrows():
        if row['team1']==teams[i]:
            mean.append(row['p1_mean'])
            time.append(int(str(row['year'])+str(row['round']+100)))
        if row['team2']==teams[i]:
            mean.append(row['p2_mean'])
            time.append(int(str(row['year'])+str(row['round']+100)))
        #date.append(row['date'].split('T')[0])
        year.append(row['year'])
        rounds.append(row['round'])
    #dates = [datetime.datetime.strptime(i, '%d/%m/%Y') for i in date]
    #dates, mean = zip(*sorted(zip(dates, mean)))
    dates = [int(str(x)+str(100+y)) for x,y in zip(year,rounds)]
    ax.plot(dates, mean, label=teams[i])

ax.legend(fontsize=10)
ax.set_xlabel('Sustituciones')
fig.suptitle('Sustituciones por equipo')
fig.tight_layout()
plt.show()
fig.savefig(fig_save_dir/'skills.png', dpi=300)
plt.close(fig)
fig, ax = plt.subplots(1,1, figsize=(12, 9))
'''
for i in range(len(teams)):
    mean = []
    time = []
    date = []
    df_temp = df[(df.team1.eq(teams[i]) | df.team2.eq(teams[i]))]
    for index, row in df_temp.iterrows():
        if row['team1']==teams[i]:
            mean.append(row['p1_std'])
            time.append(int(str(row['year'])+str(row['round']+100)))
        if row['team2']==teams[i]:
            mean.append(row['p2_std'])
            time.append(int(str(row['year'])+str(row['round']+100)))
        date.append(row['date'].split('T')[0])
    dates = [datetime.datetime.strptime(i, '%d/%m/%Y') for i in date]
    dates, mean = zip(*sorted(zip(dates, mean)))
    ax.plot(dates, mean, label=teams[i])

ax.legend(fontsize=10)
ax.set_xlabel('Sustituciones')
fig.suptitle('Sustituciones por equipo')
fig.tight_layout()
plt.show()
fig.savefig(fig_save_dir/'skills.png', dpi=300)
plt.close(fig)

'''

# total de partidos jugados por jugador




