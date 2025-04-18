import db_api
import data_objects

existing_series_ids = {}
existing_season_ids = {}
existing_channel_ids = {}
existing_season_appearance_ids = {}
existing_video_youtube_ids = set()

def uploadData(video_metadata_df):
    getExistingData()
    video_metadata_df.apply(processVideoMetadata, axis=1)

def processVideoMetadata(video_metadata):
    
        if video_metadata.series_title not in existing_series_ids:
            series_internal_id = db_api.insertSeries(series_title=video_metadata.series_title)
            existing_series_ids[video_metadata.series_title] = series_internal_id
        else :
            series_internal_id = existing_series_ids[video_metadata.series_title]
        
        if (video_metadata.series_title, video_metadata.season_title) not in existing_season_ids:
            season = data_objects.Season(title=video_metadata.season_title, series_internal_id=series_internal_id, is_current_season=video_metadata.is_current_season)
            season_internal_id = db_api.insertSeason(season=season)
            existing_season_ids[(video_metadata.series_title, video_metadata.season_title)] = season_internal_id
        else:
            season_internal_id = existing_season_ids[(video_metadata.series_title, video_metadata.season_title)]
        
        if video_metadata.channel_id not in existing_channel_ids:
            channel = data_objects.Channel(youtube_id=video_metadata.channel_id, name=video_metadata.channel_name, thumbnail_uri=video_metadata.channel_thumbnail_uri)
            channel_internal_id = db_api.insertChannel(channel)
            existing_channel_ids[video_metadata.channel_id] = channel_internal_id
        else:
            channel_internal_id = existing_channel_ids[video_metadata.channel_id]
        
        if (channel_internal_id, season_internal_id) not in existing_season_appearance_ids:
            season_appearance = data_objects.SeasonAppearance(channel_internal_id=channel_internal_id, season_internal_id=season_internal_id)
            season_appearanace_internal_id = db_api.insertSeasonAppearance(season_appearance)
            existing_season_appearance_ids[(channel_internal_id, season_internal_id)] = season_appearanace_internal_id
        else:
            season_appearanace_internal_id = existing_season_appearance_ids[(channel_internal_id, season_internal_id)]
        
        if video_metadata.video_id not in existing_video_youtube_ids:
            video = data_objects.Video(youtube_id=video_metadata.video_id, 
                                       title=video_metadata.video_title, 
                                       thumbnail_uri=video_metadata.video_thumbnail_uri,
                                       published_at=video_metadata.video_published_at,
                                       season_appearance_internal_id=season_appearanace_internal_id)
            db_api.insertVideo(video)
            existing_video_youtube_ids.add(video.youtube_id)

def getExistingData():
    getExistingSeries()
    getExistingSeasons()
    getExistingChannels()
    getExistingSeasonAppearances()
    getExistingVideos()
    
def getExistingSeries():
    rows = db_api.getSeries()
    
    for row in rows:
        existing_series_ids[row.SeriesTitle] = row.SeriesId
        
def getExistingSeasons():
    rows = db_api.getSeasons()
    
    for row in rows:
        existing_season_ids[(row.SeriesTitle, row.SeasonTitle)] = row.SeasonId

def getExistingChannels():
    rows = db_api.getChannels()

    for row in rows:
        existing_channel_ids[row.ChannelYoutubeId] = row.ChannelId

def getExistingSeasonAppearances():
    rows = db_api.getSeasonAppearances()

    for row in rows:
        existing_season_appearance_ids[(row.ChannelId, row.SeasonId)] = row.SeasonAppearanceId

def getExistingVideos():
    rows = db_api.getVideos()

    for row in rows:
        existing_video_youtube_ids.add(row.VideoYouTubeId)