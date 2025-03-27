from youtube_video_data import processWikiData

def updateCurrentSeasonsData():
    processWikiData(only_current_seasons=True)

updateCurrentSeasonsData()