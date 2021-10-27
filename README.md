# MovieTheater
![python3_support](https://img.shields.io/badge/Python-3-blue.svg "Python 3")

A simple and lightweight interface for movies stored locally or on network share(s).

---
![alt text](https://i.imgur.com/3nmawYo.gif)

## Features:
- [x] Play movies directly from the webpage
- [x] Search for movies using either name, year, genre, plot, actors or resolution.
- [x] Automatically parse torrent file names like `The.Best.Movie.Ever.2021.2160p.UHD.n0t0rr3nt-[nogrp]`
- [x] Automatically obtains information about the movie and stores it inside database _(plot, poster, imdb score, actors, genre, runtime and trailer)_
- [x] Automatically removes deleted movies from database to ensure an updated webpage

## Requirements:
* Free API key from (https://www.omdbapi.com) to obtain information about the media
* MediaPlayer (https://github.com/movietheater/mediaplayer) for playing media in fullscreen with a press of a button from the webpage.

## Installation:
```python
pip install requirements.txt
```
## Configuration:
This is a example of a basic configuration file, change to your settings before running.
```ini
# API key goes here
[API]
omdbapi = 0x3x4mpl3k3y

# Example paths:
#   path = F:\Movies, \\server01\share01\movies
[DIRECTORY]
path = F:\Movies

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

## Build (optional):
Execute the `build.py` file to build a single executable. The executable will be located in the **dist** folder.

## Running:
Make sure the [requirements](#requirements) are met and [configuration file](#configuration) is updated with correct information and have followed the [installation step](#installation). You should now be ready to run `movietheater.py` or the executable `movietheater.exe` created from running `build.py`

## Credits:
* Depends on this project (https://www.omdbapi.com) for the media information
* Depends on this project (https://github.com/platelminto/parse-torrent-title) for the torrent name parsing
