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
icons = {
    'Artist': path.join(cwd, 'icons/artist.png'),
    'Track': path.join(cwd, 'icons/track.png'),
    'ISRC': path.join(cwd, 'icons/isrc.png'),
    'Release Date': path.join(cwd, 'icons/release_date.png'),
    'Copyright': path.join(cwd, 'icons/copyright.png'),
    'Pub Rights': path.join(cwd, 'icons/pubrights.png'),
    'Explicit': path.join(cwd, 'icons/explicit.png'),
    'Clean': path.join(cwd, 'icons/clean.png')
}


# Spotify API authorization.
client_credentials_manager = SpotifyClientCredentials(client_id=creds['client_id'], client_secret=creds['client_secret'])
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


# Take input from Alfred. Input should be Spotify URL or URI.
inp = sys.argv[1]


# API Calls and get track's album ID.
meta_pull_track = sp.track(inp)
album_id = meta_pull_track['album']['id']
meta_pull_album = sp.album(album_id)


# Pull explicit status of track.
explicit_value = meta_pull_track['explicit']
explicit = 'Explicit' if explicit_value else 'Clean' if explicit_value is False else 'No explicit/clean metadata.'


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
    'Artist': meta_pull_track['artists'][0]['name'],
    'Track': meta_pull_track['name'],
    'ISRC': meta_pull_track['external_ids']['isrc'],
    'Release Date': meta_pull_track['album']['release_date'],
    'Copyright': pnc['C'],
    'Pub Rights': pnc['P'],
    'Explicit or Clean': explicit
}


# Create Alfred-readable JSON.
result = {
    'items': [
        {
            'title': value,
            'subtitle': key,
            'arg': value,
            'icon': {
                'path': icons[key] if key in icons else icons[explicit]
            }
        } for key, value in meta_list.items()
    ]
}


# Output a pretty-printed JSON for Alfred.
print(json.dumps(result, indent=4))
