CREATE TABLE [Playlists]
(
    PlaylistId INTEGER IDENTITY PRIMARY KEY,
    PublicPlaylistId UNIQUEIDENTIFIER,
    SeasonId INTEGER NOT NULL,
    OwnerId UNIQUEIDENTIFIER NOT NULL,
    PlaylistTitle NVARCHAR(64) NOT NULL,
    CONSTRAINT FK_PlaylistSeasonId FOREIGN KEY (SeasonId) REFERENCES dbo.[Seasons](SeasonId),
);