using MinecraftPlaylistBuilderApp.Server.Dtos;
using MinecraftPlaylistBuilderApp.Server.Interfaces;

namespace MinecraftPlaylistBuilderApp.Server.Services
{
    public class SeriesService : ISeriesService
    {
        private readonly ISeriesRepository _seriesRepository;

        public SeriesService(ISeriesRepository seriesRepository)
        {
            _seriesRepository = seriesRepository;
        }

        public async Task<List<SeriesDto>> GetAllSeriesAsync()
        {
            var seriesList = await _seriesRepository.GetAllSeriesAsync();
            return seriesList.Select(series => new SeriesDto(series.SeriesTitle)).ToList();
        }
    }
}
