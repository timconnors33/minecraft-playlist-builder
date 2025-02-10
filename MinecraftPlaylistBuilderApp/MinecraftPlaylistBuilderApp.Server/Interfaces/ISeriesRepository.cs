using MinecraftPlaylistBuilderApp.Server.Models;

namespace MinecraftPlaylistBuilderApp.Server.Interfaces
{
    public interface ISeriesRepository
    {
        Task<ICollection<Series>> GetAllSeriesAsync();
    }
}
