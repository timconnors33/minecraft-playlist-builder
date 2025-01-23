import os
from dotenv import load_dotenv, find_dotenv
import json


load_dotenv(find_dotenv())

YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')

class Series():
    def __init__(self, title):
        self.title = title

class Season():
    def __init__(self, title, series_title):
        self.title = title
        self.series_title = series_title

class Video():
     def __init__(self, channel_id, channel_name, title, season_title, series_title, thumbnail_uri):
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.title = title,
        self.season_title = season_title
        self.series_title = series_title
        self.thumbnail_uri = thumbnail_uri

class SeasonAppearance():
    def __init__(self, channel_id, season_title):
        self.channel_id = channel_id
        self.season = season_title

def getWikiData():
    season_appearances = []
    filepath = './data/hermitcraft/season-appearances.json'

    if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                season_appearances = json.load(f)

    return season_appearances

def processWikiData():
    season_appearances = getWikiData()
    for season_appearance in season_appearances:
        youtube_link = season_appearance['youtube_internal_link']
        '''if youtube_link == 'playlist?list=PLSCZsQa9VSCc-7-qOc8O7t9ZraR4L5y0Y':'''

processWikiData()
