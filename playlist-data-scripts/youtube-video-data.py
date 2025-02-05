import os
from dotenv import load_dotenv, find_dotenv
import json
import googleapiclient.discovery
import pyodbc
import cProfile


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

existing_channel_ids = {}
existing_season_appearance_ids = {}
existing_video_youtube_ids = set()

def getWikiData():
    filepath = './data/hermitcraft/season-appearances.json'

    if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                series = json.load(f)

    return series

def processWikiData(seasons_to_process, filter):
    getExistingData()
    series_list = getWikiData()
    for series in series_list:
        series_title = series['title']
        series_internal_id = addSeriesToDb(series_title=series_title)
        for season in series['seasons']:
            if not filter or series_title + ' ' + season['title'] in seasons_to_process:
                cur_season = Season(title=season['title'], series_internal_id=series_internal_id, is_current_season=season['is_current_season'])
                print('Currently processing ' + cur_season.title)
                cur_season_internal_id = addSeasonToDb(season=cur_season)
                for wiki_season_appearance in season['season_appearances']:
                        youtube_link = wiki_season_appearance['youtube_internal_link']
                        if 'list=PL' in youtube_link:
                            # TODO: This looks silly, but I want to make sure not to extract another
                            # ID type. Will a 'list=' substring only ever be followed by a playlist ID?
                            youtube_link = 'PL' + (youtube_link.split('list=PL', 1)[1]).split('&', 1)[0]
                        else:
                            youtube_link = getSeasonAppearancePlaylist(series_title=series_title, season_title=cur_season.title, channel_link=youtube_link)
                        processPlaylistVideos(playlist_id=youtube_link, season_internal_id=cur_season_internal_id)

def getExistingData():
    getExistingChannels()
    getExistingSeasonAppearances()
    getExistingVideos()

def getExistingChannels():
    sql_query = 'SELECT ChannelId, ChannelYoutubeId FROM [dbo].[Channels]'
    rows = queryDbGetAllRows(sql_query=sql_query)

    for row in rows:
        existing_channel_ids[row.ChannelYoutubeId] = row.ChannelId

def getExistingSeasonAppearances():
    sql_query = 'SELECT ChannelId, SeasonId, SeasonAppearanceId FROM [dbo].[SeasonAppearances]'
    rows = queryDbGetAllRows(sql_query=sql_query)

    for row in rows:
        existing_season_appearance_ids[(row.ChannelId, row.SeasonId)] = row.SeasonAppearanceId

def queryDbGetAllRows(sql_query):
    conn = pyodbc.connect(os.environ.get('ODBC_DB_CONNECTION_STRING'))
    cursor = conn.cursor()

    rows = cursor.execute(sql_query).fetchall()
    conn.commit()

    cursor.close()
    conn.close()

    return rows

def getExistingVideos():

    sql_query = 'SELECT VideoYouTubeId FROM [dbo].[Videos]'
    rows = queryDbGetAllRows(sql_query=sql_query)

    for row in rows:
        existing_video_youtube_ids.add(row.VideoYouTubeId)

def getSeasonAppearancePlaylist(series_title, season_title, channel_link):
    if channel_link.startswith('@'):
        request = youtube.channels().list(
            part='snippet',
            forHandle=channel_link,
            maxResults=1,
        )
        
    else:
        channel_link = channel_link.replace('user/', '')
        request = youtube.channels().list(
            part='snippet',
            forUsername=channel_link,
            maxResults=1,
        )

    response = request.execute()
    channel_name = response.get('items')[0]['snippet']['title']
    
    queryString = channel_name + ' ' + series_title + ' ' + season_title
    request = youtube.search().list(
        part='snippet',
        maxResults=1,
        q=queryString,
        type='playlist'
    )
    response = request.execute()

    playlist_id = response.get('items')[0]['id']['playlistId']
    return playlist_id

