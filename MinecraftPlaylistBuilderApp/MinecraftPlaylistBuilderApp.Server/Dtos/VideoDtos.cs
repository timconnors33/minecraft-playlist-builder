namespace MinecraftPlaylistBuilderApp.Server.Dtos
{
    public record VideoDto(string VideoYouTubeId) { }
    public record PostVideosDto(string SeriesTitle, string SeasonTitle, string[] ChannelNames) { }

}
