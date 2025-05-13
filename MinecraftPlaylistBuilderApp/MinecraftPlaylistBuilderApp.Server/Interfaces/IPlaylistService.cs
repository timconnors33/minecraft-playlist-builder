using MinecraftPlaylistBuilderApp.Server.Dtos;

namespace MinecraftPlaylistBuilderApp.Server.Interfaces
{
    public interface IPlaylistService
    {
        Task<List<PlaylistDto>> GetAllAsync(Guid userId);
        Task<PlaylistDto> GetPlaylistAsync(Guid playlistId, Guid userId);
        Task<PlaylistDto> CreatePlaylistAsync(CreatePlaylistDto CreatePlaylistDto, Guid userId);
        Task<PlaylistDto> UpdatePlaylistAsync(UpdatePlaylistDto updatePlaylistDto, Guid userId, Guid playlistId);
        Task<bool> DeletePlaylistAsync(Guid userId, Guid playlistId);
    }
}
