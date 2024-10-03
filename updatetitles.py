import os
from pathlib import Path
from plexapi.server import PlexServer
import lxml.etree as ET

baseurl = ''
token = ''

plex = PlexServer(baseurl, token)

section = plex.library.section('YouTube Channels')

for ep in section.search(title='Episode ', libtype='episode'):
    for part in ep.iterParts():
        nfo_data_file_path = part.file.replace(".mkv", ".nfo")
            
        if os.path.exists(nfo_data_file_path):
            print('[-] Trying to parse NFO file')
            parser = ET.XMLParser(recover=True)
            tree = ET.parse(nfo_data_file_path, parser=parser)
            root = tree.getroot()
            title = root.find('title').text
            aired = root.find('aired').text
            print ('[-] Trying to update title to be: ' + title + ' - Aired: ' + aired)
            ep.editTitle(title, locked=True)
            ep.editSortTitle(aired, locked=True)

