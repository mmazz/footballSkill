import numpy as np
import matplotlib.pyplot as plt
import git
from pathlib import Path
import pandas as pd

root = Path(git.Repo('.', search_parent_directories=True).working_tree_dir)
data_load_dir = root / "data/interim"


csv_game = data_load_dir / 'GamesInfo_features.csv'
df_game = pd.read_csv(csv_game, index_col=None, header=0, lineterminator='\n')

csv_player = data_load_dir / 'PlayersActivity.csv'
df_activity = pd.read_csv(csv_player, index_col=None, header=0, lineterminator='\n')


df_activity = df_activity[df_activity['1'].ge(0)]

activity = df_activity.loc[[3451]].values[0]
plt.plot(activity[1:])
plt.show()
