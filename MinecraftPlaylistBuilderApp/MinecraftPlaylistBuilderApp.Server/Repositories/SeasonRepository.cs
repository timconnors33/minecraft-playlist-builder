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
        public async Task<ICollection<Season>> GetSeasonsBySeriesTitleAsync(string seriesTitle)
        {
            // TODO: Check whether more rigorous string comparison method is needed
            var matchingSeries = await _context.Series.SingleOrDefaultAsync(series => series.SeriesTitle == seriesTitle);
            if (matchingSeries == null)
            {
                return [];
            }
            ICollection<Season> seasons = matchingSeries.Seasons;
            return seasons;
        }
    }
}
