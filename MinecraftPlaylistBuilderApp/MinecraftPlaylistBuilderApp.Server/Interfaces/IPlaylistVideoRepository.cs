using MinecraftPlaylistBuilderApp.Server.Models;

namespace MinecraftPlaylistBuilderApp.Server.Interfaces
{
    public interface IPlaylistVideoRepository
    {
        Task<List<PlaylistVideo>> GetPlaylistVideosByPlaylistIdAsync(Guid publicPlaylistId);
        Task<PlaylistVideo> GetPlaylistVideoByIdAsync(Guid publicPlaylistVideoId);
        Task<PlaylistVideo> CreatePlaylistVideoAsync(PlaylistVideo playlistVideo);
        Task<PlaylistVideo> UpdatePlaylistVideoAsync(Guid playlistVideoId, PlaylistVideo newPlaylistVideo);
        Task<bool> DeletePlaylistVideoAsync(Guid playlistVideoId);
    }
}
