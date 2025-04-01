import file_handler.file_handler
from . import hermitcraft_wiki_parser
import pandas as pd
import file_handler
import sys

def parse():
    input_filepath = hermitcraft_wiki_parser.writeSeasonAppearanceLinksToFile()
    df = file_handler.file_handler.readFromCsv(filepath=input_filepath)
    """ if only_current_seasons:
        for series in wiki_data:
            filtered = [season for season in series['seasons'] if season['is_current_season']]
            if filtered:
                new_series = series
                new_series['seasons'] = filtered
                processed_wiki_data.append(new_series) """
    return file_handler.file_handler.writeToCsv(df=df, filepath='./data/agg-season-appearance-links.csv')
    