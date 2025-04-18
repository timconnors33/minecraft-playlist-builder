# Wiki pages

class SeasonLink():
    def __init__(self, internal_link, text, is_current_season):
        self.internal_link = internal_link
        self.text = text
        self.is_current_season = is_current_season

class SeasonAppearanceLink():
    def __init__(self, youtube_internal_link, link_type):
        self.youtube_internal_link = youtube_internal_link
        self.link_type = link_type
        
# DTOs

class VideoMetadata():
    def __init__(self, video_id, video_title, video_thumbnail_uri, video_published_at, 
                 channel_id, channel_name, channel_thumbnail_uri):
        self.video_id = video_id
        self.video_title = video_title
        self.video_thumbnail_uri = video_thumbnail_uri
        self.video_published_at = video_published_at
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.channel_thumbnail_uri = channel_thumbnail_uri

# Database objects

class Series():
    def __init__(self, title):
        self.title = title

class Season():
    def __init__(self, title, series_internal_id, is_current_season):
        self.title = title
        self.series_internal_id = series_internal_id
        self.is_current_season = is_current_season

class Video():
     def __init__(self, youtube_id, title, thumbnail_uri, published_at, season_appearance_internal_id):
        self.youtube_id = youtube_id
        self.title = title
        self.thumbnail_uri = thumbnail_uri
        self.published_at = published_at
        self.season_appearance_internal_id = season_appearance_internal_id

class SeasonAppearance():
    def __init__(self, channel_internal_id, season_internal_id):
        self.channel_internal_id = channel_internal_id
        self.season_internal_id = season_internal_id

class Channel():
    def __init__(self, youtube_id, name, thumbnail_uri):
        self.youtube_id = youtube_id
        self.name = name
        self.thumbnail_uri = thumbnail_uri