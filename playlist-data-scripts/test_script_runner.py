import script_runner
import pytest
from dotenv import load_dotenv, find_dotenv
import pyodbc
import os
import db_api

load_dotenv(find_dotenv())
db_conn_str = os.environ.get('DEV_ODBC_DB_CONNECTION_STRING')

@pytest.fixture(scope='session')
def setupTeardownDevDatabase():
    cleanUpDatabase()
    initializeDatabase()
    yield
    cleanUpDatabase()

def initializeDatabase():
    script_runner.runDev()

def cleanUpDatabase():
    conn = pyodbc.connect(db_conn_str)
    cursor = conn.cursor()
    
    sql_query = """ DELETE FROM [dbo].[Videos];
                    DELETE FROM [dbo].[SeasonAppearances];
                    DELETE FROM [dbo].[Seasons];
                    DELETE FROM [dbo].[Series];
                    DELETE FROM [dbo].[Channels];"""

    cursor.execute(sql_query)
    conn.commit()

    cursor.close()
    conn.close()
    
def test_playlist_pagination(setupTeardownDevDatabase):
    scar_channel = [c for c in db_api.getChannels() if c.ChannelYouTubeId == 'UCodkNmk9oWRTIYZdr_HuSlg'].pop()
    hermitcraft_season_9 = [s for s in db_api.getSeasons() if s.SeasonTitle == 'Season 9' and s.SeriesTitle == 'Hermitcraft'].pop()
    scar_season_appearance = [s for s in db_api.getSeasonAppearances() if s.ChannelId == scar_channel.ChannelId and s.SeasonId == hermitcraft_season_9.SeasonId].pop()
    scar_videos = [v for v in db_api.getVideos() if v.SeasonAppearanceId == scar_season_appearance.SeasonAppearanceId]
    assert len(scar_videos) > 50
    
def test_series_upload(setupTeardownDevDatabase):
    series = db_api.getSeries()
    matching_series = [s for s in series if s.SeriesTitle == 'Hermitcraft']
    
    assert len(series) == 2
    assert len(matching_series) == 1

def test_season_upload(setupTeardownDevDatabase):
    seasons = db_api.getSeasons()
    matching_seasons = [s for s in seasons if s.SeasonTitle == 'Season 9' and s.SeriesTitle == 'Hermitcraft']
    
    assert len(seasons) == 2
    assert len(matching_seasons) == 1

def test_channel_upload(setupTeardownDevDatabase):
    channels = db_api.getChannels()
    matching_scar_channels = [c for c in channels if c.ChannelYouTubeId == 'UCodkNmk9oWRTIYZdr_HuSlg']
    matching_bdubs_channels = [c for c in channels if c.ChannelYouTubeId == 'UClu2e7S8atp6tG2galK9hgg']
    matching_etho_channels = [c for c in channels if c.ChannelYouTubeId == 'UCFKDEp9si4RmHFWJW1vYsMA']
    
    assert len(matching_scar_channels) == 1
    assert len(matching_bdubs_channels) == 1
    assert len(matching_etho_channels) == 1
    assert len(channels) == 3

def test_season_appearance_upload(setupTeardownDevDatabase):
    season_appearances = db_api.getSeasonAppearances()
    scar_channel = [c for c in db_api.getChannels() if c.ChannelYouTubeId == 'UCodkNmk9oWRTIYZdr_HuSlg'].pop()
    scar_season_appearances = [s for s in season_appearances if s.ChannelId == scar_channel.ChannelId]
    hermitcraft_season_9 = [s for s in db_api.getSeasons() if s.SeasonTitle == 'Season 9' and s.SeriesTitle == 'Hermitcraft'].pop()
    third_life = [s for s in db_api.getSeasons() if s.SeasonTitle == '3rd Life' and s.SeriesTitle == 'Life Series'].pop()
    
    assert len(season_appearances) == 4
    assert len(scar_season_appearances) == 2
    assert len([s for s in scar_season_appearances if s.SeasonId == hermitcraft_season_9.SeasonId]) == 1
    assert len([s for s in scar_season_appearances if s.SeasonId == third_life.SeasonId]) == 1

def test_sql_injection_prevention(setupTeardownDevDatabase):
    original_channels = db_api.getChannels()
    sql_query = '''
        INSERT INTO [dbo].[Channels] (ChannelYouTubeId, ChannelName, ChannelThumbnailUri)
        VALUES (?, ?, ?)
    '''
    params = ('sqlInjectionTestYouTubeId', 'sqlInjectionTestChannelName', "'); DELETE FROM [dbo].[Channels]; -- ');")
    db_api.insert(sql_query=sql_query, params=params)
    
    new_channels = db_api.getChannels()
    
    assert len(original_channels) >= 1
    assert len(new_channels) == len(original_channels) + 1
    assert len([c for c in new_channels if c.ChannelThumbnailUri == "'); DELETE FROM [dbo].[Channels]; -- ');"]) == 1
    
    