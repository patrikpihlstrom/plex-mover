## plex-mover
[![Build Status](https://travis-ci.org/patrikpihlstrom/plex-mover.svg?branch=daemon)](https://travis-ci.org/patrikpihlstrom/plex-mover)

# Features

Scans your transmission directory for content & automagically moves said content its correct plex directory.
It takes the title, season and episode into account when moving content.

# Installation

Clone the repository using the --recursive option:
```
$ git clone --recursive git@github.com:patrikpihlstrom/plex-mover.git
```

Install it:
```
$ cd plex-mover/ && pip install .
```

# Usage

```
$ python plex_mover.py
[0] - Its.Always.Sunny.In.Philadelphia.S05E02.BDRip
[1] - Some_Movie.1990.1080p
[2] - another show - s02e10
[3] - some show s01e01x256
################
select an item : 
```

You can enter a number, or '\*' in order to move all items.

If I were to select 0, Its.Always.Sunny.In.Philadelphia.S05E02.BDRip would be moved to:
```
/your/tv/lib/Its\ Always\ Sunny\ in\ Philadelphia/Season\ 5/Its.Always.Sunny.In.Philadelphia.S05E02.BDRip
```

From there, plex can parse the file/directory name and add it to your library.
