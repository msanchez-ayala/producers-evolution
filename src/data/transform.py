"""
This module transforms data extracted from Wikipedia (and maybe also Spotify
depending on how much trnasformations need to be done).

Author: M. Sanchez-Ayala (04/29/20)
"""

import re


def filter_references(names):
    """
    Returns
    --------
    A list of names that have been stripped of wikipedia references
    e.g. [a] or [b]
    
    Parameters
    -----------
    names [list]: a list of names that may or may not be appended with 
    contain wikipedia references
    """
    # Captures any reference
    pattern = '(\[[a-z]\])'
    
    result = []
    
    for name in names:
        
        # If there's a reference, return a truncated string
        if re.search(pattern, name):
            result.append(name[:-3])

        # Otherwise just return the name
        else:
            result.append(name)
    
    return result


def transform_producers_col(df):
    """
    Returns
    -------
    Copy of given df with Producer(s) column filtered of references.

    Parameters
    ----------
    df [pandas df]: a df of raw data from Wikipedia scrape.
    """
    df = df.copy()
    print(df.columns)
    df['Producer(s)'] = df['Producer(s)'].map(
        lambda names: filter_references(names)
    )

    return df
