import os
import googleapiclient.discovery
import cProfile
import data_objects

YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')
PLAYLIST_ITEMS_REQUEST_PART = 'snippet,contentDetails,status'
PLAYLIST_ITEMS_MAX_RESULTS = 50

youtube = googleapiclient.discovery.build(
        serviceName='youtube', version='v3', developerKey=YOUTUBE_API_KEY
)

def processWikiData(series_list):
    video_aggregates = []
    for series in series_list:
        series_title = series['title']
        for season in series['seasons']:
            print('Currently processing ' + season['title'])
            for wiki_season_appearance in season['season_appearances']:
                    youtube_link = wiki_season_appearance['youtube_internal_link']
                    if 'list=PL' in youtube_link:
                        # TODO: This looks silly, but I want to make sure not to extract another
                        # ID type. Will a 'list=' substring only ever be followed by a playlist ID?
                        youtube_link = 'PL' + (youtube_link.split('list=PL', 1)[1]).split('&', 1)[0]
                    else:
                        youtube_link = getSeasonAppearancePlaylist(series_title=series_title, season_title=season['title'], channel_link=youtube_link)
                    video_aggregates.append(processPlaylistVideos(playlist_id=youtube_link, series_title=series_title, season_title=season['title'], is_current_season=season['is_current_season']))
    return video_aggregates

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

def processPlaylistVideos(playlist_id, series_title, season_title, is_current_season):
    videos = []
    
    try:
        request = youtube.playlistItems().list(
            part=PLAYLIST_ITEMS_REQUEST_PART,
            maxResults=PLAYLIST_ITEMS_MAX_RESULTS,
            playlistId=playlist_id
        )
        response = request.execute()
        videos.append(processPlaylistPage(response=response, series_title=series_title, season_title=season_title, is_current_season=is_current_season))

        while 'nextPageToken' in response:
            request = youtube.playlistItems().list(
                part=PLAYLIST_ITEMS_REQUEST_PART,
                maxResults=PLAYLIST_ITEMS_MAX_RESULTS,
                playlistId=playlist_id,
                pageToken = response.get('nextPageToken')
            )
            response = request.execute()
            videos.append(processPlaylistPage(response=response, series_title=series_title, season_title=season_title, is_current_season=is_current_season))
    # If there is an HTTP error (like if the specified playlist is not found),
    # log and keep processing.
    except googleapiclient.errors.HttpError as err:
        print(err)
        pass
    
    return videos

def processPlaylistPage(response, series_title, season_title, is_current_season):
    videos = []
    
    for playlist_item in response.get('items'):
        
        # Ensures only public videos are processed
        if 'videoId' in playlist_item.get('contentDetails') and playlist_item.get('status').get('privacyStatus') == 'public':
            channel_youtube_id = playlist_item.get('snippet').get('videoOwnerChannelId')
            channel = parseChannel(channel_id=channel_youtube_id)
            
            video_id = playlist_item.get('contentDetails').get('videoId')
            video_published_at = playlist_item.get('contentDetails').get('videoPublishedAt')
            video_title = playlist_item.get('snippet').get('title')
            video_thumbnail_uri = playlist_item.get('snippet').get('thumbnails').get('high').get('url')
            
            video_metadata = data_objects.VideoMetadata(
                series_title=series_title,
                season_title=season_title,
                video_id=video_id,
                video_title=video_title,
                video_thumbnail_uri=video_thumbnail_uri,
                video_published_at=video_published_at,
                channel_id=channel_youtube_id,
                channel_name=channel.name,
                channel_thumbnail_uri=channel.thumbnail_uri
            )
            
            videos.append(video_metadata)
    return videos
            

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
