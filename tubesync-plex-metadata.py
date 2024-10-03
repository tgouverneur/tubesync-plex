import os
import configparser
import argparse
from pathlib import Path
from plexapi.server import PlexServer
import lxml.etree as ET

def main(config_path, silent, syncAll):

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
                parser = ET.XMLParser(recover=True)
                tree = ET.parse(nfo_data_file_path, parser=parser)
                root = tree.getroot()
                title = root.find('title').text
                aired = root.find('aired').text
                print ('[-] Trying to update title to be: ' + title + ' - Aired: ' + aired) if not silent else None
                ep.editTitle(title, locked=True)
                ep.editSortTitle(aired, locked=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='TubeSync Plex Media Metadata sync tool')
    parser.add_argument('-c', '--config', type=str, default='./config.ini', help='Path to the config file')
    parser.add_argument('-s', '--silent', action='store_true', help='Run in silent mode')
    parser.add_argument('--all', action='store_true', help='Update everything in the library')
    args = parser.parse_args()
    main(args.config, args.silent, args.all)



