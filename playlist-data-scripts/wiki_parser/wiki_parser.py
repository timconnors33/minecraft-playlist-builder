from . import hermitcraft_wiki_parser, life_series_wiki_parser
import pandas as pd
import sys

def parse():
    df = hermitcraft_wiki_parser.parseWikiPages()
    df = pd.concat([df, life_series_wiki_parser.parseWikiPages()], ignore_index=True)
    return df
    