using Microsoft.EntityFrameworkCore;
using MinecraftPlaylistBuilderApp.Server.Interfaces;
using MinecraftPlaylistBuilderApp.Server.Models;

namespace MinecraftPlaylistBuilderApp.Server.Repositories
{
    public class ChannelRepository : IChannelRepository
    {
        private readonly MinecraftPlaylistBuilderDbContext _context;

        public ChannelRepository(MinecraftPlaylistBuilderDbContext context)
        {
            _context = context;
        }

        public async Task<ICollection<Channel>> GetChannelsBySeriesSeasonTitlesAsync(string seriesTitle, string seasonTitle)
        {
            var matchingSeries = await _context.Series.SingleOrDefaultAsync(series => series.SeriesTitle == seriesTitle);
            if (matchingSeries == null)
            {
                return [];
            }
            var season = matchingSeries.Seasons.SingleOrDefault(s => s.SeasonTitle == seasonTitle);
            if (season == null)
            {
                return [];
            }
            var seasonAppearances = season.SeasonAppearances;
            if (seasonAppearances == null || !seasonAppearances.Any())
            {
                return [];
            }
            var channels = new List<Channel>();

            foreach (var seasonAppearance in seasonAppearances)
            {
                var matchingChannel = seasonAppearance.Channel;
                if (matchingChannel != null)
                {  
                    channels.Add(matchingChannel); 
                }
            }
            return channels;
        }
    }
}
