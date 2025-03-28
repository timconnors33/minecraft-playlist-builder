import wiki_parser
import wiki_parser.wiki_parser
import youtube_api_handler

def runCurrentSeasons():
    wiki_data = wiki_parser.wiki_parser.parse(only_current_seasons=True)
    video_metadata = youtube_api_handler.processWikiData(wiki_data)
    print(video_metadata)
    
runCurrentSeasons()