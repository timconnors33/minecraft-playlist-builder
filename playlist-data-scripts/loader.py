import os
import googleapiclient.discovery
import cProfile
import wiki_parser
import wiki_parser.wiki_parser
import db_api
import data_objects

YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')
PLAYLIST_ITEMS_REQUEST_PART = 'snippet,contentDetails,status'
PLAYLIST_ITEMS_MAX_RESULTS = 50

youtube = googleapiclient.discovery.build(
        serviceName='youtube', version='v3', developerKey=YOUTUBE_API_KEY
)

existing_channel_ids = {}
existing_season_appearance_ids = {}
existing_video_youtube_ids = set()

def processWikiData(series_list):
    getExistingData()
    for series in series_list:
        series_title = series['title']
        series_internal_id = db_api.insertSeries(series_title=series_title)
        for season in series['seasons']:
            cur_season = data_objects.Season(title=season['title'], series_internal_id=series_internal_id, is_current_season=season['is_current_season'])
            print('Currently processing ' + cur_season.title)
            cur_season_internal_id = db_api.insertSeason(season=cur_season)
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
    return channel

#cProfile.run('processWikiData(only_current_seasons=True)')
