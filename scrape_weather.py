import requests
import pandas as pd
import numpy as np
import re
from global_variables import *

def scrape_weather():
    weeks = [f'week-{week}' for week in range(starting_week, current_week)]

    file_list = []

    for week in weeks:
        url = f'https://www.nflweather.com/en/week/{current_year}/{week}/'
        res = requests.get(url)
        output = open(f'./nfl_weekly_data/weather/weather_week{week}.xls', 'wb')
        output.write(res.content)
        file_list.append(f'./nfl_weekly_data/weather/weather_week{week}.xls')
        output.close()
        
    dfs = []
    for file in file_list:
        data = pd.read_html(file)
        df2 = pd.DataFrame(data[0])
        df2.drop(columns = ['Unnamed: 0', 'Game', 'Game.1', 'Game.2', 'Time (ET)', 'TV', 'Unnamed: 8', 'Unnamed: 12'], inplace = True) 
        df2['Week'] = re.search(r'(\d+)', file)[0]
        df2['Wind_Speed_MPH'] = df2['Wind'].map(lambda x:re.search(r'(\d+)',x)[0])
        df2['Wind_Direction'] = df2['Wind'].map(lambda x:re.search(r'[A-Z]+',x)[0])
        df2['Temp'] = df2['Forecast'].map(lambda x: re.search(r'(\d+)',x)[0] if x != 'DOME' else 0)
        df2['Weather_Desc'] = df2['Forecast'].map(lambda x: re.search(r'\s(.+)',x)[0].strip() if x != 'DOME' else 0)
        df2["Wind"] = np.where(df2["Forecast"] == "DOME", 0, df2["Wind"])
        df2["Wind_Speed_MPH"] = np.where(df2["Forecast"] == "DOME", 0, df2["Wind_Speed_MPH"])
        df2["Wind_Direction"] = np.where(df2["Forecast"] == "DOME", 0, df2["Wind_Direction"])
        dfs.append(df2)
    weather_df = pd.concat(dfs, ignore_index=True)
    weather_df.rename(columns = {'Away': 'away_team', 'Home': 'home_team'}, inplace= True)
    weather_df['Week'] = weather_df['Week'].astype(int)
        
    return weather_df
    
print(scrape_weather())