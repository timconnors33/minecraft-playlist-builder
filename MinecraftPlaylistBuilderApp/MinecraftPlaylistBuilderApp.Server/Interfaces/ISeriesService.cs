using MinecraftPlaylistBuilderApp.Server.Dtos;

namespace MinecraftPlaylistBuilderApp.Server.Interfaces
{
    public interface ISeriesService
    {
        Task<List<SeriesDto>> GetAllSeriesAsync();

    }
}
