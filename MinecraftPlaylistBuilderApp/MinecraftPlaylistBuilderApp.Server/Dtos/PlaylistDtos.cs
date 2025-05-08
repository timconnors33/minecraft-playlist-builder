namespace MinecraftPlaylistBuilderApp.Server.Dtos
{
    public record CreatePlaylistDto
    (
        string PlaylistTitle,
        string SeriesTitle,
        string SeasonTitle
    )
    { 
    }

    public record UpdatePlaylistDto
    (
        string PlaylistTitle
    )
    {
    }

    public record PlaylistDto
        (
        Guid PublicPlaylistId,
        string PlaylistTitle
        )
    {
    }
}
