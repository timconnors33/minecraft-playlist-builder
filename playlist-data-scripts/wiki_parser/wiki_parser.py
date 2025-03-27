from . import hermitcraft_wiki_parser
import json

def parse(only_current_seasons=True):
    wiki_data = []
    wiki_data.append(hermitcraft_wiki_parser.parseWikiPages())
    processed_wiki_data = []
    if only_current_seasons:
        for series in wiki_data:
            filtered = [season for season in series['seasons'] if season['is_current_season']]
            if filtered:
                new_series = series
                new_series['seasons'] = filtered
                processed_wiki_data.append(new_series)
    #print(json.dumps(processed_wiki_data, indent=4))
    return processed_wiki_data