using MinecraftPlaylistBuilderApp.Server.Dtos;

namespace MinecraftPlaylistBuilderApp.Server.Interfaces
{
    public interface IPlaylistVideoService
    {
        Task<List<PlaylistVideoDto>> GetPlaylistVideosByPlaylistIdAsync(Guid userId, Guid playlistId);
        Task<PlaylistVideoDto> GetPlaylistVideoByIdAsync(Guid userId, Guid playlistId, Guid playlistVideoId);
        Task<List<PlaylistVideoDto>> CreatePlaylistVideosAsync(Guid userId, Guid playlistId, CreatePlaylistVideoDto createPlaylistVideoDto);
        Task<PlaylistVideoDto> UpdatePlaylistVideoAsync(Guid userId, Guid playlistId, Guid playlistVideoId, UpdatePlaylistVideoDto updatePlaylistVideoDto);
        Task<bool> DeletePlaylistVideoAsync(Guid userId, Guid playlistId, Guid playlistVideoId);
    }
}
