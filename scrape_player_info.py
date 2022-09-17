from global_variables import *
import requests
import pandas as pd


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

    return pi_wr, pi_qb, pi_rb

