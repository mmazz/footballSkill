import matplotlib.pyplot as plt
import time
import pandas as pd
import git
from pathlib import Path
import os
import sys
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
fpath = os.path.join(root, 'src')
sys.path.append(fpath)
import utils.functions as fun



data_load_dir = root / "data/processed"
fig_save_dir = root / "srceports/img"

csv = data_load_dir / 'skillHomePlayer.csv'
df = pd.read_csv(csv, index_col=None, header=0, lineterminator='\n')

csv_stadiums =  root / "data/interim"/ 'WFI_StadiumsInfoComplete_extra.csv'
df_stadiums = pd.read_csv(csv_stadiums, index_col=None, header=0, lineterminator='\n')


mean_loc = dict()
std_loc = dict()
time = dict()
year = []
rounds = []
i = 0
for index, row in df.iterrows():
    id_stadium = row['id_stadium']
    team1 = df_stadiums.loc[df_stadiums['id_stadium'].eq(id_stadium), 'team'].values[0]
    if (team1 == row['team1']) & (row['porcentage_attendance']>=0.5):
        if team1 in mean_loc:
            mean_loc[team1].append(row['p1_loc_mean'])
            time[team1].append(int(str(row['year'])+fun.days(str(row['round']))) )
        else:
            mean_loc[team1] = [row['p1_loc_mean']]
            time[team1] = [int(str(row['year'])+fun.days(str(row['round'])))]


teams = ["Chelsea FC", "Manchester City", "Leeds United", "West Ham United",
        "Bolton Wanderers", "Liverpool FC"]

fig, ax = plt.subplots(1,1, figsize=(12, 9))

for i in teams:
    ax.plot(time[i], mean_loc[i], label=f"localy {i}")
    ax.legend(fontsize=10)
    ax.set_xlabel('Time')
fig.suptitle('Locally skill')
fig.tight_layout()

plt.show()
fig.savefig('./img/skillsIndividualLocaly.png', dpi=300)
plt.close(fig)

fig, ax = plt.subplots(1,1, figsize=(12, 9))

for i in teams:
    df_temp = df[(df['team1'].eq(i)) | (df['team2'].eq(i))]
    mean, std, time = fun.player_skill(df_temp, i)
    ax.plot(time, mean, label=f"localy {i}")
    ax.legend(fontsize=10)
    ax.set_xlabel('Time')
fig.suptitle('Teams skill')
fig.tight_layout()

plt.show()
fig.savefig('./img/skillsIndividualTeams.png', dpi=300)
plt.close(fig)







# total de partidos jugados por jugador




