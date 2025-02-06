using MinecraftPlaylistBuilderApp.Server.Dtos;
using MinecraftPlaylistBuilderApp.Server.Interfaces;

namespace MinecraftPlaylistBuilderApp.Server.Services
{
    public class SeasonService : ISeasonService
    {
        private readonly ISeasonRepository _seasonRepository;
        public SeasonService(ISeasonRepository seasonRepository) 
        { 
            _seasonRepository = seasonRepository;
        }
        public async Task<List<SeasonDto>> GetSeasonsBySeriesTitleAsync(string seriesTitle)
        {
            var seasons = await _seasonRepository.GetSeasonsBySeriesTitleAsync(seriesTitle);
            return (seasons.Select(season => new SeasonDto (season.SeasonTitle)).ToList());
        }
    }
}
