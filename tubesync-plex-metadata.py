import os
import configparser
import argparse
import glob
import re
from pathlib import Path
from plexapi.server import PlexServer
import lxml.etree as ET

def main(config_path, silent, syncAll, subtitles):

    config = configparser.ConfigParser()
    config.read(config_path)

    plex_base_url = config['DEFAULT']['plex_base_url']
    plex_token = config['DEFAULT']['plex_token']
    plex_library_name = config['DEFAULT']['plex_library_name']

    plex = PlexServer(plex_base_url, plex_token)

    section = plex.library.section(plex_library_name)

    # Default title that Plex detect when adding TubeSync videos
    title_filter = 'Episode '
    if syncAll:
        title_filter = ''

    for ep in section.search(title=title_filter, libtype='episode'):
        for part in ep.iterParts():
            nfo_data_file_path = part.file.replace(".mkv", ".nfo")
                
            if os.path.exists(nfo_data_file_path):
                print('[-] Trying to parse NFO file') if not silent else None
                try:
                    parser = ET.XMLParser(recover=True)
                    tree = ET.parse(nfo_data_file_path, parser=parser)
                except IOError as e:
                    print(f"IOError: Could not open file. Details: {e}")
                    continue
                except ET.XMLSyntaxError as e:
                    print(f"XMLSyntaxError: Malformed XML. Details: {e}")
                    continue
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")
                    continue
                root = tree.getroot()
                if root is None:
                    continue
                title = aired = plot = ''
                if root.find('title') is not None:
                    title = root.find('title').text
                if root.find('aired') is not None:
                    aired = root.find('aired').text
                if root.find('plot') is not None:
                    plot = root.find('plot').text
                print ('[-] Trying to update title to be: ' + title + ' - Aired: ' + aired) if not silent else None
                ep.editTitle(title, locked=True)
                ep.editSortTitle(aired, locked=True)
                ep.editSummary(plot, locked=True)
                if subtitles:
                    subtitle_file_path = part.file.replace(".mkv", "")
                    part_path = os.path.dirname(part.file)
                    file_name = os.path.basename(part.file).replace(".mkv", "")
                    for root, dirs, files in os.walk(part_path):
                        for file in files:
                            if file.startswith(file_name) and file.endswith(".vtt"):
                                print ('[-] Found subtitle file: ' + file)
                                ep.uploadSubtitles(part_path + '/' + file)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='TubeSync Plex Media Metadata sync tool')
    parser.add_argument('-c', '--config', type=str, default='./config.ini', help='Path to the config file')
    parser.add_argument('-s', '--silent', action='store_true', help='Run in silent mode')
    parser.add_argument('--all', action='store_true', help='Update everything in the library')
    parser.add_argument('--subtitles', action='store_true', help='Find subtitles for the video and upload them to plex')
    args = parser.parse_args()
    main(args.config, args.silent, args.all, args.subtitles)



