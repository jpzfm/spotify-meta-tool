# Spotify Metadata Tool for Alfred
---
Python 3 script that pulls a song's metadata from Spotify using a track URI or URL as input and outputs a script filter-compatible JSON for [Alfred](https://www.alfredapp.com/). 



### Requirements
---
[Spotipy](https://github.com/plamere/spotipy)
```zsh
pip install spotipy
```


### JSON Template for Credentials File
---
Create a `creds.json` file in the working directory of the script with your Spotify credentials using this template:

```json
{
  "client_id": "YOUR_SPOTIFY_CLIENT_ID",
  "client_secret": "YOUR_SPOTIFY_CLIENT_SECRET"
}
```


### Alfred Script Filter
---
Example shell script for "script" section of Alfred script filter object:

```zsh
/usr/local/bin/python3 track_details.py $1
```


### Credits
---
All included icons by [Icons8](https://icons8.com).