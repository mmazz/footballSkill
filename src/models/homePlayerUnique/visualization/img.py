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

csv = data_load_dir / 'skillHomePlayerUnique.csv'
df = pd.read_csv(csv, index_col=None, header=0, lineterminator='\n')

csv_stadiums =  root / "data/interim/StadiumsInfo_purify.csv"
df_stadiums = pd.read_csv(csv_stadiums, index_col=None, header=0, lineterminator='\n')

fig, ax = plt.subplots(1,1, figsize=(12, 9))

mean_locmax = []
mean_locmed = []
mean_locmin = []
timeMax = []
timeMed = []
timeMin = []
year = []
rounds = []
i = 0

for index, row in df.iterrows():
    id_stadium = row['id_stadium']
    team1 = df_stadiums.loc[df_stadiums['id_stadium'].eq(id_stadium), 'team'].values[0]
    if team1 == row['team1']:
        if row['porcentage_attendance']>=0.75:
            mean_locmax.append(row['p1_loc_mean'])
            timeMax.append(i)
        elif (row['porcentage_attendance']>=0.0) & (row['porcentage_attendance']<0.75):
            mean_locmed.append(row['p1_loc_mean'])
            timeMed.append(i)
        elif row['porcentage_attendance']<0.5:
            mean_locmin.append(row['p1_loc_mean'])
            timeMin.append(i)
    i = i + 1

ax.plot(timeMax, mean_locmax, label="Max localy")
ax.plot(timeMed, mean_locmed, label="Med localy")
#ax.plot(timeMin, mean_locmin, label="Min localy")

ax.legend(fontsize=10)
ax.set_xlabel('Time')
fig.suptitle('Locally skill')
fig.tight_layout()
plt.show()
fig.savefig('./img/skillsLocaly.png', dpi=300)
plt.close(fig)


fig, ax = plt.subplots(1,1, figsize=(12, 9))
mean_locmax = []
mean_locmed = []
mean_locmin = []
timeMax = []
timeMed = []
timeMin = []
year = []
rounds = []
for index, row in df.iterrows():
    if row['porcentage_attendance']>=0.75:
        mean_locmax.append(row['p1_loc_std'])
        timeMax.append(int(str(row['year'])+str(row['round']+100)))
    elif (row['porcentage_attendance']>=0.0) & (row['porcentage_attendance']<0.75):
        mean_locmed.append(row['p1_loc_std'])
        timeMed.append(int(str(row['year'])+str(row['round']+100)))
    elif row['porcentage_attendance']<=0.33:
        mean_locmin.append(row['p1_loc_std'])
        timeMin.append(int(str(row['year'])+str(row['round']+100)))

ax.plot(timeMax, mean_locmax, label="Max localy")
ax.plot(timeMed, mean_locmed, label="Med localy")
#ax.plot(timeMin, mean_locmin, label="Min localy")
print(len(timeMax))
print(len(timeMed))
print(len(timeMin))

ax.legend(fontsize=10)
ax.set_xlabel('Time')
fig.tight_layout()
plt.show()
fig.savefig('./img/skills.png', dpi=300)
plt.close(fig)

# total de partidos jugados por jugador




