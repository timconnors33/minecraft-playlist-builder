using MinecraftPlaylistBuilderApp.Server.Models;

namespace MinecraftPlaylistBuilderApp.Server.Interfaces
{
    public interface IPlaylistRepository
    {
        Task<List<Playlist>> GetAllByOwnerAsync(Guid ownerId);
        Task<Playlist> GetPlaylistAsync(Guid playlistId);
        Task<Playlist> CreatePlaylistAsync(Playlist playlist);
        Task<Playlist> UpdatePlaylistAsync(Guid playlistId, Playlist newPlaylist);
        Task<bool> DeletePlaylistAsync(Guid playlistId);
    }
}
