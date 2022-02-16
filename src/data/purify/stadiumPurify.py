import pandas as pd
import numpy as np
from pathlib import Path
import git

root = Path(git.Repo('.', search_parent_directories=True).working_tree_dir)
data_load_dir = root / "data/raw"
data_save_dir = root / "data/interim"

csv_stadiums = data_load_dir / 'StadiumsInfo.csv'
df_stadiums = pd.read_csv(csv_stadiums, index_col=None, header=0, lineterminator='\n')

df_stadiums['last_year'] = np.zeros(len(df_stadiums),dtype=int)
df_stadiums.loc[df_stadiums.stadium=='Manor Ground', 'team'] = 'Oxford United'
df_stadiums.loc[df_stadiums.stadium=='Manor Ground', 'last_year'] = 2001
df_stadiums.loc[df_stadiums.stadium=='White Hart Lane', 'team'] = 'Tottenham Hotspur'
df_stadiums.loc[df_stadiums.stadium=='White Hart Lane', 'last_year'] = 2017
df_stadiums.loc[df_stadiums.stadium=='The Dell', 'team'] = 'Southampton FC'
df_stadiums.loc[df_stadiums.stadium=='The Dell', 'last_year'] = 2001
df_stadiums.loc[df_stadiums.stadium=='Roker Park', 'team'] = 'Sunderland AFC'
df_stadiums.loc[df_stadiums.stadium=='Roker Park', 'last_year'] = 1997
df_stadiums.loc[df_stadiums.stadium=='Baseball Ground', 'team'] = 'Derby County'
df_stadiums.loc[df_stadiums.stadium=='Baseball Ground', 'last_year'] = 1997
df_stadiums.loc[df_stadiums.stadium=='Highfield Road', 'team'] = 'Coventry City'
df_stadiums.loc[df_stadiums.stadium=='Highfield Road', 'last_year'] = 2006
df_stadiums.loc[df_stadiums.stadium=='Highbury', 'team'] = 'Arsenal FC'
df_stadiums.loc[df_stadiums.stadium=='Highbury', 'last_year'] = 2006
df_stadiums.loc[df_stadiums.stadium=='Maine Road', 'team'] = 'Manchester City'
df_stadiums.loc[df_stadiums.stadium=='Maine Road', 'last_year'] = 2003
df_stadiums.loc[df_stadiums.stadium=='Upton Park', 'team'] = 'West Ham United'
df_stadiums.loc[df_stadiums.stadium=='Upton Park', 'last_year'] = 2016
df_stadiums.loc[df_stadiums.stadium=='Filbert Street', 'team'] = 'Leicester City'
df_stadiums.loc[df_stadiums.stadium=='Filbert Street', 'last_year'] = 2002
df_stadiums.loc[df_stadiums.stadium=='Leeds Road', 'team'] = 'Huddersfield Town'
df_stadiums.loc[df_stadiums.stadium=='Leeds Road', 'last_year'] = 1994
df_stadiums.loc[df_stadiums.stadium=='The Victoria Ground', 'team'] = 'Stoke City'
df_stadiums.loc[df_stadiums.stadium=='The Victoria Ground', 'last_year'] = 1997
df_stadiums.loc[df_stadiums.stadium=='Boothferry Park', 'team'] = 'Hull City'
df_stadiums.loc[df_stadiums.stadium=='Boothferry Park', 'last_year'] = 2002
df_stadiums.loc[df_stadiums.stadium=='Vetch Field', 'team'] = 'Swansea City'
df_stadiums.loc[df_stadiums.stadium=='Vetch Field', 'last_year'] = 2005
df_stadiums.loc[df_stadiums.stadium=='Ayresome Park', 'team'] = 'Middlesbrough FC'
df_stadiums.loc[df_stadiums.stadium=='Ayresome Park', 'last_year'] = 1995
df_stadiums.loc[df_stadiums.stadium=='Goldstone Ground', 'team'] = 'Brighton & Hove Albion'
df_stadiums.loc[df_stadiums.stadium=='Goldstone Ground', 'last_year'] = 1997
df_stadiums.loc[df_stadiums.stadium=='Burnden Park', 'team'] = 'Bolton Wanderers'
df_stadiums.loc[df_stadiums.stadium=='Burnden Park', 'last_year'] = 1997

df_stadiums['stadium'] = df_stadiums['stadium'].apply(lambda x: x[:-1] if x[-1]==' ' else x)
csv_stadium = data_save_dir / 'StadiumsInfo_purify.csv'

df_stadiums.to_csv(csv_stadium, index=False)
