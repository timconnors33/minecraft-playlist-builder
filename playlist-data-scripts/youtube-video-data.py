import os
from dotenv import load_dotenv, find_dotenv
import json
import googleapiclient.discovery
import pyodbc


load_dotenv(find_dotenv())

YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')
PLAYLIST_ITEMS_REQUEST_PART = 'snippet,contentDetails,status'
PLAYLIST_ITEMS_MAX_RESULTS = 50

youtube = googleapiclient.discovery.build(
        serviceName='youtube', version='v3', developerKey=YOUTUBE_API_KEY
)

class Series():
    def __init__(self, title):
        self.title = title

class Season():
    def __init__(self, title, series_title, is_current_season):
        self.title = title
        self.series_title = series_title
        self.is_current_season = is_current_season

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
    filepath = './data/hermitcraft/season-appearances.json'

    if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                series = json.load(f)

    return series

def processWikiData():
    series_list = getWikiData()
    for series in series_list:
        series_title = series['title']
        series_id = addSeriesToDb(series_title=series_title)
        for season in series['seasons']:
            cur_season = Season(title=season['title'], series_title=series_title, is_current_season=season['is_current_season'])
            addSeasonToDb(season=cur_season, series_id=series_id)
            for wiki_season_appearance in season['season_appearances']:
                    youtube_link = wiki_season_appearance['youtube_internal_link']
                    '''
                    if youtube_link == 'playlist?list=PLSCZsQa9VSCc-7-qOc8O7t9ZraR4L5y0Y':
                        youtube_link = youtube_link.replace('playlist?list=', '')
                        videos, channels, season_appearances = processPlaylistVideos(playlist_id=youtube_link, season=cur_season)
                        #for video in videos:
                        #   print(video.__dict__)
                        for channel_id in channels:
                            print(channels[channel_id].__dict__)
                        for season_appearance in season_appearances:
                            print(season_appearance.__dict__)
                    '''

def queryDbInsert(sql_query, params):
    conn = pyodbc.connect(os.environ.get('ODBC_DB_CONNECTION_STRING'))
    cursor = conn.cursor()

    cursor.execute(sql_query, params)
    conn.commit()

    cursor.close()
    conn.close()

def addSeriesToDb(series_title):
    # https://stackoverflow.com/questions/20971680/sql-server-insert-if-not-exists
    sql_query = '''
        INSERT INTO [dbo].[Series] (SeriesTitle)
        SELECT ?
        WHERE NOT EXISTS 
            (SELECT 1 
            FROM [dbo].[Series] 
            WHERE SeriesTitle = ?)
    '''
    queryDbInsert(sql_query=sql_query, params=(series_title, series_title))

    conn = pyodbc.connect(os.environ.get('ODBC_DB_CONNECTION_STRING'))
    cursor = conn.cursor()

    sql_query = '''
        SELECT SeriesId FROM [dbo].[Series]
        WHERE SeriesTitle = ?
    '''
    params = series_title

    series_id = cursor.execute(sql_query, params).fetchone().SeriesId
    conn.commit()

    cursor.close()
    conn.close()

    return series_id

def addSeasonToDb(season, series_id):
    sql_query = '''
        INSERT INTO [dbo].[Seasons] (SeriesId, SeasonTitle, IsCurrentSeason)
        SELECT ?, ?, ?
        WHERE NOT EXISTS 
            (SELECT 1 
            FROM [dbo].[Seasons] 
            WHERE SeriesId = ?
            AND SeasonTitle = ?)
    '''
    params = (series_id, season.title, season.is_current_season, series_id, season.title)
    queryDbInsert(sql_query=sql_query, params=params)
    

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
        Ensures only public videos are processed
        '''
        if 'videoId' in playlist_item.get('contentDetails') and playlist_item.get('status').get('privacyStatus') == 'public':
            video_id = playlist_item.get('contentDetails').get('videoId')
            video_published_at = playlist_item.get('contentDetails').get('videoPublishedAt')
            channel_id = playlist_item.get('snippet').get('videoOwnerChannelId')
            video_title = playlist_item.get('snippet').get('title')
            video_thumbnail_uri = playlist_item.get('snippet').get('thumbnails').get('high').get('url')
            video = Video(
                video_id=video_id,
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
