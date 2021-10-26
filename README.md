# MovieTheater
![python3_support](https://img.shields.io/badge/Python-3-blue.svg "Python 3")

A simple and lightweight interface for movies stored locally or on network share(s).

---
![alt text](https://i.imgur.com/3nmawYo.gif)

## Features:
* Automatically parse torrent file names like `The.Best.Movie.Ever.2021.2160p.UHD.n0t0rr3nt-[nogrp]`
* Automatically obtains information about the media and stores it inside database
* Automatically removes deleted media from database to ensure an updated webpage

## Requirements:
* Free API key from (https://www.omdbapi.com) to obtain information about the media
* VLC Media Player (https://www.videolan.org/vlc) which is being used in the background for playing media
* MediaPlayer (https://github.com/rootm0s/MediaPlayer) for playing media in fullscreen with a press of a button from the webpage

## Installation:
```python
pip install requirements.txt
```
## Configuration:
```ini
# API key goes here
[API]
omdbapi = 

# Example paths:
#   path = F:\Movies, \\server01\share01\movies
[DIRECTORY]
path = 

# Leave it blank to save database in current folder or
# set full path to directory where to save it.
[DATABASE]
path = 

# Leave it blank to save webpage in current folder or
# set full path to directory where to save it.
[WEBPAGE]
path = 

# How often to check for changes regarding newly added movies or removals.
[INTERVAL]
time = 120
```

## Build:
Execute the `build.bat` file to build a single executable. The executable will be located in the dist folder and the batch file will delete all the temp files used while building.

## Credits:
* Depends on this project (https://www.omdbapi.com) for the media information
* Depends on this project (https://github.com/platelminto/parse-torrent-title) for the torrent name parsing
