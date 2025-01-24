import os
from dotenv import load_dotenv, find_dotenv
import json
import googleapiclient.discovery


load_dotenv(find_dotenv())

YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')
REQUEST_PART = 'snippet,contentDetails'
MAX_RESULTS = 50

class Series():
    def __init__(self, title):
        self.title = title

class Season():
    def __init__(self, title, series_title):
        self.title = title
        self.series_title = series_title

class Video():
     def __init__(self, channel_id, title, season_title, series_title, thumbnail_uri, published_at):
        self.channel_id = channel_id
        self.title = title
        self.season_title = season_title
        self.series_title = series_title
        self.thumbnail_uri = thumbnail_uri
        self.published_at = published_at

class SeasonAppearance():
    def __init__(self, channel_id, season_title, video_count):
        self.channel_id = channel_id
        self.season = season_title
        self.video_count = video_count

class Channel():
    def __init__(self, id, name, thumbnail_uri=None):
        self.id = id
        self.name = name
        self.thumbnail_uri = thumbnail_uri

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
            season = Season(title=season_appearance['season'], series_title='Hermitcraft')
            processPlaylistVideos(playlist_id=youtube_link, season=season)

def processPlaylistVideos(playlist_id, season):
    videos = []
    youtube = googleapiclient.discovery.build(
        serviceName='youtube', version='v3', developerKey=YOUTUBE_API_KEY
    )
    request = youtube.playlistItems().list(
        part=REQUEST_PART,
        maxResults=MAX_RESULTS,
        playlistId=playlist_id
    )
    response = request.execute()
    videos.extend(processPlaylistPageVideos(response=response, season=season))

    while 'nextPageToken' in response:
        request = youtube.playlistItems().list(
            part=REQUEST_PART,
            maxResults=MAX_RESULTS,
            playlistId=playlist_id,
            pageToken = response.get('nextPageToken')
        )
        response = request.execute()
        videos.extend(processPlaylistPageVideos(response=response, season=season))
    
    for video in videos:
        print(json.dumps(video.__dict__))

def processPlaylistPageVideos(response, season):
    videos = []
    series_title = season.series_title
    season_title = season.title
    for playlist_item in response.get('items'):
        '''
        Ensures only videos are processed and privated videos are filtered out
        '''
        if 'videoId' in playlist_item.get('contentDetails') and 'videoOwnerChannelId' in playlist_item.get('snippet'):
            video_published_at = playlist_item.get('contentDetails').get('videoPublishedAt')
            channel_id = playlist_item.get('snippet').get('videoOwnerChannelId')
            video_title = playlist_item.get('snippet').get('title')
            video_thumbnail_uri = playlist_item.get('snippet').get('thumbnails').get('high').get('url')
            video = Video(
                channel_id=channel_id, 
                title=video_title, 
                season_title=season_title,
                series_title=series_title,
                thumbnail_uri=video_thumbnail_uri,
                published_at=video_published_at)
            videos.append(video)
    return videos

processWikiData()
