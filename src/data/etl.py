"""
This module executes etl from functions in relevant modules.

Author: M. Sanchez-Ayala (04/29/20)
"""

import pandas as pd
from extract_wikipedia import *
# from extract_spotify import *
from transform import *


def main():
    """
    Currently returns a dict of all album information of an artist's albums 
    that are listed on their Wikipedia page in separate dataframes.
    """
    # Set up
    headers = {'user-agent': 'Safari/13.0.2 (Macintosh; Intel Mac OS X 10_15)'}
    url = 'https://en.wikipedia.org/wiki/Drake_(musician)#Discography'

    # Get album names and urls
    albums = get_albums(url, headers)

    # Empty container to store dict of dataframes
    album_dfs = {}

    # Scrape each album's wikipedia page for album metadata
    for title, url in albums.items():
        df = get_album_info(title, url, headers)
        df = transform_producers_col(df)
        album_dfs[title] = df

    return album_dfs


if __name__ == '__main__':
    main()