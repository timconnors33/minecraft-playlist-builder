using MinecraftPlaylistBuilderApp.Server.Models;

namespace MinecraftPlaylistBuilderApp.Server.Interfaces
{
    public interface ISeriesRepository
    {
        Task<List<Series>> GetAllSeriesAsync();
    }
}
