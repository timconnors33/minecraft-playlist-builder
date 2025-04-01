import file_handler.file_handler
import wiki_parser
import wiki_parser.wiki_parser
import youtube_api_handler
import loader
import pandas as pd
import file_handler

def filterCurrentSeasons(df):
    new_df = df.drop(df[df['is_current_season'] == False].index)
    return new_df

def filterDev(df):
    new_df = df.drop(df[df['youtube_internal_link'] != 'playlist?list=PL2XncHqN_7yI07heM6HAV-FBL80eeEZ0a&si=dY0mOyIwhi8hW8A2'].index)
    return new_df

def runCurrentSeasons():
    wiki_data_filepath = wiki_parser.wiki_parser.parse()
    df = file_handler.file_handler.readFromCsv(filepath=wiki_data_filepath)
    df = filterCurrentSeasons(df=df)
    filtered_filepath = file_handler.file_handler.writeToCsv(df=df, filepath='./data/filtered-wiki-data.csv')
    youtube_metadata_filepath = youtube_api_handler.processWikiData(input_filepath=filtered_filepath)
    #loader.uploadData(video_metadata_list=video_metadata_list)
    
runCurrentSeasons()