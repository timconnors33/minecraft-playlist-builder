using MinecraftPlaylistBuilderApp.Server.Models;

namespace MinecraftPlaylistBuilderApp.Server.Interfaces
{
    public interface ISeasonAppearanceRepository
    {
        Task<List<SeasonAppearance>> GetAllSeasonAppearancesAsync();
    }
}
