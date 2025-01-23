import os
from dotenv import load_dotenv, find_dotenv
import json
import googleapiclient.discovery


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
     def __init__(self, channel_id, title, season_title, series_title, thumbnail_uri):
        self.channel_id = channel_id
        self.title = title,
        self.season_title = season_title
        self.series_title = series_title
        self.thumbnail_uri = thumbnail_uri

class SeasonAppearance():
    def __init__(self, channel_id, season_title, video_count):
        self.channel_id = channel_id
        self.season = season_title
        self.video_count = video_count

class Channel():
    def __init__(self, id, name, thumbnail):
        self.id = id
        self.name = name
        self.thumbnail = thumbnail

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
        if youtube_link == 'playlist?list=PLSCZsQa9VSCc-7-qOc8O7t9ZraR4L5y0Y':
            youtube_link = youtube_link.replace('playlist?list=', '')
            processPlaylistVideos(youtube_link)

def processPlaylistVideos(playlist_id):
    youtube = googleapiclient.discovery.build(
        serviceName='youtube', version='v3', developerKey=YOUTUBE_API_KEY
    )
    request = youtube.playlistItems().list(
        part='snippet',
        maxResults=50,
        playlistId=playlist_id
    )
    response = request.execute()
    print(response)

processWikiData()
