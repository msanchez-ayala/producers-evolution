"""
This module calls the Spotify API through Python driver Spotipy and parses
results for information relevant to this study.
"""
import spotipy
from config import *
from consts import *


def get_auth():
	"""
	Attempts to get a Spotify API authentication token.

	Returns
	-------
	A spotify.Spotify client object if a token is retrieved. Else, gives a
	failure message.
	"""
	token = spotipy.util.prompt_for_user_token(
		username = username,
		client_id = client_id,
		client_secret = client_secret,
		redirect_uri = redirect_uri
	)

	if token:
		sp = spotipy.Spotify(auth=token)
		return sp

	else:
		print("Can't get token for", username)

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
		return artist['uri']

def get_artist_albums(artist_id, sp):
	"""
	"""
	# Can change any of these params
	print(
		sp.artist_albums(
			artist_id, album_type='album', country=None, limit=50, offset=0
		)
	)


def get_table(json):
	"""
	Helper for get_artist_albums. Parses the JSON received from the
	artist_albums API call.
	"""
	table = {
		'artist_name': [],
		'album_name': [],
		'album_id': [],
		'release_date': [],
		'total_tracks': []    
	}

	for item in json['items']:
		table['artist_name'].append(item['artists'][0]['name'])
		table['album_name'].append(item['name'])
		table['album_id'].append(item['uri'])
		table['release_date'].append(item['release_date'])
		table['total_tracks'].append(item['total_tracks'])



if __name__ == '__main__':

	sp = get_auth()
	artist_id = get_artist_id(artist, sp)
	get_artist_albums(artist_id, sp)

