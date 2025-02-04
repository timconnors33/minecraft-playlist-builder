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
    def __init__(self, title, series_internal_id, is_current_season):
        self.title = title
        self.series_internal_id = series_internal_id
        self.is_current_season = is_current_season

class Video():
     def __init__(self, youtube_id, title, thumbnail_uri, published_at, season_appearance_internal_id):
        self.youtube_id = youtube_id
        self.title = title
        self.thumbnail_uri = thumbnail_uri
        self.published_at = published_at
        self.season_appearance_internal_id = season_appearance_internal_id

class SeasonAppearance():
    def __init__(self, channel_internal_id, season_internal_id):
        self.channel_internal_id = channel_internal_id
        self.season_internal_id = season_internal_id

class Channel():
    def __init__(self, youtube_id, name, thumbnail_uri):
        self.youtube_id = youtube_id
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
        series_internal_id = addSeriesToDb(series_title=series_title)
        for season in series['seasons']:
            cur_season = Season(title=season['title'], series_internal_id=series_internal_id, is_current_season=season['is_current_season'])
            cur_season_internal_id = addSeasonToDb(season=cur_season)
            for wiki_season_appearance in season['season_appearances']:
                    youtube_link = wiki_season_appearance['youtube_internal_link']
                    if youtube_link == 'playlist?list=PLSCZsQa9VSCc-7-qOc8O7t9ZraR4L5y0Y':
                        youtube_link = youtube_link.replace('playlist?list=', '')
                        processPlaylistVideos(playlist_id=youtube_link, season_internal_id=cur_season_internal_id)

def queryDbInsert(sql_query, params):
    conn = pyodbc.connect(os.environ.get('ODBC_DB_CONNECTION_STRING'))
    cursor = conn.cursor()

    cursor.execute(sql_query, params)
    conn.commit()

    cursor.close()
    conn.close()

def queryDbGetRow(sql_query, params):
    conn = pyodbc.connect(os.environ.get('ODBC_DB_CONNECTION_STRING'))
    cursor = conn.cursor()

    row = cursor.execute(sql_query, params).fetchone()
    conn.commit()

    cursor.close()
    conn.close()

    return row

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

    sql_query = '''
        SELECT SeriesId FROM [dbo].[Series]
        WHERE SeriesTitle = ?
    '''
    params = series_title

    series_id = queryDbGetRow(sql_query=sql_query, params=params).SeriesId

    return series_id

def addSeasonToDb(season):
    sql_query = '''
        INSERT INTO [dbo].[Seasons] (SeriesId, SeasonTitle, IsCurrentSeason)
        SELECT ?, ?, ?
        WHERE NOT EXISTS 
            (SELECT 1 
            FROM [dbo].[Seasons] 
            WHERE SeriesId = ?
            AND SeasonTitle = ?)
    '''
    params = (season.series_internal_id, season.title, season.is_current_season, season.series_internal_id, season.title)
    queryDbInsert(sql_query=sql_query, params=params)

    sql_query = '''
        SELECT SeasonId FROM [dbo].[Seasons]
        WHERE SeriesId = ? AND SeasonTitle = ?
    '''
    params = (season.series_internal_id, season.title)

    season_id = queryDbGetRow(sql_query=sql_query, params=params).SeasonId

    return season_id

def addChannelToDb(channel):
    sql_query = '''
        INSERT INTO [dbo].[Channels] (ChannelYouTubeId, ChannelName, ChannelThumbnailUri)
        SELECT ?, ?, ?
        WHERE NOT EXISTS 
            (SELECT 1 
            FROM [dbo].[Channels] 
            WHERE ChannelYouTubeId = ?)
    '''
    params = (channel.youtube_id, channel.name, channel.thumbnail_uri, channel.youtube_id)
    queryDbInsert(sql_query=sql_query, params=params)

    sql_query = '''
        SELECT ChannelId FROM [dbo].[Channels]
        WHERE ChannelYouTubeId = ?
    '''
    params = (channel.youtube_id)

    channel_internal_id = queryDbGetRow(sql_query=sql_query, params=params).ChannelId

    return channel_internal_id

def addSeasonAppearanceToDb(season_appearance):
    sql_query = '''
        INSERT INTO [dbo].[SeasonAppearances] (SeasonId, ChannelId)
        SELECT ?, ?
        WHERE NOT EXISTS 
            (SELECT 1 
            FROM [dbo].[SeasonAppearances] 
            WHERE SeasonId = ?
            AND ChannelId = ?)
    '''
    params = (season_appearance.season_internal_id, season_appearance.channel_internal_id, 
              season_appearance.season_internal_id, season_appearance.channel_internal_id)
    queryDbInsert(sql_query=sql_query, params=params)

    sql_query = '''
        SELECT SeasonAppearanceId FROM [dbo].[SeasonAppearances]
        WHERE SeasonId = ? AND ChannelId = ?
    '''
    params = (season_appearance.season_internal_id, season_appearance.channel_internal_id)

    season_appearance_internal_id = queryDbGetRow(sql_query=sql_query, params=params).SeasonAppearanceId

    return season_appearance_internal_id

    

def processPlaylistVideos(playlist_id, season_internal_id):
    request = youtube.playlistItems().list(
        part=PLAYLIST_ITEMS_REQUEST_PART,
        maxResults=PLAYLIST_ITEMS_MAX_RESULTS,
        playlistId=playlist_id
    )
    response = request.execute()
    processPlaylistPage(response=response, season_internal_id=season_internal_id)

    while 'nextPageToken' in response:
        request = youtube.playlistItems().list(
            part=PLAYLIST_ITEMS_REQUEST_PART,
            maxResults=PLAYLIST_ITEMS_MAX_RESULTS,
            playlistId=playlist_id,
            pageToken = response.get('nextPageToken')
        )
        response = request.execute()
        processPlaylistPage(response=response, season_internal_id=season_internal_id)


def processPlaylistPage(response, season_internal_id):
    for playlist_item in response.get('items'):
        '''
        Ensures only public videos are processed
        '''
        if 'videoId' in playlist_item.get('contentDetails') and playlist_item.get('status').get('privacyStatus') == 'public':
            channel = parseChannel(channel_id=playlist_item.get('snippet').get('videoOwnerChannelId'))
            channel_internal_id = addChannelToDb(channel)

            season_appearance = SeasonAppearance(
                channel_internal_id=channel_internal_id,
                season_internal_id=season_internal_id)
            season_appearanace_internal_id = addSeasonAppearanceToDb(season_appearance)
            
            video_id = playlist_item.get('contentDetails').get('videoId')
            video_published_at = playlist_item.get('contentDetails').get('videoPublishedAt')
            video_title = playlist_item.get('snippet').get('title')
            video_thumbnail_uri = playlist_item.get('snippet').get('thumbnails').get('high').get('url')
            '''
            video = Video(
                youtube_id=video_id,
                title=video_title, 
                season_appearance_internal_id=season_appearanace_internal_id,
                thumbnail_uri=video_thumbnail_uri,
                published_at=video_published_at)
            '''
            #addVideoToDb(video)

def parseChannel(channel_id):
    request = youtube.channels().list(
        part='snippet',
        maxResults=1,
        id=channel_id
    )
    response = request.execute()
    snippet = response.get('items')[0].get('snippet')

    thumbnail_uri = snippet.get('thumbnails').get('high').get('url')
    name = snippet.get('title')
    channel = Channel(youtube_id=channel_id, name=name, thumbnail_uri=thumbnail_uri)
    return channel

processWikiData()
