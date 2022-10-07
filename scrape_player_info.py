from global_variables import *
from data_cleaning import drop_rows
import requests
import pandas as pd

# Run this script once a week.  The goal of the output is to pair each player generating statistics with a team.     
def scrape_player_info():
    position = ["rushing", "passing", "receiving"]

    for element in position:
        url = (
            f"https://www.pro-football-reference.com/years/{current_year}/{element}.htm"
        )
        resp = requests.get(url)

        with open(f"./nfl_weekly_data/{current_year}_{element}_stats.xls", "wb") as f:
            f.write(resp.content)

    pi_wr = pd.read_html(f"./nfl_weekly_data/{current_year}_receiving_stats.xls")
    pi_wr = pd.DataFrame(pi_wr[0])  # Saves df var to dataframe

    pi_qb = pd.read_html(f"./nfl_weekly_data/{current_year}_passing_stats.xls")
    pi_qb = pd.DataFrame(pi_qb[0])  # Saves df var to dataframe

    pi_rb = pd.read_html(f"./nfl_weekly_data/{current_year}_rushing_stats.xls")
    pi_rb = pd.DataFrame(pi_rb[0])  # Saves df var to dataframe
    pi_rb = pi_rb.droplevel(0, axis=1)  # Removes first level column
    
    drop_rows(pi_rb)
    drop_rows(pi_wr)
    drop_rows(pi_qb)

    pi_wr['Player'] = pi_wr['Player'].map(lambda x: x.rstrip('_+!*@#$?^'))
    pi_qb['Player'] = pi_qb['Player'].map(lambda x: x.rstrip('_+!*@#$?^'))
    pi_rb['Player'] = pi_rb['Player'].map(lambda x: x.rstrip('_+!*@#$?^'))
       
    pi_wr = pi_wr[['Player', 'Tm']].copy()
    pi_rb = pi_rb[['Player', 'Tm']].copy()
    pi_qb = pi_qb[['Player', 'Tm']].copy()
      
    dfs = [pi_wr, pi_qb, pi_rb]
    player_info = pd.concat([player_info.squeeze() for player_info in dfs], ignore_index=True)
    player_info.rename(columns = {'Tm':'Team_Abbreviation'}, inplace = True)
    player_info = player_info.drop_duplicates()
    
    Team_Abbreviations_Dict = {
    'Arizona Cardinals': 'ARI', 'Cardinals': 'ARI',
    'Atlanta Falcons': 'ATL', 'Falcons': 'ATL',
    'Baltimore Ravens': 'BAL', 'Ravens': 'BAL',
    'Buffalo Bills' : 'BUF', 'Bills' : 'BUF',
    'Carolina Panthers': 'CAR', 'Panthers': 'CAR',
    'Chicago Bears': 'CHI', 'Bears': 'CHI',
    'Cincinnati Bengals': 'CIN',  'Bengals': 'CIN',
    'Cleveland Browns': 'CLE', 'Browns': 'CLE',
    'Dallas Cowboys': 'DAL',  'Cowboys': 'DAL',
    'Denver Broncos': 'DEN',  'Broncos': 'DEN',
    'Detroit Lions': 'DET',    'Lions': 'DET',
    'Green Bay Packers': 'GNB', 'Packers': 'GNB',
    'Houston Texans': 'HOU', 'Texans': 'HOU',
    'Indianapolis Colts': 'IND',  'Colts': 'IND',
    'Jacksonville Jaguars': 'JAX', 'Jaguars': 'JAX',
    'Kansas City Chiefs': 'KAN', 'Chiefs': 'KAN',
    'Miami Dolphins': 'MIA', 'Dolphins': 'MIA',
    'Minnesota Vikings': 'MIN', 'Vikings': 'MIN',
    'New England Patriots': 'NWE', 'Patriots': 'NWE',
    'New Orleans Saints': 'NOR', 'Saints': 'NO',
    'New York Giants': 'NYG', 'Giants': 'NYG',
    'New York Jets': 'NYJ', 'Jets': 'NYJ',
    'Las Vegas Raiders': 'LVR', 'Raiders': 'LVR',
    'Philadelphia Eagles': 'PHI', 'Eagles': 'PHI',
    'Pittsburgh Steelers': 'PIT', 'Steelers': 'PIT',
    'Los Angeles Chargers': 'LAC', 'Chargers': 'LAC',
    'San Francisco 49ers': 'SFO', '49ers': 'SFO',
    'Seattle Seahawks': 'SEA', 'Seahawks': 'SEA',
    'Los Angeles Rams': 'LAR', 'Rams': 'LAR',
    'Tampa Bay Buccaneers': 'TAM', 'Buccaneers': 'TAM',
    'Tennessee Titans': 'TEN', 'Titans': 'TEN',
    'Washington Commanders': 'WAS', 'Commanders': 'WAS'
    }
    player_info_dict = pd.Series(player_info.Team_Abbreviation.values,index=player_info.Player).to_dict()
    
    
    def get_key(val):
        for key, value in Team_Abbreviations_Dict.items():
            if val == value:
                return key
            return f'key does not exist --> {val}'
        
    player_info['Team_Name_Full'] = player_info['Team_Abbreviation'].map(get_key)
    
    replace_values = {'KAN': 'KC', 
                  'TAM': 'TB',
                  'SFO': 'SF', 
                  'GNB': 'GB', 
                  'NWE': 'NE',
                  'LVR': 'LV',
                  'NOR': 'NO',
                  'JAX': 'JAC'}
    player_info['players_team'] = player_info['Team_Abbreviation'].replace(replace_values)
    player_info['Team_Name_Mascot'] = player_info['Team_Name_Full'].map(lambda x: x.split()[-1])
    player_info['Team_Name_Mascot'] = player_info['Team_Name_Mascot'].replace({'NOR': 'Saints'})
    
    return player_info

