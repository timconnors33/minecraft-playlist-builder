CREATE TABLE [Videos]
(
    VideoId INTEGER IDENTITY PRIMARY KEY,
    VideoYouTubeId NVARCHAR(32) UNIQUE NOT NULL,
    VideoTitle NVARCHAR(128) NOT NULL,
    VideoThumbnailUri NVARCHAR(2048) NOT NULL,
    VideoPublishedAt DATETIME NOT NULL,
    SeasonAppearanceId INTEGER NOT NULL,
    CONSTRAINT FK_SEASONAPPEARANCEID FOREIGN KEY (SeasonAppearanceId) REFERENCES dbo.[SeasonAppearances](SeasonAppearanceId),
);