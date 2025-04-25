import requests
from bs4 import BeautifulSoup
import os
import json
from urllib.parse import urlparse
import re

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
    for gallery_item in members_gallery_items:
        internal_link = parseMemberGalleryItem(gallery_item=gallery_item)
        if internal_link != '':
            member_wiki_links.append(internal_link)
    for member_wiki_link in member_wiki_links:
        print(member_wiki_link)
        if member_wiki_link == "BdoubleO100":
            parseMemberPage(internal_link=member_wiki_link)
    
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
    # TODO: Safe to use internal link as part of file path?
    soup = getSoup(filepath=f'./data/life-series/wiki-pages/{internal_link}.json', uri=f'https://the-life-series.fandom.com/api.php?action=parse&page={internal_link}&format=json')
    episodes_header = soup.find('h3', text="Episodes:")
    episodes_list = episodes_header.find_next('ul')
    # TODO: Is this necessary?
    episode_list_items = episodes_list.findChildren('li')
    for episode_list_item in episode_list_items:
        anchor = episode_list_item.find_next('a')
        print(anchor['href'])
        print(anchor.get_text())
        
parseWikiPages()