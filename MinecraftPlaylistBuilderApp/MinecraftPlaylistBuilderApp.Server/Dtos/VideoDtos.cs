namespace MinecraftPlaylistBuilderApp.Server.Dtos
{
    public record VideoDto(
        string VideoTitle,
        string VideoYouTubeId,
        string VideoThumbnailUri)
    {
    }
}
