using Microsoft.EntityFrameworkCore;
using MinecraftPlaylistBuilderApp.Server.Interfaces;
using MinecraftPlaylistBuilderApp.Server.Models;

namespace MinecraftPlaylistBuilderApp.Server.Repositories
{
    public class SeasonRepository : ISeasonRepository
    {
        private readonly MinecraftPlaylistBuilderDbContext _context;
        public SeasonRepository(MinecraftPlaylistBuilderDbContext context)
        {
            _context = context;
        }
        public async Task<List<Season>> GetSeasonsBySeriesTitleAsync(string seriesTitle)
        {
            // TODO: Check whether more rigorous string comparison method is needed
            var matchingSeries = await _context.Series.SingleOrDefaultAsync(series => series.SeriesTitle == seriesTitle);
            if (matchingSeries == null)
            {
                return [];
            }
            int matchingSeriesId = matchingSeries.SeriesId;
            List<Season> seasons = await _context.Seasons.Where(season => season.SeriesId == matchingSeriesId).ToListAsync();
            return seasons;
        }
    }
}
