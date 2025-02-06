using MinecraftPlaylistBuilderApp.Server.Models;

namespace MinecraftPlaylistBuilderApp.Server.Interfaces
{
    public interface ISeasonRepository
    {
        Task<List<Season>> GetSeasonsBySeriesTitleAsync(string seriesTitle);
    }
}
