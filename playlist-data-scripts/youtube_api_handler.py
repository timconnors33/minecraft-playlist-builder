import os
import googleapiclient.discovery
import data_objects
import file_handler
import pandas as pd

import file_handler.file_handler

YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')
PLAYLIST_ITEMS_REQUEST_PART = 'snippet,contentDetails,status'
PLAYLIST_ITEMS_MAX_RESULTS = 50

youtube = googleapiclient.discovery.build(
        serviceName='youtube', version='v3', developerKey=YOUTUBE_API_KEY
)

channels = {}

def processLink(series_title, season_title, youtube_internal_link):
    if 'list=PL' in youtube_internal_link:
        # TODO: This looks silly, but I want to make sure not to extract another
        # ID type. Will a 'list=' substring only ever be followed by a playlist ID?
        processed_link = 'PL' + (youtube_internal_link.split('list=PL', 1)[1]).split('&', 1)[0]
    else:
        processed_link = getSeasonAppearancePlaylist(series_title=series_title, season_title=season_title, channel_link=youtube_internal_link)
    return processed_link

def processWikiData(input_filepath):
    df = file_handler.file_handler.readFromCsv(input_filepath)
    df['youtube_internal_link'] = df.apply(lambda row: processLink(series_title=row['series_title'], season_title=row['season_title'], youtube_internal_link=row['youtube_internal_link']), axis=1)
    
    df.pop('link_type')
    
    df['video_metadata'] = df['youtube_internal_link'].apply(processPlaylistVideos)
    df = df.explode('video_metadata')
    metadata_df = pd.DataFrame(data=df['video_metadata'].values.tolist(), index=df.index)
    aggregated_df = pd.concat([df.drop('video_metadata', axis=1), metadata_df], axis=1)
    output_filepath = './data/video_metadata.csv'
    
    return file_handler.file_handler.writeToCsv(df=aggregated_df, filepath=output_filepath)

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

def processPlaylistVideos(playlist_id):
    video_metadata_list = []
    try:
        request = youtube.playlistItems().list(
            part=PLAYLIST_ITEMS_REQUEST_PART,
            maxResults=PLAYLIST_ITEMS_MAX_RESULTS,
            playlistId=playlist_id
        )
        response = request.execute()
        video_metadata_list.extend(processPlaylistPage(response=response))

        while 'nextPageToken' in response:
            request = youtube.playlistItems().list(
                part=PLAYLIST_ITEMS_REQUEST_PART,
                maxResults=PLAYLIST_ITEMS_MAX_RESULTS,
                playlistId=playlist_id,
                pageToken = response.get('nextPageToken')
            )
            response = request.execute()
            video_metadata_list.extend(processPlaylistPage(response=response))
    # If there is an HTTP error (like if the specified playlist is not found),
    # log and keep processing.
    except googleapiclient.errors.HttpError as err:
        print(err)
        pass
    
    return video_metadata_list

def processPlaylistPage(response):
    video_metadata_list = []
    
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
                video_id=video_id,
                video_title=video_title,
                video_thumbnail_uri=video_thumbnail_uri,
                video_published_at=video_published_at,
                channel_id=channel_youtube_id,
                channel_name=channel.name,
                channel_thumbnail_uri=channel.thumbnail_uri,
            )
            video_metadata_list.append(video_metadata.__dict__)
            
    return video_metadata_list
            

def parseChannel(channel_id):
    if channel_id not in channels:
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
        channels[channel_id] = channel
    else:
        channel = channels[channel_id]
    return channel
