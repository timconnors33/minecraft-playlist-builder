namespace MinecraftPlaylistBuilderApp.Server.Dtos
{
    public record VideoDto(string VideoYouTubeId, string VideoTitle, string VideoThumbnailUri, string ChannelName) { }
    public record PostVideosDto(string SeriesTitle, string SeasonTitle, string[] ChannelNames) { }

}
