using MinecraftPlaylistBuilderApp.Server.Dtos;
using MinecraftPlaylistBuilderApp.Server.Interfaces;

namespace MinecraftPlaylistBuilderApp.Server.Services
{
    public class SeasonAppearanceService : ISeasonAppearanceService
    {
        private readonly ISeasonAppearanceRepository _repository;

        public SeasonAppearanceService(ISeasonAppearanceRepository repository)
        {
            _repository = repository;
        }
        public async Task<List<SeasonAppearanceDto>> GetAllSeasonAppearancesAsync()
        {
            var seasonAppearances = await _repository.GetAllSeasonAppearancesAsync();
            if (seasonAppearances == null || !seasonAppearances.Any())
            {
                return [];
            }
            var seasonAppearanceDtos = new List<SeasonAppearanceDto>();
            foreach (var seasonAppearance in seasonAppearances)
            {
                seasonAppearanceDtos.Add(new SeasonAppearanceDto(
                    seasonAppearance.Season.Series.SeriesTitle,
                    seasonAppearance.Season.SeasonTitle,
                    seasonAppearance.Channel.ChannelName,
                    seasonAppearance.Channel.ChannelYouTubeId,
                    seasonAppearance.Channel.ChannelThumbnailUri
                    ));
            }
            return seasonAppearanceDtos;
        }
    }
}
