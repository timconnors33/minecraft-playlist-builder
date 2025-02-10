using MinecraftPlaylistBuilderApp.Server.Models;

namespace MinecraftPlaylistBuilderApp.Server.Interfaces
{
    public interface ISeasonRepository
    {
        Task<ICollection<Season>> GetSeasonsBySeriesTitleAsync(string seriesTitle);
    }
}
