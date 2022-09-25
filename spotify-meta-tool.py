import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
from os import path


# Define current working directory and call creds file.

cwd = path.dirname(__file__)

creds_file = path.join(cwd, 'creds.json')
creds = json.load(open(creds_file))


# Define icon file paths.

artist_icon = path.join(cwd, 'icons/artist.png')
track_icon = path.join(cwd, 'icons/track.png')
isrc_icon = path.join(cwd, 'icons/isrc.png')
release_date_icon = path.join(cwd, 'icons/release_date.png')
copyrights_icon = path.join(cwd, 'icons/copyright.png')
pubrights_icon = path.join(cwd, 'icons/pubrights.png')
explicit_icon = path.join(cwd, 'icons/explicit.png')
clean_icon = path.join(cwd, 'icons/clean.png')


# Spotify API authorization.

client_credentials_manager = SpotifyClientCredentials(client_id=creds['client_id'], client_secret=creds['client_secret'])
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


# Take input from Alfred. Input should be Spotify URL or URI.

inp = sys.argv[1]


# API Calls and get track's album ID.

meta_pull_track = sp.track(inp)

album_id = meta_pull_track['album']['id']

meta_pull_album = sp.album(album_id)


# Pull explicit status of track and assign easy-to-read string.

explicit_value = meta_pull_track['explicit']

if explicit_value is False:
	explicit = "Clean"
elif explicit_value is True:
	explicit = "Explicit"
else:
	explicit = "No explicit/clean metadata."


# Pull PnC line from tracks album and add to its own dictionary.

pnc_pull = meta_pull_album['copyrights']

pnc = {}

for rights in pnc_pull:
	for key, value in rights.items():
		if key == 'text':
			pnc_text = value
		elif key == 'type':
			pnc_type = value
	pnc[pnc_type] = pnc_text


# Form dictionary with API output.

meta_list = {
	"Artist": meta_pull_track['artists'][0]['name'],
	"Track": meta_pull_track['name'],
	"ISRC": meta_pull_track['external_ids']['isrc'],
	"Release Date": meta_pull_track['album']['release_date'],
	"Copyright": pnc['C'],
	"Pub Rights": pnc['P'],
	"Explicit or Clean": explicit
}


# Create Alfred-readable JSON.

result = {"items": []}


# Asign an icon to each item and build add each to the Alfred-readable JSON.

for key, value in meta_list.items():

	if key == 'Artist':
		path = artist_icon
	elif key == 'Track':
		path = track_icon
	elif key == 'ISRC':
		path = isrc_icon
	elif key == 'Release Date':
		path = release_date_icon
	elif key == 'Copyright':
		path = copyrights_icon
	elif key == 'Pub Rights':
		path = pubrights_icon
	elif value == 'Explicit':
		path = explicit_icon
	elif value == 'Clean':
		path = clean_icon
	elif value == 'No explicit/clean metadata.':
		path = explicit_icon

	result["items"].append({
		"title": value,
		"subtitle": key,
		"arg": value,
		"icon": {
			"path": path
		}
	})


# Output pretty-print JSON for Alfred.

print(json.dumps(result, indent=4))
