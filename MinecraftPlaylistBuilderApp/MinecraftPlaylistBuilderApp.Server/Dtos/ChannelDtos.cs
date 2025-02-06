namespace MinecraftPlaylistBuilderApp.Server.Dtos
{
    public record ChannelDto(
        string ChannelName,
        string ChannelYouTubeId,
        string ChannelThumbnailUri)
    {
    }
}
