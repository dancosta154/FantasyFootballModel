import requests
import pandas as pd
import re

url = 'https://www.pro-football-reference.com/years/2022/opp.htm'
res = requests.get(url)
with open('./nfl_data/weekly/defensive_ranks.xls', 'wb') as f:
    f.write(res.content)
    
# Set the defensive week to the week you care about; default is current_week
defensive_week = 1

df_def = pd.read_html('./nfl_data/weekly/defensive_ranks.xls')
df_def = pd.DataFrame(df_def[0]) 
df_def = df_def.droplevel(0, axis=1)
df_def = df_def.rename(columns = {'Tm':'Team', 'Rk': 'Rank'})
df_def = df_def.iloc[:, [0,1]].copy() # filter to only Rank and Team
df_def['Tm_Abr'] = df_def['Team'].map(lambda x: Team_Abbreviations_Dict.get(x)) # tack on column with corresponding team abbreviation
df_def.drop(index = [32,33,34], axis = 0, inplace = True) # drop the average and total rows
df_def['Current_Week'] = defensive_week
df_def['Team_Mascot'] = df_def['Team'].map(lambda x: x.split()[-1])
df_def.rename(columns = {'Rank': f'Def_Rank_Week_{current_week}'}, inplace = True)
df_def.head()