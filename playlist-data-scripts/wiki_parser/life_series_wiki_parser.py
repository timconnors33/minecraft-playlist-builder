import requests
from bs4 import BeautifulSoup
import os
import json
import pandas as pd
import re
from urllib.parse import urlparse

MEMBERS_GALLERY_ID = 'gallery-0'

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

def parseWikiPages():
    members_gallery_items = parseMembersPage()
    member_wiki_links = []
    season_appearance_links = []
    for gallery_item in members_gallery_items:
        internal_link = parseMemberGalleryItem(gallery_item=gallery_item)
        if internal_link != '':
            member_wiki_links.append(internal_link)
    for member_wiki_link in member_wiki_links:
        season_appearance_links.extend(parseMemberPage(internal_link=member_wiki_link))
    return pd.DataFrame(season_appearance_links)
    
def parseMembersPage():
    soup = getSoup(filepath='./data/life-series/wiki-pages/members-wiki-page.json', uri="https://the-life-series.fandom.com/api.php?action=parse&page=Members&format=json")
    members_gallery = soup.find(id=MEMBERS_GALLERY_ID)
    gallery_items = members_gallery.findChildren('div', {'class': 'wikia-gallery-item'})
    return gallery_items

def parseMemberGalleryItem(gallery_item):
    internal_link = ''
    caption = gallery_item.findChild('div', {'class': 'lightbox-caption'})
    anchor = caption.find_next('a')
    if anchor.has_attr('href') and anchor['href'].startswith('/wiki/'):
        internal_link = anchor['href'].replace('/wiki/', '')
    return internal_link
    

def parseMemberPage(internal_link):
    season_appearances = []
    # TODO: Safe to use internal link as part of file path?
    soup = getSoup(filepath=f'./data/life-series/wiki-pages/{internal_link}.json', uri=f'https://the-life-series.fandom.com/api.php?action=parse&page={internal_link}&format=json')
    
    main_channel_header = soup.find('h3', string='Main Channel:')
    main_channel_div = main_channel_header.find_next_sibling('div')
    main_channel_anchor = main_channel_div.findChild('a', recursive=False)
    
    episodes_header = soup.find('h3', string="Episodes:")
    episodes_list = episodes_header.find_next('ul')
    # TODO: Is this necessary?
    episode_list_items = episodes_list.findChildren('li')
    for episode_list_item in episode_list_items:
        anchor = episode_list_item.findChild('a')
        # https://stackoverflow.com/questions/9889635/regular-expression-to-return-all-characters-between-two-special-characters
        season_text_pattern = re.compile(r'.*?\((.*)\).*')
        if anchor:
            parsed = urlparse(anchor['href'])
            if (parsed.scheme == 'http' or parsed.scheme == 'https') and (parsed.netloc == 'www.youtube.com' or parsed.netloc == 'youtube.com'):
                if parsed.path == '/playlist' or 'list=PL' in parsed.query:
                    link_type = 'playlist'
                    youtube_internal_link = getPlaylistId(youtube_internal_link=parsed.query)
            season_text = season_text_pattern.match(anchor.get_text()).group(1)
        else:
            parsed = urlparse(main_channel_anchor['href'])
            link_type = 'channel'
            youtube_internal_link = parsed.path
            if parsed.path.count('/') == 1:
                youtube_internal_link = parsed.path.split('/')[1]
            if parsed.path.count('/') >= 2:
                youtube_internal_link = parsed.path.split('/')[2]
            season_text = season_text_pattern.match(episode_list_item.get_text()).group(1)
            
        # TODO: Should add a test case for this behavior
        life_substr = season_text.find('Life')
        if life_substr is not -1:
            season_text = season_text.split(sep='Life')[0] + 'Life'
            
        season_appearance = SeasonAppearanceLinkAggregate(
            series_title='Life Series', 
            season_title=season_text,
            # TODO: Implement a way of determining whether a season is current or not. When viewing version history,
            # it looks like current seasons don't have most elements in an aside at the top of the page content,
            # but this should be investigated further.
            is_current_season=False,
            youtube_internal_link=youtube_internal_link, 
            link_type=link_type)
        season_appearances.append(season_appearance.__dict__)
            
    return season_appearances

        
def getPlaylistId(youtube_internal_link):
    # TODO: This looks silly, but I want to make sure not to extract another
    # ID type. Will a 'list=' substring only ever be followed by a playlist ID?
    processed_link = 'PL' + (youtube_internal_link.split('list=PL', 1)[1]).split('&', 1)[0]
    return processed_link