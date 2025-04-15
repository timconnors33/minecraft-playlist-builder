import script_runner
import pytest
from dotenv import load_dotenv, find_dotenv
import pyodbc
import os
import db_api

load_dotenv(find_dotenv())
db_conn_str = os.environ.get('DEV_ODBC_DB_CONNECTION_STRING')

@pytest.fixture
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
    scar_season_appearance = [s for s in db_api.getSeasonAppearances() if s.ChannelId == scar_channel.ChannelId].pop()
    scar_videos = [v for v in db_api.getVideos() if v.SeasonAppearanceId == scar_season_appearance.SeasonAppearanceId]
    assert len(scar_videos) > 50