namespace MinecraftPlaylistBuilderApp.Server.Dtos
{
    public record PlaylistVideoDto
    (
        Guid PublicPlaylistVideoId,
        string VideoTitle,
        string VideoYouTubeId,
        bool IsWatched,
        string ChannelName,
        DateTime VideoPublishedAt
    )
    {
    }
    public record CreatePlaylistVideoDto
    (
        string[] ChannelNames
    )
    {
    }

    public record UpdatePlaylistVideoDto
    (
        bool IsWatched
    )
    {
    }

    public record DeletePlaylistVideoDto
    (
        Guid PublicPlaylistVideoId
    )
    {
    }

    public record GetPlaylistVideoDto
    (
        Guid PublicPlaylistVideoId
    )
    {
    }

    public record GetPlaylistVideosByPlaylistDto
    (
        Guid PublicPlaylistVideoId
    )
    {
    }
}
