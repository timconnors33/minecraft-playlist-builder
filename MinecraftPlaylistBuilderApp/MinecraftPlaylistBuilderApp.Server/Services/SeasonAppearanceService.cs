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
        public async Task<SeasonAppearanceDto> GetSeasonAppearanceDataAsync()
        {
            var seriesList = await _repository.GetAllSeriesAsync();
            if (seriesList == null || !seriesList.Any())
            {
                return null;
            }
            var seriesDtos = new List<SeasonAppearanceSeriesDto>();
            foreach (var series in seriesList)
            {
                var seriesSeasons = new List<SeasonAppearanceSeasonDto>();
                foreach (var season in series.Seasons)
                {
                    var seasonChannels = new List<SeasonAppearanceChannelDto>();
                    foreach (var seasonAppearance in season.SeasonAppearances)
                    {
                        var channel = new SeasonAppearanceChannelDto
                            (
                                seasonAppearance.Channel.ChannelName,
                                seasonAppearance.Channel.ChannelYouTubeId,
                                seasonAppearance.Channel.ChannelThumbnailUri
                            );
                        seasonChannels.Add(channel);
                    }
                    var seasonDto = new SeasonAppearanceSeasonDto
                        (
                            season.SeasonTitle,
                            seasonChannels
                        );
                    seriesSeasons.Add(seasonDto);
                }
                var seriesDto = new SeasonAppearanceSeriesDto
                    (
                        series.SeriesTitle,
                        seriesSeasons
                    );
                seriesDtos.Add(seriesDto);
            }
            var seasonAppearanceDto = new SeasonAppearanceDto(seriesDtos);
            return seasonAppearanceDto;
        }
    }
}
