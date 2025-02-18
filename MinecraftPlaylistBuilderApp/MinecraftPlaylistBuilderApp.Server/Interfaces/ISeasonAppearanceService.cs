using MinecraftPlaylistBuilderApp.Server.Dtos;

namespace MinecraftPlaylistBuilderApp.Server.Interfaces
{
    public interface ISeasonAppearanceService
    {
        Task<SeasonAppearanceDto> GetSeasonAppearanceDataAsync();
    }
}
