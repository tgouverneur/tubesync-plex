# tubesync-plex

After using TubeSync for a little while, I was frustrated that the title of my youtube videos were not synced from either the NFO or the MKV's metadata in Plex.

I've found a little snippet of code from @RtypeStudios that was updating those title through the PlexAPI.
I found the solution to be very simple and decided to build on it, here is this script.

## Prerequisites

Either run this on your plex server directly or on a VM that has the same path for the media as on the plex server.
Ensure TubeSync is writting your thumbnails and NFOs.

## Usage

```
$ python3 -m venv venv
$ pip3 install -r requirements.txt 
$ cp config.ini-example config.ini
$ vi config.ini
# Tune the variable to suit your plex install
$ python3 tubesync-plex-metadata.py --help
usage: tubesync-plex-metadata.py [-h] [-c CONFIG] [-s] [--all]

TubeSync Plex Media Metadata sync tool

options:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Path to the config file
  -s, --silent          Run in silent mode
  --subtitles           Find subtitles for the video and upload them to plex
  --all                 Update everything in the library

$ python3 tubesync-plex-metadata.py --all
```

## Caveats

The `--subtitles` option seems to not work on my systems for some reason it returns 400. If anyone get it to work, I'm interested to know...
