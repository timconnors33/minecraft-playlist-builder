from dotenv import load_dotenv, find_dotenv
import pyodbc
import os

# TODO: Can this line be a top-level statement?
load_dotenv(find_dotenv())
db_conn_str = os.environ.get('DEV_ODBC_DB_CONNECTION_STRING')
if os.environ.get('ENVIRONMENT') == 'production':
    db_conn_str = os.environ.get('ODBC_DB_CONNECTION_STRING')
print('db_conn_str: ' + db_conn_str)

def getChannels():
    sql_query = 'SELECT ChannelId, ChannelYoutubeId FROM [dbo].[Channels]'
    rows = getAll(sql_query=sql_query)

    return rows

def getSeasonAppearances():
    sql_query = 'SELECT ChannelId, SeasonId, SeasonAppearanceId FROM [dbo].[SeasonAppearances]'
    rows = getAll(sql_query=sql_query)

    return rows

def getAll(sql_query):
    conn = pyodbc.connect(db_conn_str)
    cursor = conn.cursor()

    rows = cursor.execute(sql_query).fetchall()
    conn.commit()

    cursor.close()
    conn.close()

    return rows

def getVideos():

    sql_query = 'SELECT VideoYouTubeId FROM [dbo].[Videos]'
    rows = getAll(sql_query=sql_query)

    return rows

def insert(sql_query, params):
    try:
        conn = pyodbc.connect(db_conn_str)
        cursor = conn.cursor()

        cursor.execute(sql_query, params)
        conn.commit()

        cursor.close()
        conn.close()

    # If violating integrity constraint, (like trying to insert an existing unique value),
    # pass and keep inserting other rows.
    except pyodbc.IntegrityError:
        pass

def getRow(sql_query, params):
    conn = pyodbc.connect(db_conn_str)
    cursor = conn.cursor()

    row = cursor.execute(sql_query, params).fetchone()
    conn.commit()

    cursor.close()
    conn.close()

    return row

def insertSeries(series_title):
    # https://stackoverflow.com/questions/20971680/sql-server-insert-if-not-exists
    sql_query = '''
        INSERT INTO [dbo].[Series] (SeriesTitle)
        VALUES (?)
    '''
    insert(sql_query=sql_query, params=(series_title))

    sql_query = '''
        SELECT SeriesId FROM [dbo].[Series]
        WHERE SeriesTitle = ?
    '''
    params = series_title

    series_id = getRow(sql_query=sql_query, params=params).SeriesId

    return series_id

def insertSeason(season):
    sql_query = '''
        INSERT INTO [dbo].[Seasons] (SeriesId, SeasonTitle, IsCurrentSeason)
        VALUES (?, ?, ?)
    '''
    params = (season.series_internal_id, season.title, season.is_current_season)
    insert(sql_query=sql_query, params=params)

    sql_query = '''
        SELECT SeasonId FROM [dbo].[Seasons]
        WHERE SeriesId = ? AND SeasonTitle = ?
    '''
    params = (season.series_internal_id, season.title)

    season_id = getRow(sql_query=sql_query, params=params).SeasonId

    return season_id

def insertChannel(channel):
    sql_query = '''
        INSERT INTO [dbo].[Channels] (ChannelYouTubeId, ChannelName, ChannelThumbnailUri)
        VALUES (?, ?, ?)
    '''
    params = (channel.youtube_id, channel.name, channel.thumbnail_uri)
    insert(sql_query=sql_query, params=params)

    sql_query = '''
        SELECT ChannelId FROM [dbo].[Channels]
        WHERE ChannelYouTubeId = ?
    '''
    params = (channel.youtube_id)

    channel_internal_id = getRow(sql_query=sql_query, params=params).ChannelId

    return channel_internal_id

def insertSeasonAppearance(season_appearance):
    sql_query = '''
        INSERT INTO [dbo].[SeasonAppearances] (SeasonId, ChannelId)
        VALUES (?, ?)
    '''
    params = (season_appearance.season_internal_id, season_appearance.channel_internal_id)
    insert(sql_query=sql_query, params=params)

    sql_query = '''
        SELECT SeasonAppearanceId FROM [dbo].[SeasonAppearances]
        WHERE SeasonId = ? AND ChannelId = ?
    '''
    params = (season_appearance.season_internal_id, season_appearance.channel_internal_id)

    season_appearance_internal_id = getRow(sql_query=sql_query, params=params).SeasonAppearanceId

    return season_appearance_internal_id

def insertVideo(video):
    sql_query = '''
        INSERT INTO [dbo].[Videos] (VideoYouTubeId, VideoTitle, VideoThumbnailUri, VideoPublishedAt, SeasonAppearanceId)
        VALUES (?, ?, ?, ?, ?)
    '''
    params = (video.youtube_id,
              video.title,
              video.thumbnail_uri,
              video.published_at.replace('T', ' ').replace('Z', ''),
              video.season_appearance_internal_id)
    insert(sql_query=sql_query, params=params)

    sql_query = '''
        SELECT VideoId FROM [dbo].[Videos]
        WHERE VideoYouTubeId = ?
    '''
    params = (video.youtube_id)

    video_internal_id = getRow(sql_query=sql_query, params=params).VideoId

    return video_internal_id