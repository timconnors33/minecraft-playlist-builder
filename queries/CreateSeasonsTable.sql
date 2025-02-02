CREATE TABLE [Seasons]
(
    SeasonId INTEGER PRIMARY KEY,
    SeriesId INTEGER NOT NULL,
    SeasonTitle NVARCHAR(64) NOT NULL,
    IsCurrentSeason BIT NOT NULL,
    CONSTRAINT FK_SeriesId FOREIGN KEY (SeriesId) REFERENCES dbo.[Series](SeriesId),
    CONSTRAINT AK_SeriesSeasonTitles UNIQUE (SeriesId, SeasonTitle)
);