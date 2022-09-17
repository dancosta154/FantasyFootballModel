import pandas as pd
import re
import requests


def scrape_statistics():
    # Set the weeks in which you would like to pull data
    starting_week = 1
    current_week = 1
    current_year = 2022

    all_positions = ["QB", "WR", "RB", "TE", "K"]
    weeks = [week for week in range(starting_week, current_week + 1)]

    file_list = []

    for position in all_positions:
        for week in weeks:
            url = f"https://www.cbssports.com/nfl/stats/leaders/live/{position}/{week}/"
            res = requests.get(url)
            output = open(f"./nfl_weekly_data/week-{week}_{position}.xls", "wb")
            output.write(res.content)
            file_list.append(f"./nfl_weekly_data/week-{week}_{position}.xls")
            output.close()
            data = pd.read_html(f"./nfl_weekly_data/week-{week}_{position}.xls")
            df = data[0]

    position_list = all_positions
    dfs = []
    for file in file_list:
        for i in range(len(position_list)):
            if position_list[i] in file:
                data = pd.read_html(file)
                df2 = pd.DataFrame(data[0])
                if position_list[i] != "K":
                    df2 = df2.droplevel(0, axis=1)
                    df2["Week"] = re.search(r"(?<=\-)\s*(..)", file)[0]
                    df2["Pos"] = [i.split()[-1] for i in df2["Player  Player on team"]]
                    df2.rename(
                        columns={"Player  Player on team": "Player"}, inplace=True
                    )
                    df2["Player"] = df2["Player"].map(
                        lambda x: x.split()[3] + " " + x.split()[4]
                    )
                else:
                    df2["Week"] = re.search(r"(?<=\-)\s*(..)", file)[0]
                    df2["Pos"] = [i.split()[-1] for i in df2["Player  Player on team"]]
                    df2.rename(
                        columns={"Player  Player on team": "Player"}, inplace=True
                    )
                    df2["Player"] = df2["Player"].map(
                        lambda x: x.split()[3] + " " + x.split()[4]
                    )
                df2["Week"] = df2["Week"].map(lambda x: x.rstrip("_"))
        dfs.append(df2)
    df = pd.concat(dfs, ignore_index=True)
    return df
