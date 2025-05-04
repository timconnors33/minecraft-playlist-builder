CREATE TABLE [PlaylistVideos]
(
    PlaylistVideoId INTEGER IDENTITY PRIMARY KEY,
    PlaylistId INTEGER NOT NULL,
    VideoId INTEGER NOT NULL,
    IsWatched BIT NOT NULL,
    CONSTRAINT FK_PLAYLISTID FOREIGN KEY (PlaylistId) REFERENCES dbo.[Playlists](PlaylistId),
    CONSTRAINT FK_VIDEOID FOREIGN KEY (VideoId) REFERENCES dbo.[Videos](VideoId),
    CONSTRAINT AK_PlaylistVideo UNIQUE (PlaylistId, VideoId)
);