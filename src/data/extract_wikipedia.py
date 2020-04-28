"""
This module will scrape Wikipedia using Beautiful Soup given a musical artist's
URL. Currently, it's tailored to work for just Drake. It does not parse or
clean the information in any way.

Author: M. Sanchez-Ayala (04/27/20)
"""

import pandas as pd
from bs4 import BeautifulSoup as BS
import requests


def get_page(url, headers):
    """
    Returns
    -------

    A list of 50 IMDB html tags representing each one movie block from the specified url.

    Parameters
    -----------
    url: [str] url to search on.

    headers: [str] headers to pass into requests.get so that the website knows we are not russian hackers.
    """
    try:
        page = requests.get(url,headers=headers, timeout = 5)
        if page.status_code != 200:
            print(page.status_code)

    except requests.ConnectionError as e:
        print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
        print(str(e))
    except requests.Timeout as e:
        print("OOPS!! Timeout Error")
        print(str(e))
    except requests.RequestException as e:
        print("OOPS!! General Error")
        print(str(e))
    except KeyboardInterrupt:
        print("Someone closed the program")

    soup = BS(page.content, 'html.parser')

    return  soup


def get_albums(url, headers):
    """
    Returns
    --------
    A dict with the album names and wikipedia album URLs
    
    Parameters
    ---------
    url [str]: the full URL of the artist wikipedia page to pass to the requests.get() method for scraping
    
    headers [str]: the headers to pass to the requests.get() method for scraping
    """
    # Scrape the consumption page
    artist_page = get_page(url, headers)
    
    # find a tag that starts the section since the HTML is all flat
    start = artist_page.find('span', {'class': 'mw-headline'}, text = 'Discography').parent
    
    # Isolate tags
    album_tags_parent = start.find_next_sibling('ul')
    album_tags = album_tags_parent.find_all('li')

    # Populate a dict with album titles and URL suffixes
    albums = {}
    for tag in album_tags:
        albums[tag.i.a.getText()] = tag.i.a['href']   
    
    return albums


def get_album_info(title, url, headers):
    """
    Returns
    -------
    A list of information for each track listed in the album
    
    Parameters
    ---------
    title [str]: the album name
    
    url [str]: the URL suffix of the album wikipedia page to pass to the requests.get() method for scraping
    
    headers [str]: the headers to pass to the requests.get() method for scraping
    """
    album_page = get_page('https://www.wikipedia.org' + url, headers)

    # find a tag that starts the section since the HTML is all flat
    table_tag = album_page.find('table', {'class': 'tracklist'})

    # Each row is nested within a top-level 'tr' tag
    all_rows = table_tag.find_all('tr')

    # Isolate the header row (uses th tag, different from other rows)
    headers_row = all_rows[0].find_all('th')

    # A container to store by column
    table = {value.getText(): [] for value in headers_row}

    # All column titles just to iterate through table keys later
    col_titles = list(table.keys())

    # We exlude the final row from this count, which stores the total play time for the album
    num_rows = len(all_rows) - 1

    # Go through each row excluding the header row and final row. Header is accounted for
    # by starting range at 1
    for row_num in range(1, num_rows):
        
        # For each row, we iterate through each value and add the value to table
        for i, value in enumerate(all_rows[row_num].find_all('td')):
            table[col_titles[i]].append(value.getText())
    
    return pd.DataFrame(table).set_index('No.')


if __name__ == '__main__':
    
    # Set up 
    headers = {'user-agent': 'Safari/13.0.2 (Macintosh; Intel Mac OS X 10_15)'}
    url = 'https://en.wikipedia.org/wiki/Drake_(musician)#Discography'
    
    # Get album names and urls
    albums = get_albums(url, headers)
    
    # Empty container to store dict of dataframes
    album_dfs = {}
    
    # Scrape each album's wikipedia page for album metadata
    for title, url in albums.items():
        album_dfs[title] = get_album_info(title, url, headers)