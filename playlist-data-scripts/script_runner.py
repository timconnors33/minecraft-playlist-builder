from dotenv import load_dotenv, find_dotenv
import os
import wiki_parser
import wiki_parser.wiki_parser
import youtube_api_handler
import loader
import pandas as pd
import cProfile

load_dotenv(find_dotenv())

# TODO: Add error handling
def writeToCsv(df, filepath):
    if os.environ.get('ENVIRONMENT') == 'production' or not os.path.exists(filepath):
        df.to_csv(filepath)
    return filepath
    
def readFromCsv(filepath):
    return pd.read_csv(filepath)

def filterCurrentSeasons(df):
    new_df = df.drop(df[df['is_current_season'] == False].index)
    return new_df

def filterDev(df):
    new_df = df.drop(df[df['season_title'] != 'Season 9'].index)
    # Scar's, Bdub's, and Ethos's season 9 videos
    allowed_links = ['PLSCZsQa9VSCc-7-qOc8O7t9ZraR4L5y0Y', 'PL2XncHqN_7yJhlp6JgHAQG4M5LJmhmZlW', 'EthosLab']
    new_df = new_df[new_df['youtube_internal_link'].isin(allowed_links)]
    scar_third_life = [{'series_title': 'Life Series',
                        'season_title': 'Third Life',
                        'is_current_season': 'False',
                        'youtube_internal_link': 'PLSCZsQa9VSCf4dGJL_0U1wt2UaPhUbTqB',
                        'link_type': 'playlist'}]
    new_df = pd.concat([new_df, pd.DataFrame(scar_third_life)])
    return new_df

def runDev():
    if os.environ.get('ENVIRONMENT') == 'development': 
        df = wiki_parser.wiki_parser.parse()
        writeToCsv(df=df, filepath='./data/raw-wiki-data.csv')
        df = filterDev(df)
        writeToCsv(df=df, filepath='./data/filtered-wiki-data.csv')
        youtube_metadata_df = youtube_api_handler.processWikiData(df=df)
        writeToCsv(youtube_metadata_df, './data/video-metadata.csv')
        loader.uploadData(video_metadata_df=youtube_metadata_df)
    else:
        print('Environment is not set to development.')

def runCurrentSeasons():
    print('Fetching data for current seasons')
    df = wiki_parser.wiki_parser.parse()
    writeToCsv(df=df, filepath='./data/raw-wiki-data.csv')
    df = filterCurrentSeasons(df=df)
    writeToCsv(df=df, filepath='./data/filtered-wiki-data.csv')
    youtube_metadata_df = youtube_api_handler.processWikiData(df=df)
    writeToCsv(youtube_metadata_df, './data/video-metadata.csv')
    loader.uploadData(video_metadata_df=youtube_metadata_df)

def runAllSeasons():
    print('Fetching data for all seasons')
    df = wiki_parser.wiki_parser.parse()
    writeToCsv(df=df, filepath='./data/raw-wiki-data.csv')
    youtube_metadata_df = youtube_api_handler.processWikiData(df=df)
    writeToCsv(youtube_metadata_df, './data/video-metadata.csv')
    loader.uploadData(video_metadata_df=youtube_metadata_df)

#cProfile.run('runDev()')
