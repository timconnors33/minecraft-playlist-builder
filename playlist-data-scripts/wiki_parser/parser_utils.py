import requests
from bs4 import BeautifulSoup
import os
import json
from urllib.parse import urlparse

class SeasonLink():
    def __init__(self, internal_link, text, is_current_season):
        self.internal_link = internal_link
        self.text = text
        self.is_current_season = is_current_season

class SeasonAppearanceLink():
    def __init__(self, youtube_internal_link, link_type):
        self.youtube_internal_link = youtube_internal_link
        self.link_type = link_type

class SeasonAppearanceLinkAggregate():
    def __init__(self, series_title, season_title, is_current_season, youtube_internal_link, link_type):
        self.series_title = series_title
        self.season_title = season_title
        self.is_current_season = is_current_season
        self.youtube_internal_link = youtube_internal_link
        self.link_type = link_type
        
def getSoup(filepath, uri):
    if not os.path.exists(filepath):
        r = requests.get(uri)
        htmlData = r.json()['parse']['text']['*']
        with open(filepath, 'w') as f:
            json.dump(htmlData, f)
    else:
        with open(filepath, 'r') as f:
            htmlData = json.load(f)
    soup = BeautifulSoup(htmlData, 'html.parser')

    return soup

def parseYouTubeUri(uri):
    parsed = urlparse(uri)
    if (parsed.scheme == 'http' or parsed.scheme == 'https') and (parsed.netloc == 'www.youtube.com' or parsed.netloc == 'youtube.com'):
        if parsed.path == '/playlist' or 'list=PL' in parsed.query:
            link_type = 'playlist'
            youtube_internal_link = getPlaylistId(youtube_internal_link=parsed.query)
        else:
            link_type = 'channel'
            youtube_internal_link = parsed.path
            # Could maybe reformat this to not use any if statements and just get the string at parsed.path.count('/'),
            # however I think this relationship is coincidential rather than intrinsic.
            if parsed.path.count('/') == 1:
                youtube_internal_link = parsed.path.split('/')[1]
            if parsed.path.count('/') >= 2:
                youtube_internal_link = parsed.path.split('/')[2]
        season_appearance_link = SeasonAppearanceLink(youtube_internal_link=youtube_internal_link, link_type=link_type)
        return season_appearance_link
    # TODO: Check behavior if the top level if statement is false?
    return None

def getPlaylistId(youtube_internal_link):
    # TODO: This looks silly, but I want to make sure not to extract another
    # ID type. Will a 'list=' substring only ever be followed by a playlist ID?
    processed_link = 'PL' + (youtube_internal_link.split('list=PL', 1)[1]).split('&', 1)[0]
    return processed_link