"""
This module calls the Spotify API through Python driver Spotipy and parses
results for information relevant to this study.
"""

import spotipy
import config


def get_auth():

	token = spotipy.util.prompt_for_user_token(
		username = config.username,
		client_id = config.client_id,
		client_secret = config.client_secret,
		redirect_uri = config.redirect_uri
	)


	if token:
		sp = spotipy.Spotify(auth=token)
		return sp

	else:
		print("Can't get token for", config.username)

def get_artist_id(artist, sp):
	"""
	Returns
	-------
	A Spotify artist ID

	Parameters
	----------
	artist [str]: The artist name 

	sp [spotipy.Spotify obj]: The currently active Spotify client object.
	"""
	results = sp.search(q='artist:' + artist, type = 'artist')
	items = results['artists']['items']
	if len(items):
		artist = items[0]
		print(artist)



if __name__ == '__main__':
	# get_auth()
	sp = spotipy.Spotify(auth = config.token)
