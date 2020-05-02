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


def frame_table():
    """
    Helper for get_album_info()

    Returns
    -------
    A dict with keys as column headers and values as empty lists.
    """
    columns = ['No.', 'Title', 'Writer(s)', 'Producer(s)', 'Length']

    table = {column: [] for column in columns}

    return table, columns


def separate_names(value):
    """
    Helper for populate_table()

    Returns
    -------
    List with writer or procuder names separated and devoid of references e.g. [a]

    Parameters
    ----------
    value [bs4.element.Tag]: the tag containing the table's entry for writers or producers
    """
    if value.ul:
        # Isolate all li tags and extract text from those individually rather
        lis = value.ul.find_all('li')
#         print('lis', lis)
        result = [li.getText() for li in lis]
        return result
    else:
        return [value.getText()]


def populate_table(table, all_rows, col_titles):
    """
    Helper for get_album_info(). Populates the supplied empty table with the 
    rows from `all_rows` using col_titles.

    Parameters
    ----------
    table [dict]: dict containing column titles as keys. Each key has an 
    empty list as its value.

    all_rows [list]: All tags containing the data for each row of the table.

    col_titles [list]: All of the names of each column.
    """
    # Final row excluded from this count, which stores the total play time for the album
    num_rows = len(all_rows) - 1

    # Go through each row excluding the header row and final row. Header is 
    # accounted for by starting range at 1
    for row_num in range(1, num_rows):
        # print('row num', row_num)

        # For each row, iterate through each column and add the value table
        for i, value in enumerate(all_rows[row_num].find_all('td')):
            
            # print('i', i)
            # separate names in writers/producers columns
            if i in [2, 3]:
                table[col_titles[i]].append(separate_names(value))

            # For other columns just extract text
            else:
                table[col_titles[i]].append(value.getText())


def get_album_info(title, url, headers):
    """
    Returns
    -------
    A list of information for each track listed in the album

    Parameters
    ----------
    title [str]: the album name

    url [str]: the URL suffix of the album wikipedia page to pass to the requests.get() method for scraping

    headers [str]: the headers to pass to the requests.get() method for scraping
    """
    album_page = get_page('https://www.wikipedia.org' + url, headers)

    # find a tag that starts the section since the HTML is all flat
    table_tag = album_page.find('table', {'class': 'tracklist'})

    # Each row is nested within a top-level 'tr' tag
    all_rows = table_tag.find_all('tr')

    # # Isolate the header row (uses th tag, different from other rows)
    # headers_row = all_rows[0].find_all('th')

    # A dict to store data by column, column names
    table, col_titles = frame_table()

    table = populate_table(table, all_rows, col_titles)

    return pd.DataFrame(table).set_index('No.')