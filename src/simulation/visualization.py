from matplotlib import pyplot as plt
import pandas as pd
import git
from pathlib import Path

root = Path(git.Repo('.', search_parent_directories=True).working_tree_dir)
data_load_dir = root / "data/processed"
data_save_dir = root / "reports/img"

csv_path = data_load_dir / 'syntethic.csv'
df = pd.read_csv(csv_path)

messi = df.iloc[0]
companero = df.iloc[2]

companero0 = df.iloc[11]
companero1 = df.iloc[22]
companero2 = df.iloc[44]

messi.plot()
companero.plot()
#companero0.plot()
#companero1.plot()
#companero2.plot()
plt.show()
