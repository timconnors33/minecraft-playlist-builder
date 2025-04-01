from dotenv import load_dotenv, find_dotenv
import os
import wiki_parser
import wiki_parser.wiki_parser
import youtube_api_handler
import loader
import pandas as pd

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
    new_df = df.drop(df[df['youtube_internal_link'] != 'playlist?list=PL2XncHqN_7yI07heM6HAV-FBL80eeEZ0a&si=dY0mOyIwhi8hW8A2'].index)
    return new_df

def runCurrentSeasons():
    df = wiki_parser.wiki_parser.parse()
    df = filterCurrentSeasons(df=df)
    df = filterDev(df)
    filtered_filepath = writeToCsv(df=df, filepath='./data/filtered-wiki-data.csv')
    youtube_metadata_df = youtube_api_handler.processWikiData(df=df)
    writeToCsv(youtube_metadata_df, './data/video-metadata.csv')
    loader.uploadData(video_metadata_df=youtube_metadata_df)
    
runCurrentSeasons()