def queryDbInsert(sql_query, params):
    try:
        conn = pyodbc.connect(os.environ.get('ODBC_DB_CONNECTION_STRING'))
        cursor = conn.cursor()

        cursor.execute(sql_query, params)
        conn.commit()

        cursor.close()
        conn.close()

    # If violating integrity constraint, (like trying to insert an existing unique value),
    # pass and keep inserting other rows.
    except pyodbc.IntegrityError:
        pass

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
        VALUES (?)
    '''
    queryDbInsert(sql_query=sql_query, params=(series_title))

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
        VALUES (?, ?, ?)
    '''
    params = (season.series_internal_id, season.title, season.is_current_season)
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
        VALUES (?, ?, ?)
    '''
    params = (channel.youtube_id, channel.name, channel.thumbnail_uri)
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
        VALUES (?, ?)
    '''
    params = (season_appearance.season_internal_id, season_appearance.channel_internal_id)
    queryDbInsert(sql_query=sql_query, params=params)

    sql_query = '''
        SELECT SeasonAppearanceId FROM [dbo].[SeasonAppearances]
        WHERE SeasonId = ? AND ChannelId = ?
    '''
    params = (season_appearance.season_internal_id, season_appearance.channel_internal_id)

    season_appearance_internal_id = queryDbGetRow(sql_query=sql_query, params=params).SeasonAppearanceId

    return season_appearance_internal_id

async def addVideoToDb(video):
    sql_query = '''
        INSERT INTO [dbo].[Videos] (VideoYouTubeId, VideoTitle, VideoThumbnailUri, VideoPublishedAt, SeasonAppearanceId)
        VALUES (?, ?, ?, ?, ?)
    '''
    params = (video.youtube_id,
              video.title,
              video.thumbnail_uri,
              video.published_at.replace('T', ' ').replace('Z', ''),
              video.season_appearance_internal_id)
    queryDbInsert(sql_query=sql_query, params=params)

    sql_query = '''
        SELECT VideoId FROM [dbo].[Videos]
        WHERE VideoYouTubeId = ?
    '''
    params = (video.youtube_id)

    video_internal_id = queryDbGetRow(sql_query=sql_query, params=params).VideoId

    return video_internal_id

    

def processPlaylistVideos(playlist_id, season_internal_id):
    try:
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
    # If there is an HTTP error (like if the specified playlist is not found),
    # log and keep processing.
    except googleapiclient.errors.HttpError as err:
        print(err)
        pass

def processPlaylistPage(response, season_internal_id):
    for playlist_item in response.get('items'):
        '''
        Ensures only public videos are processed
        '''
        if 'videoId' in playlist_item.get('contentDetails') and playlist_item.get('status').get('privacyStatus') == 'public':
            channel_youtube_id = playlist_item.get('snippet').get('videoOwnerChannelId')
            if channel_youtube_id in existing_channel_ids:
                channel_internal_id = existing_channel_ids[channel_youtube_id]
            else:
                channel = parseChannel(channel_id=channel_youtube_id)
                channel_internal_id = addChannelToDb(channel)
                existing_channel_ids[channel_youtube_id] = channel_internal_id

            season_appearance = SeasonAppearance(
                channel_internal_id=channel_internal_id,
                season_internal_id=season_internal_id)
            if (channel_internal_id, season_internal_id) not in existing_season_appearance_ids:
                season_appearanace_internal_id = addSeasonAppearanceToDb(season_appearance)
                existing_season_appearance_ids[(channel_internal_id, season_internal_id)] = season_appearanace_internal_id
            else:
                season_appearanace_internal_id = existing_season_appearance_ids[(channel_internal_id, season_internal_id)]
            
            video_id = playlist_item.get('contentDetails').get('videoId')
            video_published_at = playlist_item.get('contentDetails').get('videoPublishedAt')
            video_title = playlist_item.get('snippet').get('title')
            video_thumbnail_uri = playlist_item.get('snippet').get('thumbnails').get('high').get('url')
            
            video = Video(
                youtube_id=video_id,
                title=video_title, 
                season_appearance_internal_id=season_appearanace_internal_id,
                thumbnail_uri=video_thumbnail_uri,
                published_at=video_published_at)
            
            if video.youtube_id not in existing_video_youtube_ids:
                addVideoToDb(video)
                existing_video_youtube_ids.add(video.youtube_id)

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


seasons_to_process = [  
                        'Hermitcraft Season 10']

cProfile.run('processWikiData(filter=False, seasons_to_process=seasons_to_process)')
