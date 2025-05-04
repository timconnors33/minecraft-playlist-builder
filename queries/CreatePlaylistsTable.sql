CREATE TABLE [Playlists]
(
    PlaylistId INTEGER IDENTITY PRIMARY KEY,
    UserId UNIQUEIDENTIFIER NOT NULL,
    PlaylistTitle NVARCHAR(64) NOT NULL,
    CONSTRAINT AK_UserPlaylistTitle UNIQUE (UserId, PlaylistTitle)
);