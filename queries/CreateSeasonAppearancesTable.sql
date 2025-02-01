CREATE TABLE [SeasonAppearances]
(
    SeasonAppearanceId INTEGER IDENTITY PRIMARY KEY,
    SeasonId INTEGER NOT NULL,
    ChannelId INTEGER NOT NULL,
    CONSTRAINT FK_SEASONID FOREIGN KEY (SeasonId) REFERENCES dbo.[Seasons](SeasonId),
    CONSTRAINT FK_CHANNELID FOREIGN KEY (ChannelId) REFERENCES dbo.[Channels](ChannelId)
);