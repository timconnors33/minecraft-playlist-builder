import os
from dotenv import load_dotenv, find_dotenv
import json
import googleapiclient.discovery


load_dotenv(find_dotenv())

YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')
PLAYLIST_ITEMS_REQUEST_PART = 'snippet,contentDetails'
PLAYLIST_ITEMS_MAX_RESULTS = 50

youtube = googleapiclient.discovery.build(
        serviceName='youtube', version='v3', developerKey=YOUTUBE_API_KEY
)

class Series():
    def __init__(self, title):
        self.title = title

class Season():
    def __init__(self, title, series_title):
        self.title = title
        self.series_title = series_title

class Video():
     def __init__(self, video_id, channel_id, title, season_title, series_title, thumbnail_uri, published_at):
        self.video_id = video_id
        self.channel_id = channel_id
        self.title = title
        self.season_title = season_title
        self.series_title = series_title
        self.thumbnail_uri = thumbnail_uri
        self.published_at = published_at

class SeasonAppearance():
    def __init__(self, channel_id, season_title, series_title):
        self.channel_id = channel_id
        self.season_title = season_title
        self.series_title = series_title

class Channel():
    def __init__(self, id, name, thumbnail_uri):
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
    wiki_season_appearances = getWikiData()
    for wiki_season_appearances in wiki_season_appearances:
        youtube_link = wiki_season_appearances['youtube_internal_link']
        if youtube_link == 'playlist?list=PLSCZsQa9VSCc-7-qOc8O7t9ZraR4L5y0Y':
            youtube_link = youtube_link.replace('playlist?list=', '')
            season = Season(title=wiki_season_appearances['season'], series_title='Hermitcraft')
            videos, channels, season_appearances = processPlaylistVideos(playlist_id=youtube_link, season=season)
            #for video in videos:
             #   print(video.__dict__)
            for channel_id in channels:
                print(channels[channel_id].__dict__)
            for season_appearance in season_appearances:
                print(season_appearance.__dict__)

def processPlaylistVideos(playlist_id, season):
    videos = []
    channels = {}
    season_appearances = []
    request = youtube.playlistItems().list(
        part=PLAYLIST_ITEMS_REQUEST_PART,
        maxResults=PLAYLIST_ITEMS_MAX_RESULTS,
        playlistId=playlist_id
    )
    response = request.execute()
    videos.extend(processPlaylistPage(response=response, season=season))

    while 'nextPageToken' in response:
        request = youtube.playlistItems().list(
            part=PLAYLIST_ITEMS_REQUEST_PART,
            maxResults=PLAYLIST_ITEMS_MAX_RESULTS,
            playlistId=playlist_id,
            pageToken = response.get('nextPageToken')
        )
        response = request.execute()
        videos.extend(processPlaylistPage(response=response, season=season))

    # TODO: Should probably do this in the same pass as the videos as some point
    for video in videos:
        if video.channel_id not in channels:
            channel = getChannel(channel_id=video.channel_id)
            channels[video.channel_id] = channel
            season_appearances.append(SeasonAppearance
                                      (channel_id=video.channel_id, 
                                       season_title=season.title,
                                       series_title=season.series_title))
    return videos, channels, season_appearances


def processPlaylistPage(response, season):
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

def getChannel(channel_id):
    request = youtube.channels().list(
        part='snippet',
        maxResults=1,
        id=channel_id
    )
    response = request.execute()
    snippet = response.get('items')[0].get('snippet')

    thumbnail_uri = snippet.get('thumbnails').get('high').get('url')
    name = snippet.get('title')
    channel = Channel(id=channel_id, name=name, thumbnail_uri=thumbnail_uri)
    return channel

processWikiData()
