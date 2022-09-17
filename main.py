#!/usr/bin/env python3

from scrape_player_info import scrape_player_info
from scrape_statistics import *
from data_cleaning import *


def main():
    # impute_special_char(scrape_statistics(), "_")
    # change_col_types
    print(scrape_statistics())
    print(scrape_player_info())


if __name__ == "__main__":
    main()
