from . import hermitcraft_wiki_parser
import pandas as pd
import sys

def parse():
    df = hermitcraft_wiki_parser.writeSeasonAppearanceLinksToFile()
    """ if only_current_seasons:
        for series in wiki_data:
            filtered = [season for season in series['seasons'] if season['is_current_season']]
            if filtered:
                new_series = series
                new_series['seasons'] = filtered
                processed_wiki_data.append(new_series) """
    return df
    