export interface Series {
    seriesTitle: string;
    seasons: Season[];
}

export interface Season {
    seasonTitle: string;
    channels: Channel[];
}

export interface Channel {
    channelName: string;
    channelYouTubeId: string;
    channelThumbnailUri: string;
}

export interface SeasonAppearance {
    series: Series[];
}