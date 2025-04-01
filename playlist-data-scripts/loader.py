import db_api
import data_objects

existing_channel_ids = {}
existing_season_appearance_ids = {}
existing_video_youtube_ids = set()

def uploadData(video_metadata_list):
    getExistingData()
    for video_metadata in video_metadata_list:
        series_internal_id = db_api.insertSeries(series_title=video_metadata.series_title)
        
        season = data_objects.Season(title=video_metadata.season_title, series_internal_id=series_internal_id, is_current_season=video_metadata.is_current_season)
        season_internal_id = db_api.insertSeason(season=season)
        
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
                                       thumbnail_uri=video_metadata.thumbnail_uri,
                                       published_at=video_metadata.published_at,
                                       season_appearance_internal_id=season_appearanace_internal_id)
            db_api.insertVideo(video)
            existing_video_youtube_ids.add(video.youtube_id)
        

def getExistingData():
    getExistingChannels()
    getExistingSeasonAppearances()
    getExistingVideos()

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

""" def getSeasonAppearancePlaylist(series_title, season_title, channel_link):
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
        
        # Ensures only public videos are processed
        if 'videoId' in playlist_item.get('contentDetails') and playlist_item.get('status').get('privacyStatus') == 'public':
            channel_youtube_id = playlist_item.get('snippet').get('videoOwnerChannelId')
            if channel_youtube_id in existing_channel_ids:
                channel_internal_id = existing_channel_ids[channel_youtube_id]
            else:
                channel = parseChannel(channel_id=channel_youtube_id)
                channel_internal_id = db_api.insertChannel(channel)
                existing_channel_ids[channel_youtube_id] = channel_internal_id

            season_appearance = data_objects.SeasonAppearance(
                channel_internal_id=channel_internal_id,
                season_internal_id=season_internal_id)
            if (channel_internal_id, season_internal_id) not in existing_season_appearance_ids:
                season_appearanace_internal_id = db_api.insertSeasonAppearance(season_appearance)
                existing_season_appearance_ids[(channel_internal_id, season_internal_id)] = season_appearanace_internal_id
            else:
                season_appearanace_internal_id = existing_season_appearance_ids[(channel_internal_id, season_internal_id)]
            
            video_id = playlist_item.get('contentDetails').get('videoId')
            video_published_at = playlist_item.get('contentDetails').get('videoPublishedAt')
            video_title = playlist_item.get('snippet').get('title')
            video_thumbnail_uri = playlist_item.get('snippet').get('thumbnails').get('high').get('url')
            
            video = data_objects.Video(
                youtube_id=video_id,
                title=video_title, 
                season_appearance_internal_id=season_appearanace_internal_id,
                thumbnail_uri=video_thumbnail_uri,
                published_at=video_published_at)
            
            if video.youtube_id not in existing_video_youtube_ids:
                db_api.insertVideo(video)
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
    channel = data_objects.Channel(youtube_id=channel_id, name=name, thumbnail_uri=thumbnail_uri)
    return channel """
