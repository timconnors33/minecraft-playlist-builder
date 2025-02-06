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

        public async Task<List<Channel>> GetChannelsBySeriesSeasonTitlesAsync(string seriesTitle, string seasonTitle)
        {
            var matchingSeries = await _context.Series.SingleOrDefaultAsync(series => series.SeriesTitle == seriesTitle);
            if (matchingSeries == null)
            {
                return [];
            }
            var matchingSeriesId = matchingSeries.SeriesId;

            var matchingSeason = await _context.Seasons.SingleOrDefaultAsync(season => (season.SeriesId == matchingSeriesId) && (season.SeasonTitle == seasonTitle));
            if (matchingSeason == null)
            {
                return [];
            }
            var matchingSeasonId = matchingSeason.SeasonId;

            var seasonAppearances = await _context.SeasonAppearances.Where(seasonAppearance => seasonAppearance.SeasonId == matchingSeasonId).ToListAsync();
            if (seasonAppearances == null || !seasonAppearances.Any())
            {
                return [];
            }
            var channels = new List<Channel>();

            foreach (var seasonAppearance in seasonAppearances)
            {
                var matchingChannel = await _context.Channels.SingleOrDefaultAsync(channel => channel.ChannelId == seasonAppearance.ChannelId);
                if (matchingChannel != null)
                {  
                    channels.Add(matchingChannel); 
                }
            }
            return channels;
        }
    }
}
