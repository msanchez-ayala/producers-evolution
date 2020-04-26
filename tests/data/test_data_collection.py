# import pytest
import re


class TestGetArtistId(object):

	def test_null_artist_input(self):
		# null artist
		# null sp
		# nonsense text (len(items) == 0?)
		# I guess need artist['name'] to be some sort of match with artist input
		# - This means need to test that it works with artists having &, and 
		# characters
		artist = 'Drake' # fill in with different 
		artist_id = 'spotify:artist:3TVXtAsR1Inumwj472S9r4' # get_artist_id(artist)

		# Confirm the returned URI corresponds to an artist
		pattern = 'spotify:artist:[\d\w]*'

		message = f'The artist id for {artist} ({artist_id}) does not \
			correspond to a Spotify artist'

		# want to assert that the result will match with the 
		assert re.match(artist_id, pattern).group(0), message
