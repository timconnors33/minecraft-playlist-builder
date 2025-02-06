using MinecraftPlaylistBuilderApp.Server.Dtos;

namespace MinecraftPlaylistBuilderApp.Server.Interfaces
{
    public interface ISeasonService
    {
        Task<List<SeasonDto>> GetSeasonsBySeriesTitleAsync(string seriesTitle);
    }
}
